from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from random import randint
from .util import check_cost, get_drops
from .models import User, Mineral, Mine, Dwarf, Upgrade, Upgrade_owned, Job


# defining the amount of dwarf portraits (found in static/dwarves/media)
amount_portraits = 20


# renders the all dwarves page
def all_dwarves(request):
    dwarves_list = Dwarf.objects.all()
    return render(request, "dwarves/all_dwarves.html",{
        "page_title" : "All Dwarves",
        "dwarves" : dwarves_list,
    })


# renders the all dwarves page with only the users dwarves
@login_required(login_url='login')
def my_dwarves(request):
    dwarves_list = request.user.user_dwarfs.all()
    return render(request, "dwarves/all_dwarves.html",{
        "page_title" : "My Dwarves",
        "dwarves" : dwarves_list
    })


# renders the leaderboard page
def leaderboard(request):
    users = User.objects.order_by("-gold_obtained")
    return render(request, "dwarves/leaderboard.html",{
        "users" : users
    })


# renders the mining page
@login_required(login_url='login')
def mining(request):
    mines = Mine.objects.all()

    # grab all the jobs that belong to one of the users dwarfs
    active_jobs = Job.objects.filter(dwarf__in=request.user.user_dwarfs.all())
    active_mines = []
    active_dwarves = []
    for job in active_jobs:
        active_dwarves.append(job.dwarf.name)
        active_mines.append(job.mine)

    # grab all the dwarves the users dwarves without jobs
    inactive_dwarves = request.user.user_dwarfs.exclude(name__in=active_dwarves)
    dwarves_count = request.user.user_dwarfs.all().count()

    return render(request, "dwarves/mining.html",{
        "mines" : mines,
        "active_mines" : active_mines,
        "active_jobs" : active_jobs,
        "inactive_dwarves" : inactive_dwarves,
        "dwarves_count" : dwarves_count,
    })

# handle the start mining posts
def start_mining(request, name):
    if request.method == "POST":
        form = SelectionForm(request.POST)
        if form.is_valid():
            dwarf_name = form.cleaned_data["dwarf"]
            dwarf = request.user.user_dwarfs.get(name = dwarf_name)
            mine = Mine.objects.get(name=name)

            # only create a new job if that mine doesn't have a job
            try:
                Job.objects.get(dwarf__in=request.user.user_dwarfs.all(), mine=mine)
            except ObjectDoesNotExist:

                # only create a new job if that dwarf does not already have a job
                try:
                    Job.objects.get(dwarf=dwarf)
                except ObjectDoesNotExist:
                    new_job = Job(start_time = timezone.now(), dwarf=dwarf, mine=mine)
                    new_job.save()
    return redirect("mining")

# handle the stop mining posts
def stop_mining(request, name):
    if request.method == "POST":
        active_jobs = Job.objects.filter(dwarf__in=request.user.user_dwarfs.all())

        # try to get the current job if that job still exists else do nothing
        try:
            current_job = active_jobs.get(mine=Mine.objects.get(name=name))

            # calculate the drops via the get_drops util function
            drops = get_drops(current_job)
            current_job.delete()
            for drop in drops:
                if drop[1] != 0:

                    # create the mineral if it does not exist yet
                    try:
                        mineral = request.user.inventory.get(name=drop[0])
                    except ObjectDoesNotExist:
                        mineral = Mineral(name=drop[0], user=request.user)
                    mineral.value += drop[1]
                    mineral.save()

                    # if the mineral is gold update gold_obtained
                    if drop[0] == "Gold":
                        request.user.gold_obtained += drop[1]
                        request.user.save()
                    messages.info(request, f"You mined {drop[1]} {drop[0]}!")
        except ObjectDoesNotExist:
            pass

    return redirect("mining")


# a simple selectionform to fill user submitted input
class SelectionForm(forms.Form):
    dwarf = forms.CharField(label="", widget=forms.TextInput(attrs={"placeholder":"Name of new Dwarf"})) 


# render the upgrade page
@login_required(login_url='login')
def upgrading(request, name):

    # try to get the users dwarf else redirect user to selection page
    try:
        dwarf = request.user.user_dwarfs.get(name = name)
    except ObjectDoesNotExist:
        return redirect("select")

    # filter out the normal upgrades from the new dwarf upgrades
    upgrades = Upgrade.objects.exclude(name__istartswith="new_dwarf")
    new_dwarf_upgrades = Upgrade.objects.filter(name__istartswith="new_dwarf")

    dwarf_upgrades_owned = dwarf.dwarf_upgrades.all()
    dwarf_upgrades_owned = dwarf_upgrades_owned.exclude(amount_owned = 0)
    dwarf_upgrades = []
    for upgrade_owned in dwarf_upgrades_owned:
        dwarf_upgrades.append(upgrade_owned.upgrade)
    dwarves_count = request.user.user_dwarfs.all().count()

    return render(request, "dwarves/upgrading.html",{
        "page_title" : f"Upgrading {name}",
        "dwarf" : dwarf,
        "upgrades" : upgrades,
        "dwarf_upgrades_owned" : dwarf_upgrades_owned,
        "dwarf_upgrades" : dwarf_upgrades,
        "new_dwarf_upgrades" : new_dwarf_upgrades,
        "dwarves_count" : dwarves_count,
        "form" : SelectionForm(),
    })


# handle the stop mining posts
@login_required(login_url='login')
def new_dwarf(request, upgrade, name):
    if request.method == "POST":
        upgrade = Upgrade.objects.get(name=upgrade)
        form = SelectionForm(request.POST)
        if form.is_valid() and upgrade.requirement == request.user.user_dwarfs.count():
            dwarf_name = form.cleaned_data["dwarf"]

            # check if the user has a dwarf with the same name
            dwarf_names = request.user.user_dwarfs.all().values_list("name",flat=True)
            if dwarf_name.lower() not in [x.lower() for x in dwarf_names]:

                # check if user can afford upgrade then create new dwarf
                if check_cost(request.user, upgrade, 0):
                    new_dwarf = Dwarf(user = request.user, name=dwarf_name, portrait = "portrait" + str(randint(1,amount_portraits)) + ".png")
                    new_dwarf.save()
                    messages.success(request, f"Succesfully added new dwarf!")
                else:
                    messages.error(request, f"You dont have enough Minerals for a new dwarf!")
            else:
                messages.error(request, f"You already have a dwarf named: {dwarf_name}")
    return redirect("upgrading", name)


# handle the regular upgrades
@login_required(login_url='login')
def buy_upgrade(request, name, upgrade):
    if request.method == "POST":
        dwarf = request.user.user_dwarfs.get(name = name)
        upgrade = Upgrade.objects.get(name=upgrade)

        # check if the dwarf already has the upgrade else create it
        try:
            new_upgrade = Upgrade_owned.objects.get(dwarf=dwarf, upgrade=upgrade)
        except ObjectDoesNotExist:
            new_upgrade = Upgrade_owned(dwarf=dwarf, upgrade=upgrade)

        # buy the upgrade if the user can afford it
        if check_cost(request.user, upgrade, new_upgrade.amount_owned):
            new_upgrade.amount_owned += 1
            new_upgrade.save()
            dwarf.speed = round(dwarf.speed + upgrade.speed, 2)
            dwarf.capacity += upgrade.capacity
            dwarf.discovery = round(dwarf.discovery + upgrade.discovery, 2)
            dwarf.save()
            messages.success(request, f"Succesfully bought: {upgrade.name}!")
        else:
            messages.error(request, f"You dont have enough Minerals for: {upgrade.name}!")
        
    return redirect("upgrading", name)


# renders the selection page
@login_required(login_url='login')
def select(request):
    dwarves_list = request.user.user_dwarfs.all()
    return render(request, "dwarves/select.html",{
        "page_title" : "Select a Dwarf for Upgrading",
        "dwarves" : dwarves_list
    })


# renders the users inventory page
@login_required(login_url='login')
def inventory(request):
    user_inventory = request.user.inventory.all()
    return render(request, "dwarves/inventory.html", {
        "inventory" : user_inventory,
    })


# renders the login page
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("all_dwarves"))
        else:
            return render(request, "dwarves/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "dwarves/login.html")


# renders the login page
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("all_dwarves"))


# renders the register page
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "dwarves/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "dwarves/register.html", {
                "message": "Username already taken."
            })
        login(request, user)

        # create a users first dwarf
        dwarf = Dwarf(name=user.username, user=user, portrait = "portrait" + str(randint(1,amount_portraits)) + ".png")
        dwarf.save()
        mineral = Mineral(user=user, name="Gold", value=0)
        mineral.save()

        return HttpResponseRedirect(reverse("all_dwarves"))
    else:
        return render(request, "dwarves/register.html")

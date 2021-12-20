from django import template
from django.utils import timezone


register = template.Library()


# filter to calculate the time before a job is finished
@register.filter(name='time_remaining')
def time_remaining(job):
    time = timezone.now() - job.start_time
    time = time.seconds / 60
    rate = job.mine.rate / 60
    remainder = job.dwarf.capacity / (rate * job.dwarf.speed) - time
    if remainder <= 0:
        return 0
    else: 
        return round(remainder,1)


# filter to calculate the progress of a job
@register.filter(name='progress')
def progress(job):
    time = timezone.now() - job.start_time
    time = time.seconds / 60
    rate = job.mine.rate / 60
    if rate * time * job.dwarf.speed > job.dwarf.capacity:
        return job.dwarf.capacity
    else:
        return round(rate * job.dwarf.speed * time)


# formats the effect of an upgrade nicely
@register.filter(name='get_effect')
def get_effect(upgrade):
    effect = ""
    if upgrade.speed != 0:
        effect += f" +{upgrade.speed} Speed"
    if upgrade.capacity != 0:
        effect += f" +{upgrade.capacity} Capacity"
    if upgrade.discovery != 0:
        effect += f" +{upgrade.discovery} Discovery"
    return effect


# calculates the cost based on the amount of upgrades the dwarf already has
@register.filter(name='cost_complete')
def cost_complete(value, amount):

    # the cost increases by 50% each time
    new_value = value * (1.50 ** amount)
    new_value = round(new_value)
    return new_value


# gets the actual name of the mine (skipping the word "the")
@register.filter(name='get_mine_name')
def get_mine_name(name):
    if name.split(' ', 1)[0].lower() == "the":
        return name.split(' ', 1)[1]
    else:
        return name.split(' ', 1)[0]





# this file contains a bunch of utility functions used in views.py


from random import random
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone


# buys an upgrade if the user can pay
def check_cost(user, upgrade, amount_owned):
    price = upgrade.cost.all()
    inventory = user.inventory.all()

    # check if the user can pay for the upgrade
    for mineral in price:
        try:
            user_mineral = inventory.get(name=mineral.name)
        except ObjectDoesNotExist:
            return False
        if user_mineral.value < cost_complete(mineral.value, amount_owned):
            return False
    
    # buy the upgrade
    for mineral in price:
        user_mineral = inventory.get(name=mineral.name)
        user_mineral.value = user_mineral.value - cost_complete(mineral.value, amount_owned)
        user_mineral.save()
    return True


# calculates the actual cost based on the amount of upgrades already owned
def cost_complete(value, amount):

    # the cost increases by 50%
    new_value = value * (1.50 ** amount)
    new_value = round(new_value)
    return new_value


# the algorithm to calculate the drops
def get_drops(job):

    # calculate how much time has passed
    time = (timezone.now() - job.start_time).seconds / 60
    drop_rate = job.mine.rate / 60
    minerals = job.mine.minerals.all()
    drops = []
    chances = calculate_chance(minerals, job.dwarf.discovery)
    total_value = 0

    # for each mineral calculate the amount the user will receive
    for mineral in minerals:
        value = round((drop_rate * time * job.dwarf.speed) * chances[mineral.name])
        drops.append([mineral.name, value])
        total_value += value

    # shrink down drops if outside of capacity
    if job.dwarf.capacity < total_value:
        factor = job.dwarf.capacity/total_value
        drops = [[drop[0], round(drop[1]*factor)] for drop in drops]
    return drops


# used in the drops algorithm to calculate chances
def calculate_chance(minerals, discovery):

    # drop table of chances; chances are chosen based on playtesting
    # the chances are effected by discovery
    drop_table = {"Common" : 0.68, "Uncommon" : 0.25 * ((discovery - 1) * 0.5 + discovery),
                    "Rare" : 0.06 * discovery, "Very Rare" : 0.01 * discovery}
    chances = {}
    total_chance = 0
    for mineral in minerals:
        chance = drop_table[mineral.rarity] * random()
        chances[mineral.name] = chance
        total_chance += chance

    # standardize the chances to sum to 1
    for name in chances:
        chances[name] = chances[name] / total_chance
    return chances
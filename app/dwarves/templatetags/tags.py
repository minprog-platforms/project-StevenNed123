from django import template
from django.utils import timezone
register = template.Library()

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

@register.filter(name='progress')
def progress(job):
    time = timezone.now() - job.start_time
    time = time.seconds / 60
    rate = job.mine.rate / 60
    if rate * time * job.dwarf.speed > job.dwarf.capacity:
        return job.dwarf.capacity
    else:
        return round(rate * job.dwarf.speed * time)

@register.filter(name='get_effect')
def get_effect(upgrade):
    effect = ""
    if upgrade.speed != 0:
        effect += f"+{upgrade.speed} Mining Speed"
    if upgrade.capacity != 0:
        effect += f"+{upgrade.capacity} Capacity"
    if upgrade.discovery != 0:
        effect += f"+{upgrade.discovery} Discovery"
    return effect

@register.filter(name='cost_complete')
def cost_complete(value, amount):
    new_value = value * (1.25 ** amount)
    new_value = round(new_value)
    return new_value






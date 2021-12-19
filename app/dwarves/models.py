from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, FloatField, IntegerField
from django.db.models.fields.related import ForeignKey
from django.utils import timezone


# defining all the different minerals
possible_minerals = [('Gold', 'gold'), ('Clay', 'clay'), ('Iron', 'iron'), ('Coal', 'coal'),
                     ('Tin', 'tin'), ('Zinc', 'zinc'),('Jade', 'jade'), ('Copper', 'copper'), 
                     ('Silver', 'silver'), ("Mithril", "mithril"), ('Marble', 'marble'), ('Quartz', 'quartz')]


# user model to store usernames and passwords
class User(AbstractUser):
    gold_obtained = models.IntegerField(default=0)


# store information about the mines
class Mine(models.Model):
    name = models.CharField(max_length=64)
    rate = models.IntegerField(default=0)
    requirement = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.name}"


# store information about the dwarves
class Dwarf(models.Model):
    name = models.CharField(max_length=64)
    user = ForeignKey(User, related_name="user_dwarfs", on_delete=CASCADE)
    portrait = models.CharField(max_length=64,default="portrait1.png")
    speed = FloatField(default=1)
    capacity = models.IntegerField(default=100)
    discovery = FloatField(default=1)
    def __str__(self):
        return f"{self.user}, {self.name}"


# job model, when a dwarf starts working in a mine a job is created
class Job(models.Model):
    mine = ForeignKey(Mine, on_delete=CASCADE, related_name="mine_jobs")
    dwarf = ForeignKey(Dwarf, on_delete=CASCADE, related_name="dwarf_jobs")
    start_time = models.DateTimeField(default=timezone.now())
    def __str__(self):
        return f"{self.dwarf} in {self.mine}"


# store information about the upgrades
class Upgrade(models.Model):
    name = CharField(max_length=64)
    speed = FloatField(default=0)
    capacity = IntegerField(default=0)
    discovery = FloatField(default=0)
    requirement = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.name}"
        

# links a dwarf to an upgrade
class Upgrade_owned(models.Model):
    dwarf = ForeignKey(Dwarf, related_name="dwarf_upgrades", on_delete=CASCADE)
    upgrade = ForeignKey(Upgrade, related_name="upgrade_dwarfs", on_delete=CASCADE)
    amount_owned = IntegerField(default=0)
    def __str__(self):
        return f"{self.upgrade}, {self.dwarf}"


# stores information about a mineral
# mineral can be linked to a user, upgrade or mine
class Mineral(models.Model):
    user = ForeignKey(User,blank=True, null=True, default="", on_delete=CASCADE, related_name="inventory")
    upgrade = ForeignKey(Upgrade,blank=True, null=True, default="", on_delete=CASCADE, related_name="cost")
    mine = ForeignKey(Mine,blank=True, null=True, default="", on_delete=CASCADE, related_name="minerals")
    name = models.CharField(max_length=64, choices=possible_minerals)
    value = models.IntegerField(blank=True, null=True, default=0)
    rarity = models.CharField(max_length=64, blank=True, null=True, default='', choices=[
        ('', ''), ('Common', 'common') ,('Uncommon', 'uncommon'), ('Rare', 'rare'), ('Very Rare', 'very_rare')])
    def __str__(self):
        if self.user != None:
            return f"{self.user}, {self.name}, {self.value},"
        elif self.upgrade != None:
            return f"{self.upgrade}, {self.name}, {self.value}"
        else:
            return f"{self.mine}, {self.name}, {self.rarity}"





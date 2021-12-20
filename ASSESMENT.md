# Code Review

## Important things

<ul>

<li>
Made some changes to the admin.py file to be able to easily add different minerals to mines and upgrades.
</li>

<li>
The game has a total of thirteen mines, twelve upgrades and twelve minerals for the player to collect and unlock.
</li>

<li>
Inside of util.py there is a function get_drops that calculates the drops in O(1) without having to loop for every drop.
</li>

<li>
The entire website is made using flexbox, so the elements will adjust with different window sizes.
</li>

<li>
All the different dwarf portraits aswell as the mineral sprites are all drawn by myself using GraphicsGale.
</li>

<li>
Inside of the templatetags folder are some filters that I used inside of the html templates.
</li>

<li>
There are safeguards in place in case a player goes to the previous page and tries to assign the same dwarf to the same mine.
</li>

</ul>

## Big decisions

### linking upgrades to dwarves instead of users
The original design was to link the cost increase of an upgrade to a user instead of a dwarf.
The main problem with this design was that the upgrades are better when combined, for example: a dwarf with higher speed will make better use out of a single point of discovery than a dwarf with lower speed. I was worried that this would disincentivize players from upgrading multiple dwarves. In the end I think this is the right decision based on the playtesting I have done. 

### Creating sprites for minerals instead of mines
The original idea was to create unique sprites for each of the different mines to add some more flavour to each individual mine. 
In the end I decided against it because it would be very time consuming and other things would be more important.
Instead of drawing the sprites for the mines I drew the sprites for the minerals, and I am happy with how they turned out.
As for the Mines, I decided to give them unique background colors instead.

### Balancing of dwarf stats
Because it takes a long time to get through the game I have not had the time to playtest all of it, only the early portions.
Because of this I am worried that later in the game either capacity or speed will outgrow the other and mining will either take really long or really short. I thought that having longer mining times would be better than shorter mining times and therefor decided to make capacity upgrades intentionally a little better than speed upgrades. Another problem that could arise would be because of the way discovery works, you could get a dwarf with such high discovery that they are unable to find common minerals. Altough this has not happened during playtesting, this could potentally lock a player out of progressing because common minerals are necessary to buy a new dwarf upgrade. With this in mind i decided to make the discovery upgrades a little weaker than the other upgrades.



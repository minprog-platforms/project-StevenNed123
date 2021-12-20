# Code Review

reviewed by: Melissa Sam-sin

During the code review there were a couple of important points that could use some improvement:

<ul>
<li>A mineral can have a foreign key to a user, mine or an upgrade but not more than one. 
Also if a mineral is linked to a mine it doesn't have a value and if linked to a user or upgrade it doesn't have a rarity.
This could be more elegently designed by using a GenericForeignKey to multiple different moddels or by restructuring the database by creating different mineral models for each different use.
</li>

<li>
Consistency in the code could be improved, for instance the related name linking a user to their dwarfs is called "user_dwarfs" in the model while in the rest of the code the plural of dwarf is dwarves.
Also possible minerals is defined as a variable at the top of models.py while the choices for rarity are not.
</li>

<li>
Within the html template there are often to many variables in the style attribute. It would make the html templates a lot more clear if the objects had a class and that class was styled in the style sheet.
</li>

<li>
Both the upgrading and mining page require a lot of variables and both have very lengthy complicated html. This could be simplified by creating a filter/tag that on for example the mining page selects the job that is currently going on in that specific mine. Right now this is done by checking if the mine is being mined in and then it loops over all the jobs to select the job that belongs to that mine, probaply not the best way of doing things.
</li>

<li>
The upgrade page makes use of two types of messages and right now an if statement determines which bootstrap element gets displayed with each message. There is however a way to make Django figure this out and not need the if statement. Right now this works fine but with multiple types of messages it could get very messy. 
</li>

</ul>
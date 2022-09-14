Elite Dangerous Classes Library aka `edclasses`

This README is a work in progress.

# What is this library for?
Data about systems, factions and stations in Elite Dangerous at your fingertips!

Elite Dangerous Classes Library provides classes representing various objects in the game "Elite Dangerous" (systems, factions etc.).

Developers can use these classes to speed up developing simple applications working with the game data.

# How to install it?
`pip install elite-dangerous-classes-library`

# How to use it?
Here is an example of how it can be used. Note, that system name is all that needs to be provided. The rest is loaded
from the third party API.
```python
>>> from edclasses import System
>>> sol = System.create(name="Sol")
>>> for faction_branch in sol.faction_branches:
...    print(f"{faction_branch} has {len(faction_branch.stations)} stations.")

Faction 'Sol Constitution Party' in System 'Sol' has 0 stations.
Faction 'Federal Congress' in System 'Sol' has 1 stations.
Faction 'Sol Nationalists' in System 'Sol' has 0 stations.
Faction 'Sol Workers' Party' in System 'Sol' has 3 stations.
Faction 'Mother Gaia' in System 'Sol' has 6 stations.
Faction 'Aegis Core' in System 'Sol' has 0 stations.
```

Generally, even though it's possible to initialize objects directly, it's advised to use the `create` method. Here is why:

```python
>>> from edclasses import System

# trying to create the same object directly causes InstanceAlreadyExists error
>>> system = System("Colonia")
>>> system_2 = System("Colonia")
Error: edclasses.utils.InstanceAlreadyExists

# using "create" method makes sure you get the same instance of System, so you don't have to worry about creating the
# same object twice in two different places:
>>> system = System.create(name="Colonia")
>>> system_2 = System.create(name="Colonia")
>>> system is system_2
True
```

And here is an example of a function which is meant to find a station with mission for particular faction_branch:
```python

# missions.py:

import random
from edclasses import enums

def find_mission(
    faction_branch
):
    stations = faction_branch.stations
    random.shuffle(stations)

    for station in stations:
        if enums.StationService.MISSIONS in station.services:
            return {"faction_branch": faction_branch, "station": station}
    return None

>>> from missions import find_mission
>>> from edclasses import FactionBranch, Faction, System
>>> my_faction = Faction.create(name="Mother Gaia")
>>> my_system = System.create(name="Sol")
>>> my_faction_branch = FactionBranch.create(faction=my_faction, system=my_system)
>>> mission_data = find_mission(my_faction_branch)
>>> mission_station = mission_data["station"]
>>> print(f"TRANSMISSION RECIEVED")
>>> print(f"Commander, your presence is required at {mission_station} in the {mission_station.system}!")

TRANSMISSION RECIEVED
Commander, your presence is required at Ocellus 'Columbus' in the System 'Sol'!
```

Generally the library should let you focus on the logic of your application, instead of dealing with Elite Dangerous
data structure for 100th time.

# What classes are included?
Currently the following objects are represented:
- System - single star system
- Faction - faction entity, galaxy-wide
- FactionBranch - representation of a faction within a single system.
- OrbitalStation - station inside a system.

The classes are not a full representation - such objects would be expensive to work with. However, they can be easily
extended if you need to add a particular attribute. They will definitely be extended gradually in the future, as new
needs show up.

# How are relations between objects kept?
There is a special class representing parent-children relation (one-to-many). It takes care of updating both sides of
the relation. For example, when OrbitalStation instance changes its attribute `controlling_faction`, the attribute `stations` on the
FactionBranch instance is also updated, and vice versa. The parent is kept in sync with the children.

# Can I use the classes without external data source?
From now on - Yes! The whole adapter engine has been extracted, so now, apart from full auto-refreshed classes available
in the `classes` module, you can use the "offline" Model classes available in the `models` module.

## Model classes
They represent objects (factions, systems, faciton branches and stations) and keep the relation between them, but they
are static objects, not connected to any external data source. If you use these classes, they will only store the data
you have filled them with. For example. creating a SystemModel of system Sol will no longer let you fetch data about
"Sol" system:

```python
from edclasses.models import SystemModel

sol_model = SystemModel.create(name="Sol")
# the model has the same attributes ed class has, however it will not look for data anywhere else:

print(sol_model.stations)
[]
# A normal instance of System class would at this point query API Adapter for data, but the model doesn't do that.
```

### Advantages
Is there anything special about the model class itself if it doesn't fetch the data? Well, yes - relations. The model
classes are meant to work like a database - keep links between different objects in your program. Look at this example:

```python
>>> from edclasses.models import SystemModel, FactionModel, FactionBranchModel

>>> sol = SystemModel.create(name="Sol")
>>> sol.faction_branches
[]

>>> faction = FactionModel.create(name="Some Faction")
>>> faction.faction_branches
[]

>>> faction_branch = FactionBranchModel.create(faction=faction, system=sol)
# at these point the relations between are updated:

>>> sol.faction_branches
[Some Faction in Sol]

>>> faction.faction_branches
[Some Faction in Sol]
```

How can this be useful? Even though `edlasses` have been designed to be used with the API, maybe you have some idea
to create a whole universe simulation based on a CSV file on some Database of your own? This objects should make it
possible to do so without writing your own classes.

# Where is the data coming from?
The library comes with a simple adapter to a magnificent API at www.elitebgs.app (seriously, they made a great job, you
should check it out if you haven't already).
Every response is cached to avoid spamming the API with too many requests.
Apart from that, the API client is limited to 20 requests per minute. In the current representation breaking this limit
will raise RateLimitException. This behaviour might change in the future.

# When is the data loaded?
The attributes are lazy, which means they get filled with data as you access them. For example:
```python
sol = System.create(name="Sol") # no data is being sent at this point

print(sol.stations) # request for the data about stations is being made.
print(sol.stations) # data is already there, no request is being made
```

[//]: # (TODO: add info about how caching works)

# Any words of advice?
The library stores the whole data in the memory - which means, it might be expensive. I've designed it to work
with small scripts which I plan to use along VoiceAttack, to enrich my experience while playing. It's not meant for
massive data analysis, to be used on web servers etc. - it's designed to work with a few systems of interest, or a few
factions of interests. If your app is too data-hungry, it will result in the following problems:
- you will send too many requests to the API, causing rate limit error (or even a ban - respect the APIs!)
- your application will work slowly - the more data the app has to keep track of, the slower it runs
- you might run out of memory.

# Can I use different data sources? Can I add more fields?
Yes, the provided EliteBgsApiAdapter is just an example. You can write a similar adapter, or extend this one, and then
connect it to the proper class in edclasses. I will add a more detailed tutorial in the future.

You can also use the model classes (check out ## model classes above) and create your own data source system.

# Why don't you XYZ:
The project is in very early phase. Have any idea? Please open an issue, I would be glad to discuss.

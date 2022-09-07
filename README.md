Elite Dangerous Classes Library aka `edclasses`

This README is a work in progress.

# What is this library for?
It's a library providing classes representing various objects in the game "Elite Dangerous" (systems, factions etc.)
Developers can use these classes to speed up developing simple applications working with the game data.

Apart from the objects representation, it also provides an architecture to fill the objects with data from APIs.

# How to install it?
`pip install edclasses`

# How to use it?
Here is an example of how it can be used. Note, that system name is all that needs to be provided. The rest is loaded
from the third party API.
```python
from edclasses import System, Faction, FactionBranch, OrbitalStation

sol = System.create(name="Sol")

for faction_branch in sol.faction_branches:
    print(f"{faction_branch} has {len(faction_branch.stations)}.")
```

And here is an example of a function which is meant to find a station with mission for particular faction_branch:
```python
def find_mission(
    faction_branch
):
    stations = faction_branch.stations
    random.shuffle(stations)

    for station in stations:
        if enums.StationService.MISSIONS in station.services:
            return {"faction_branch": faction_branch, "station": station}
    return None

my_faction_branch = settings.MY_FACTION_BRANCH
mission_data = find_mission(my_faction_branch)
mission_station = mission_data["station"]
print(f"TRANSMISSION RECIEVED")
print(f"Commander, your presence is required at {mission_station} in the {mission_station.system}!")
```

Generally the library should let you focus on the logic of your application, instead of dealing with Elite Dangerous
data structure for 100th time.

# What classes are included?
Currently the following objects are represented:
- System - single star system
- Faction - faction entity, galaxy-wide
- FactionBranch - representation of a faction within a single system.
- OrbitalStation - station inside a system.

The classes are not a full representation - such objects would be expensive to work with, and probably noone would need
that. However, they can be easily extended if you need to add a particular attribute. They will definitely be extended
gradually in the future, as new needs show up.

# How are relations between objects kept?
There is a special class representing parent-children relation (one-to-many). It takes care of updating both sides of
the relation. For example, when OrbitalStation instance changes its attribute `controlling_faction`, the attribute `stations` on the
FactionBranch instance is also updated, and vice versa. The parent is kept in sync with the children.

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

# Why don't you XYZ:
The project is in very early phase. Have any idea? Please open an issue, I would be glad to discuss.

# - New `enemy_director.py`: an **open-ended wave generator** — reseeds the formation Galaga-style (anti-camping: enemies replenish if you stall), never "completes," and ramps difficulty by wave count/time (speed, aggression, diver count).
# - This also kills the dead `enemy_count` variable and the buggy `enemy_list[i]` indexing.
#
# **Research pointers**
# - "Galaga wave system / enemy restock mechanic" — waves keep refilling a stage if you camp.
# - "difficulty scaling curves in arcade games".
# - Add a lightweight **tick/timer/scheduler** helper so the game can choreograph entrance fly-ins, dive calls, and formation restocks on a schedule.

from assets.enemy import Enemy


def scheduler(dt):
    """
    This funciton should keep track of how much time has passed.
    I am thinking I can use modulo arithmatic to have enemies spawn every x seconds or whatever.
    """
    pass


def enemy_director(dt):
    """
    This function should spawn an enemy (or an enemy formation?) using scheduler.
    """
    pass

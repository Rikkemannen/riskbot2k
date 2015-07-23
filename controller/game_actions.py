# coding: latin1
from random import randint


def throw_die(throws):
    throws = min(throws, 3)
    throw_list = []
    for throw in range(0, throws):
        throw_list.append(randint(1, 6))
    return throw_list


def combat(attacker, defender):
    return attacker if attacker > defender else defender


def battle(attacker, defender, soldiers_left):
    attacker_dies = throw_die(attacker.get_soldiers() - soldiers_left)
    if defender.get_soldiers() > 2:
        defender_dies = throw_die(defender.get_soldiers())
    else:
        defender_dies = throw_die(2)
    nbr_throws = min(len(defender_dies),len(attacker_dies))
    for x in range(0, nbr_throws):
        combat_results = combat(max(attacker_dies), max(defender_dies))
        if combat_results == max(attacker_dies) and combat_results != max(defender_dies):
            defender.set_soldiers(defender.get_soldiers()- 1)
            attacker_dies.pop(attacker_dies.index(combat_results))
            defender_dies.pop(defender_dies.index(max(defender_dies)))
        else:
            attacker.set_soldiers(attacker.get_soldiers()- 1)
            attacker_dies.pop(attacker_dies.index(max(attacker_dies)))
            defender_dies.pop(defender_dies.index(combat_results))
    return defender.get_soldiers() == 0 or attacker.get_soldiers() == soldiers_left

def conquer_territory(winner, looser, soldiers_left):
    if winner.war_status == 'attacker':
        looser.territory.set_owner(winner.territory.get_owner_obj())
        looser.territory.set_soldiers(soldiers_left)
        winner.territory.set_soldiers(winner.territory.get_soldiers()- soldiers_left)

def war(attacker, defender, attacking_soldiers):
    soldiers_left = attacker.territory.get_soldiers() - attacking_soldiers
    if soldiers_left < 1 or attacking_soldiers < 1 :
        raise RuntimeError('u been smokin\' crack, who gon defend u nau?')
    while not battle(attacker.territory,defender.territory, soldiers_left):
        pass
    return defender if defender.get_soldiers() > 0 else attacker
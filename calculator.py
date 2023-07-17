# main damage stats = cc, cd, damage, reload
import copy

import itertools
def parse(perks): # parses what damage perks teh item has
    d = {"cr": [], "cd": [], "dmg": [], "rld":[]}
    for perk in perks:
        if(not isinstance(perk, list)):
            continue
        perk_name = perk[0]
        perk_value = perk[1]
        for ptype in d.keys():
            if(perk_name == ptype):
                d[ptype].append(perk_value)

    return d

def convert_crit_rating(cr):
    cc = (75 * cr)/ (50 + cr)
    decimal = cc % 1

    if(decimal < .25): return int(cc)
    if(decimal < .75): return int(cc)+.5
    else: return int(cc)+ 1


class Trap:
    def __init__(self) -> None:
        self.base_damage = 0
        self.base_crit_chance_p = 0
        self.base_crit_damage_p = 0
        self.base_reload = 0

class DamageCalculator(Trap):
    def calculate_base_stats(self, perks, damage, crit_damage, crit_chance, reload):
        self.base_damage = damage/(1+sum(perks['dmg'])/100) # base_dmg * damage% = new_damage
        self.base_crit_chance_p = crit_chance - convert_crit_rating(sum(perks['cr']))
        self.base_crit_damage_p = (crit_damage/damage)-(1+sum(perks['cd'])/100) # damage * (1+x+perks["cd"]) = cd
        self.base_reload = round(reload * (1+sum(perks['rld'])/100), 1) # new_reload = reload/(1+perks)


    def calculate_damage(self, perks, shots=10):
        calculated_damage = self.base_damage*(1+sum(perks['dmg'])/100)
        crit_chance = (self.base_crit_chance_p + convert_crit_rating(sum(perks['cr'])))/100
        crit_damage = 1 + self.base_crit_damage_p + sum(perks['cd'])/100
        total_damage = ( calculated_damage * (1-crit_chance)) + (calculated_damage * (crit_chance) * crit_damage)
        return total_damage, (100*total_damage/ (round(self.base_reload/(1+sum(perks['rld'])/100), 1) * 99))


# weapon = DamageCalculator()
# weapon.calculate_base_stats(parse(perks), damage, crit_damage, crit_chance, reload)




# print(convert_crit_rating(23))

perk_levels = {
    'dmg': ["dmg", 30],
    'cr': ["cr", 30],
    'cd': ["cd", 135],
    'rld': ["rld", 42],
    "eng": ["dmg", 20],
    "phys": ["dmg", 44]
}

trap = DamageCalculator()

possible_perks = [
    ['phys'],
    ['dmg', 'cr', 'dura'],
    ['cd', 'dura', 'dmg', 'rld'],
    ['dmg', 'cr', 'dura'],
    ['cd', 'dura', 'dmg', 'rld'],
    ['dura']
]

trap.calculate_base_stats(parse([["eng", 20], ["cr", 30],  ['cd', 135], ['damage', 30], ['cd', 135], ['heals builds attatched', 30]]), 5589, 23473.8, 33, 12)

print(trap.base_damage, trap.base_crit_chance_p, trap.base_crit_damage_p, trap.base_reload)

def main():
    all_possible = list(itertools.product(*possible_perks))
    all_possible = list(set(tuple(sorted(sub)) for sub in all_possible))
    _all_possible = copy.deepcopy(all_possible)
    for x, column in enumerate(all_possible):
        all_possible[x] = list(all_possible[x])
        for y, perk in enumerate(column):
            if(perk in perk_levels.keys()):
                all_possible[x][y] = perk_levels[perk]

    # print(all_possible)
    results = {}
    for i, combination in enumerate(_all_possible):
        perks = parse(all_possible[i])
        s = "" 
        for perk in combination:
            if(isinstance(perk, list)):
                s += "{} ".format(perk[0])
            else:
                s += perk + " "
        results[s] = trap.calculate_damage(perks)

    print("SORTED BY DPS (CALCULATED OVER 100 SHOTS)")

    
    print(*sorted(results.items(), key=lambda x: x[1][1]), sep='\n')
    print("="*100)
    print("SORTED BY SINGLE SHOT DAMAGE")
    print(*sorted(results.items(), key=lambda x: x[1][0]), sep='\n')

main()


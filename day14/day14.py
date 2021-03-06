"""day14.py
"""
import math


class NanoFactory:
    def __init__(self, fname):
        self.rx = {}
        self.bank = {}
        self.get_data(fname)

    def get_data(self, fname):
        with open(fname, 'r') as f:
            for line in f:
                line = line.strip().split('=>')
                reactants = line[0].split(',')
                reactants = tuple((int(x.split()[0]), x.split()[1]) for x in reactants)
                product = line[1].split()
                self.rx[product[1]] = (int(product[0]), reactants)

    def ore_per_product(self, product='FUEL', amount=1):
        banked = self.bank.get(product, 0)
        if banked > 0:
            if amount >= banked:
                # we have some banked, but not enough
                amount, self.bank[product] = amount - banked, 0
            else:
                # we have more than enough banked
                amount, self.bank[product] = 0, banked - amount
                return 0
        parts = {key: val for val, key in self.rx[product][1]}
        count = self.rx[product][0]
        mult = math.ceil(amount / count)
        extra = (count * mult) - amount
        self.bank[product] = self.bank.get(product, 0) + extra
        total = 0
        for reactant, reactant_amount in parts.items():
            total_reactant_needed = reactant_amount * mult
            if reactant == 'ORE':
                total += total_reactant_needed
            else:
                total += self.ore_per_product(reactant, total_reactant_needed)
        return total

    def fuel_with_ore(self, ore):
        check, lower, upper = 1, 1, None
        while (upper is None) or (upper - lower != 1):
            temp_ore = self.ore_per_product(amount=check)
            if temp_ore < ore:
                lower = check
                check = check * 2 if upper is None else lower + ((upper - lower) // 2)
            elif temp_ore > ore:
                upper = check
                check = lower + ((upper - lower) // 2)
            else:
                # Got lucky and hit an exact value
                return check
        return lower

if __name__ == '__main__':
    factory = NanoFactory('data.txt')

    ore = factory.ore_per_product(amount=1)
    print(f'Need {ore:,} ore for 1 fuel.')

    fuel_with_ore = factory.fuel_with_ore(1_000_000_000_000)
    print(f'Can make {fuel_with_ore:,} fuel with 1 trillion ore.')

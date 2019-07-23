class Submarine:
    '''
    Test Documentation
    ทดสอบ Help
    '''
    def __init__(self, price, budget):
        self.captain = 'Prawit'
        self.sub_name = 'BrIGhTZ'
        self.price = price #Million
        self.kilo = 0
        self.totalcost = 0
        self.budget = budget

    def Missile(self):
        print('We are Department of Missle')

    def Calcommission(self):
        pc = 10 # 10%
        percent = self.price * (pc/100)
        print('Yo! You will got : {} Million Baht'.format(percent))
    
    def Goto(self, enemypoint,distance):
        print(f"Let's go to {enemypoint} Distance: {distance} KM")
        self.kilo += distance
        self.Fuel()


    def Fuel(self):
        deisel = 20 # 20 Baht/litre
        cal_fuel_cost = self.kilo * deisel
        print('Current Fuel Cost: {:,.2f} Baht'.format(cal_fuel_cost))
        self.totalcost += cal_fuel_cost

    @property
    def BudgetRemaining(self):
        remaining = self.budget - self.totalcost
        print('Budget Remaining : {:,.2f} Baht'.format(remaining))
        return remaining

class ElectricSubmarine(Submarine):
    def __init__(self, price, budget):
        self.sub_name = 'Prayet'
        self.battery_distance = 10000
        super().__init__(price, budget)
        # self.sub_name = 'Prayet'

    def Battery(self):
        allbattery = 100
        print(self.kilo)
        calculate = (self.kilo / self.battery_distance) *100
        print('CAL : ',calculate)
        print('We have Battery : {} %'.format(allbattery-calculate))
 
    def Fuel(self):
        killowatt = 20 # 20 Baht/KW
        cal_fuel_cost = self.kilo * killowatt
        print('Current Power Cost: {:,.2f} Baht'.format(cal_fuel_cost))
        self.totalcost += cal_fuel_cost

'''
kongtabreuw = Submarine(500)


kongtabreuw.Calcommission()
kongtabreuw.Missile()

kongtabbok = Submarine(5600)
kongtabbok.Calcommission()

kongtabbok.Goto('ชะอำ',5000)

print(kongtabbok.kilo)

kongtabbok.Goto('ระยอง',5000)

print(kongtabbok.kilo)

kongtabreuw.Fuel()
kongtabbok.Fuel()

KTR = kongtabreuw.BudgetRemaining
KTB = kongtabbok.BudgetRemaining

print('งบประมาณของกองทัพเรือ คือ {}'.format(KTR))
print('งบประมาณของกองทัพบก คือ {}'.format(KTB))
'''

if  __name__ == '__main__':

    tesla = ElectricSubmarine(500, 2000000)

    print(tesla.captain)
    print(tesla.budget)
    tesla.Goto('อินเดีย',5000)
    # tesla.Fuel()
    print(tesla.BudgetRemaining)
    # tesla.CalBattery()
    print(tesla.sub_name)
    tesla.Battery()

    print('---------------------------')


    kongtabbok = Submarine(5600, 99999999)
    kongtabbok.Calcommission()

    kongtabbok.Goto('ชะอำ',5000)

    print(kongtabbok.kilo)

    kongtabbok.Goto('ระยอง',5000)

    print(kongtabbok.kilo)

    kongtabbok.Fuel()

    KTB = kongtabbok.BudgetRemaining


    print('งบประมาณของกองทัพบก คือ {}'.format(KTB))


    bright = ElectricSubmarine(1000000,80000000)

    print(bright.sub_name)
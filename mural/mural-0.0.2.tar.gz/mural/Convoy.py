from numpy.random import normal
from threading import Timer
import time,random,math
try:
    from Trader import Trader
    from Commodity import Stock
except:
    from .Trader import Trader
    from .Commodity import Stock

class Convoy(Trader):
    def __init__(self,owner,cost,money=0,quantity=0):
        name="%s's Convoy"%(owner.name)
        self.origin=owner.market
        self.owner=owner
        self.commodity=self.origin.getMainExport()
        
        buy=self.owner.stock[self.commodity].buyPrice
        sell=self.owner.stock[self.commodity].sellPrice
        
        stock=Stock(self.commodity,quantity,buy,sell)
        super(Convoy,self).__init__(name,owner.market,money)
        self.stock[stock.name]=stock
        self.cost=cost
        self.quantity=quantity
        self.speed=self.getSpeed(cost)
        self.destination=None
        
        self.businesses=[]
        print("Convoy created, ",self)
        
    def getSpeed(self,money):
        slowest=.5
        fastest=2
        scale=money/300
        if scale > 1: scale=1
        loc=slowest + (fastest-slowest) * scale
        spread=slowest*(1-scale)
        speed = normal(loc,spread)
        if speed > fastest: return fastest
        if speed < slowest: return slowest
        return speed

    def getTransitTime(self,market):
        return self.market.getDistance(market)/self.speed
    
    def gotoMarket(self,destination,businesses):
        if len(businesses) < 1:
            print("Must have specify which businesses to transact with.")
            return
        self.businesses=businesses
        self.setMarket(destination,self.arrivedRemote)


    #businesses is a tuple array (busisness,quantity)
    def setMarket(self,destination,finished):
        transitTime=self.getTransitTime(destination)
        print("%s going to %s will take %.02f sec."%(self,destination,transitTime))
        self.destination=destination
        self.market=None

        duration=transitTime
        steps=math.ceil(1.5*duration)
        char=str(random.choice(['Þ','.','*','-','Ø','o','#','!','^','|']))
        direction=random.choice(['>','<','^'])
        allSteps=range(steps)
        if random.choice([True,False]):
            allSteps=reversed(allSteps)
        for i in allSteps:
            print(("{:%s%ss}"%(direction,steps)).format(char*(i+1)))
            time.sleep(duration/steps)
        finished()

    def goHome(self):
        self.setMarket(self.origin,self.arrivedHome)
        
    def arrivedRemote(self):
        print(self,"arrived.")
        self.market=self.destination
        self.destination=None
        export=self.market.getMainExport()
        for business,quantity in self.businesses:
            Trader.transact(self,business,business.stock[export].commodity,quantity)
            time.sleep(2)
        self.goHome()
        
    def arrivedHome(self):
        if self.destination is not self.origin:
            raise Exception("Error wrong market")
        self.market=self.destination
        self.destination=None
        self.owner.money += self.money
        self.money=0
        for name,stock in self.stock.items():
            self.owner.stock[name].quantity += stock.quantity
            stock.quantity=0
        print(self.owner.convoys)
        del self.owner.convoys[self.owner.convoys.index(self)]
        print(self.owner.convoys)


from math import sqrt
try:
    from db import marketdb
    from Saveable import Saveable
except Exception as e:
    from mural.db import marketdb
    from mural.Saveable import Saveable
    
_market=marketdb.market
class Market(Saveable):
    def __init__(self,name,position=(0,0),exports=[],_id=None):
        super(Market,self).__init__()
        self._id=_id
        if self._id is None:
            self._id=Saveable.getId(name,_market)
        self.name=name
        self.position=position
        self.exports=exports
        self.businesses=[]
    def getVacancy():
        markets=[(m['name'],len(m['businesses'])) for m in Market.all()]
        markets=sorted(markets, key=lambda a: a[1])
        return Market.load(markets[0][0])
        

    def getMainExport(self):
        return self.exports[0]
    def load(d,deep=True):
        d=Saveable.load(d,_market)
        market=Market(d['name'],d['position'],d['exports'],d['_id'])
        if deep:
            try:
                from Business import Business
            except:
                from mural.Business import Business
            for business in d['businesses']:
                Business.load(business,market)
        return market
    
    def save(self):
        super(Market,self).save(_market)
        for b in self.businesses: b.save()
        

    def data(self):
        if len([e for e in self.exports if issubclass(type(e),str)])>0:
            exports=self.exports
        else:
            exports=[e.name for e in self.exports]            
        return {
            'name': self.name,
            'businesses': [b._id for b in self.businesses],
            'position': self.position,
            'exports': exports,
        }
    def __repr__(self):
        return self.name
    
    def display(self):
        for business in self.businesses:
            business.display()

    def getDistance(self,market):
        x=market.position[0]-self.position[0]
        y=market.position[1]-self.position[1]
        return sqrt(x**2 + y**2)
    
    def addBusiness(self,business):
        self.businesses.append(business)
        
    def all():
        output=[]
        cursor=_market.find({})
        for market in cursor:
            output.append(market)
        return output
    




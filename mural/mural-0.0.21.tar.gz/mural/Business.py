try:
    from Trader import Trader
    from Convoy import Convoy
    from Saveable import Saveable
    from Commodity import Stock
    import Market
    from db import marketdb
except:
    from mural.Trader import Trader
    from mural.Convoy import Convoy
    from mural.Saveable import Saveable
    from mural.Commodity import Stock
    from mural.Market import Market
    from mural.db import marketdb
_business=marketdb.business

class Business(Trader,Saveable):
    def all():
        cursor=_business.find({})
        output=[]
        for b in cursor:
            output.append(b)
        return output
    
    def __init__(self,name,market,money=0):
        super(Business,self).__init__(name,market,money)
        market.addBusiness(self)
        self.convoys=[]
        
    def load(d,market=None):
        d=Saveable.load(d,_business)
        if d is None:
            print("This business does not exist! Check spelling; it is case sensitive!")
            return None
        if market is None:
            market=Market.load(d['market'],deep=False)
        print("Getting %s's stock info..."%d['name'])
        b=Business(d['name'],market,d['money'])
        b.stock={name: Stock.load(s) for name,s in d['stock'].items()}
        return b
    def save(self):
        super(Business,self).save(_business)

    def display(self,commodity=None):
        print("|===== {:^11.10} =====|".format(self.name))
        print("|  Money      ${:<8.2f} |".format(self.money))
        print("|-------  Stock  -------|")
        print("|                       |")
        stocks=self.stock.items()
        if commodity is not None:
            stocks=[(commodity,self.stock[commodity])]
        for name,stock in stocks:
            print("|****   {:^9.6}   ****|".format(name))
            print("| Quantity:    {:<8d} |".format(stock.quantity))
            if stock.buyPrice > 9999:
                print("| Buy Price:  ${:06.2e} |".format(stock.buyPrice))
            else:
                print("| Buy Price:  ${:<8.2f} |".format(stock.buyPrice))
            if stock.sellPrice > 9999:
                print("| Sell Price: ${:06.2e} |".format(stock.sellPrice))
            else:
                print("| Sell Price: ${:<8.2f} |".format(stock.sellPrice))
            print("|                       |")
        print("|=======================|\n")
        
    def data(self):
        data=super(Business,self).data()
        data['convoys']=len(self.convoys)
        data['market']=self.market._id
        return data
    
    def createConvoy(self,cost,money=0,quantity=0):
        export=self.market.getMainExport()
        convoy=Convoy(self,cost,money,quantity)
        self.money-=money+cost
        self.stock[export].quantity-=quantity
        self.convoys.append(convoy)
        return convoy
    


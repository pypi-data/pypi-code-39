try:
    from Commodity import Commodity,Stock
except:
    from mural.Commodity import Commodity,Stock
    
class Trader:
    def __init__(self,name,market,money=0):
        super(Trader,self).__init__()
        self.name=name
        self.market=market
        self.money=money
        stock={c.name: c.getStock() for c in Commodity.all()}
        self.stock=stock

    def data(self):
        return {
            'name': self.name,
            'money': self.money,
            'stock': {stock.name: stock.data() for key,stock in self.stock.items()}
        }
    
    def setMarket(self,market):
        self.market=market
        
    def __repr__(self):
        return "%s (%s)"%(self.name,self.market)

    def setBuyPrice(self,commodity,price):
        if issubclass(type(commodity),Commodity):
            commodity=commodity.name
        self.stock['commodity'].buyPrice=price
        
    def setSellPrice(self,commodity,price):
        if issubclass(type(commodity),Commodity):
            commodity=commodity.name
        self.stock['commodity'].buyPrice=price

    def spend(self,money,supress=False):
        if self.money-money < 0:
            if not supress: print("Cannot transact! Not enough money.")
            return False
        else:
            self.money-=money
            return True

    #Assume a transaction from A to B
    def transact(A,B,commodity,units,buy=None,sell=None,supress=False):
        if units <= 0:
            print("Wrong parameters in transaction.")
            return None
        if not issubclass(Commodity,type(commodity)):
            raise Exception("Old transaction occured! Please update to support commodities.")
        if A.market is None or B.market is None or A.market.name != B.market.name:
            print("Wrong market; no sale.",A,B)
            return None

        stockA=A.stock[commodity.name]
        stockB=B.stock[commodity.name]

        if not supress:
            print("")
            print("|============= Transaction ============|")
            print("| Commodity {:>18.18s} pigment |".format(commodity.name))
            print("| {:20.20} {:>6d} pigments |".format(B.name+"'s Quantity",stockB.quantity))
            print("| Your Quantity {:>13d} pigments |".format(stockA.quantity))
        
        buyPrice=(stockA.buyPrice-stockB.sellPrice)/2 + stockB.sellPrice
        sellPrice=(stockB.buyPrice-stockA.sellPrice)/2 + stockA.sellPrice

        #Check if they are willing and if they have the quantity to sell
        #TODO: TEST: If I want 5 but they only have 4, buy the 4.
        _canBuy=stockA.buyPrice >= stockB.sellPrice
        canBuy=_canBuy and stockB.quantity>0
        _canSell=stockB.buyPrice >= stockA.sellPrice
        canSell=_canSell and stockA.quantity>0
        
        buyEnabled= buy is None or buy is True
        sellEnabled= sell is None or sell is True

        isOnlySell= sell is True and buy is None
        isOnlyBuy = buy is True and sell is None

        purchase=canBuy and buyEnabled and not isOnlySell
        sale=canSell and sellEnabled and not isOnlyBuy
        yesno=lambda a: 'Yes' if a else 'No'
        if not supress:
            purchase_text="Failed"
            sale_text="Failed"
            if purchase: purchase_text="Succeded"
            if sale: sale_text="Succeded"
            print("|                                      |")
            if not isOnlySell:
                print("| - - - - - - - Purchase - - - - - - - |")
                print("| Your            Buy Price  ${:<8.2f} |".format(stockA.buyPrice))
                print("| {:9.9s}      Sell Price  ${:<8.2f} |".format(B.name+"'s",stockB.sellPrice))
                print("| Is Buy Price >= Sell Price?      {:>3s} |".format(yesno(_canBuy)))
                print("| Does {:7.7s} have stock to sell? {:>3s} |".format(B.name,yesno(stockB.quantity>0)))
                print("| Purchase {:>27s} |".format(purchase_text))
                print("|                                      |")
            if not isOnlyBuy:
                print("| - - - - - - - - Sale - - - - - - - - |")
                print("| {:10.10s}       Buy Price ${:<8.2f} |".format(B.name+"'s",stockB.buyPrice))
                print("| Your            Sell Price ${:<8.2f} |".format(stockA.sellPrice))
                print("| Is Buy Price >= Sell Price?      {:>3s} |".format(yesno(_canSell)))
                print("| Do you have stock to sell?       {:>3s} |".format(yesno(stockA.quantity>0)))
                print("| Sale {:>31s} |".format(sale_text))
                print("|                                      |")
            
        if purchase:
            if stockB.quantity-units<0:
                return Trader.transact(A,B,commodity,stockB.quantity,buy,sell,supress=True)
            if A.spend(buyPrice*units,True):
                stockA.quantity+=units
                stockB.quantity-=units
                B.money+=buyPrice*units
                print("| - - - - - - - Conclusion - - - - - - |")
                print("| {:10.10s} recieved ${:<8.2f}        |".format(B.name,buyPrice*units))
                print("| You recieved {:5d} {:<17.17s} |".format(units,commodity.name+' pigments'))
                print("|======================================|")
                return True
            else:
                print("| - - - - - - - Conclusion - - - - - - |")
                print("| Sale failed, because you             |") 
                print("| do   not have enough money.          |")
                print("| You have ${:<8.2f}                   |".format(B.money))
                print("|======================================|")
        elif sale:
            if stockA.quantity-units<0:
                return Trader.transact(A,B,commodity,stockA.quantity,buy,sell,supress=True)
            if B.spend(sellPrice*units,True):
                stockA.quantity-=units
                A.money+=sellPrice*units
                stockB.quantity+=units
                print("| - - - - - - - Conclusion - - - - - - |")
                print("| {:8.8s} recieved {:3d} {:5.5s} pigments |".format(B.name,units,commodity.name))
                print("| You recieved ${:<22.2f} |".format(sellPrice*units))
                print("|======================================|")
                return True
            else:
                print("| - - - - - - - Conclusion - - - - - - |")
                print("| Sale failed, because {:<10.10s}      |".format(B.name)) 
                print("| does not have enough money.          |")
                print("| {:<10.10s} has ${:<8.2f}             |".format(B.name,B.money))
                print("|======================================|")
        else:
            #Failed transaction.
            print("| - - - - - - - Conclusion - - - - - - |")
            print("| No transaction occured.              |")

            if not _canBuy and not isOnlySell:
                print("| Consider raising your buy price.     |")
            if not _canSell and not isOnlyBuy:
                print("| Consider lowering your sell price.   |")
            if not _canBuy or not _canSell:
                print("| Do this with the update command.     |")

            if stockA.quantity == 0 and not isOnlyBuy:
                print("| Make sure that you have pigments to  |")
                print("| sell to your customer.               |")
            if stockB.quantity == 0 and not isOnlySell:
                print("| Your vendor does not have pigments   |")
                print("| To sell.                             |")
            print("|======================================|")
            return False
    
    #self is buying from business
    def buy(self,business,commodity,units):
        return Trader.transact(self,business,commodity,units,buy=True)

    #business is buying from self
    def sell(self,business,commodity,units):
        return Trader.transact(self,business,commodity,units,sell=True)

if __name__=='__main__':
    from Market import Market
    red=Commodity('Red')
    mall=Market('test',exports=[red])
    joe=Trader('joe',mall,money=10)
    joe.stock['Red']=Stock(red,1,10,10)
    ken=Trader('ken',mall,money=10)
    ken.stock['Red']=Stock(red,1,1,1)
    Trader.sell(joe,ken,red,20)

    

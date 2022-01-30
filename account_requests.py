import alpaca_trade_api as alpaca
import config

ALPACA_BASE_URL = config.ALPACA_BASE_URL
ALPACA_KEY_ID = config.API_KEY_ID
ALPACA_SECRET_KEY = config.API_SECRET_KEY

class bot():
    def __init__(self) -> None:
        self.api = alpaca.REST(ALPACA_KEY_ID,ALPACA_SECRET_KEY,ALPACA_BASE_URL)
        self.account = self.api.get_account()
        self.orders = []

    def get_long_value(self):
        
        return float(self.account.long_market_value)

    def get_equity(self):
        return float(self.account.equity)

    def submit_buy(self, symbol, shares):
        self.orders.append(self.api.submit_order(symbol,qty=shares,side='buy',time_in_force='gtc'))

    def submit_sell(self, symbol, shares):
        pass

        # probably only used for demo
    def get_value_sim(self):
        orders = self.get_orders()
        buy = []
        sell = []
        val = 0
        for o in orders:
            if o.side == 'buy':
                buy.append(o)
                val += o.filled_avg_price
            else:
                sell.append(o)
                val -= o.filled_avg_price
        
    
    def get_orders(self):
        return self.api.list_orders(status=all)

if __name__ == '__main__':
    t = bot()
    print(t.get_long_value())
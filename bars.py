from textwrap import indent
from time import timezone
import config,requests,json, csv
from app.models import User
from flask_login import current_user

# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
# What is a bar? (we are requesting bars from API)
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
# - Data struct that holds the open, high, low, and close prices of a stock within  
#   a certain period of time
# - Our requested bars will also hold timestamp, volume, number of trades, and 
#   volume-weighted average price for that period of time
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  
class Bars:
    def __init__(self, portfolio,active) -> None:
        self.symbols = []
        self.qtys = []
        self.active = active
        self.all_r = []
        for k in portfolio:
            self.symbols.append(k)
            self.qtys.append(portfolio[k])
        self.start_date = '2021-03-04'         # Begin date for bar requests 
        self.end_date = '2021-12-10'           # End date for bar requests
        self.timeframe = '1Min'                # Time between bars. From [1Min,5Min, 15Min, 1Hour, 1Day]
        self.bar_limit = '100'                # Number of bars to request. Range: [1,10000] Default: 1,000
        # will cover ~104 days for now
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # Historical Data API request parameters
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    
    #symbols = ['MSFT','AAPL','AMZN']  # Symbol list to make requests
    #all_used_symbols = ['MSFT', 'APPL','AMZN']

    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 

    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # Data handling variables
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    #out = open('out.txt','w')       # File to output requested data
    #fout = open('avgs.csv','w')     # CSV file output
    #writer = csv.writer(fout)       # CSV writer
    #urls = []                       # Holds a url for each symbol in symbols[]
    #all_r = []                      # holds request-response objects 
    #lines = []                      # holds formatted response to be written to file
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 

    def generate_bar_request(self,sy, sd, ed, tf, bl = 1000):
        """Generate formatted URL for API bar request

        Keyword arguments:
        sy -- the symbol to request
        sd -- start date as YYYY-MM-DD
        ed -- end date as YYYY-MM-DD
        tf -- the time frame 
        bl -- limit number of request responses 
        """
        return config.DAT_URL + f'/stocks/{sy}/bars?'\
        + f'start={sd}&end={ed}&limit={bl}&timeframe={tf}'

    def get_response(self):
        # Generate urls for every symbol
        urls = [self.generate_bar_request(self.symbols[i],self.start_date\
            ,self.end_date,self.timeframe,self.bar_limit) for i in range(len(self.symbols))]

        # Make an API request for every url
        self.all_r = [requests.get(urls[i], headers=config.HEADERS) for i in range(len(urls))]

        # Convert Response objects to JSON
        self.all_r = [self.all_r[i].json() for i in range(len(self.all_r))]
        # Result:  all_r[i]             contains dict with keys ['bars','symbol','next_page_token'] and each                                             
        #          all_r[i]["bars"]     contains list of bars objects for the specific symbol
        #          all_r[i]["bars"][j]  contains dict with keys ['t','o','h','l','c','v','n','vw']

        # Generate D,O,H,L,C,V,OI text file for each symbol
        for s in range(len(self.all_r)):
            filename = 'ohlc/{}.txt'.format(self.all_r[s]['symbol'])
            with open(filename,'w') as f:
                f.write('Date,Open,High,Low,Close,Volume,OpenInterest\n')
                for b in range(len(self.all_r[s]['bars'])):
                    cur_bar = self.all_r[s]['bars'][b]
                    l = '{},{},{},{},{},{},{}\n'.format(
                        cur_bar['t'],
                        cur_bar['o'],
                        cur_bar['h'],
                        cur_bar['l'],
                        cur_bar['c'],
                        cur_bar['v'],
                        0
                    )
                    f.write(l)

        with open('account_value.txt','w') as out:
            out.write('Account Value\n')
            sum = 0
            
            for i in range(len(self.all_r[0]["bars"])):
                for j in range(len(self.symbols)):
                    #d = self.all_r[j]["bars"][i]['t'] + ','
                    sum += (self.all_r[j]["bars"][i]['vw'])#*self.qtys[j])
                #out.write(d)
                out.write('%.3f' % sum + '\n')
                sum = 0


#b = Bars()
#b.get_response()

    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # Old file-writing debugging stuff
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 

    # Format API response-objects to look nice
    #lines = [json.dumps(all_r[i],indent=4) for i in range(len(all_r))]
    # Write entire Response objects to file
    #for i in range(len(lines)):
    #    out.write(lines[i])


    # Create List with lists of bar averages per symbol. Indexed same way as all_r
    #all_avgs = []
    #for i in range(len(all_r)):
    #    s_avg = []
    #    for j in range(len(all_r[i]["bars"])):
    #        s_avg.append(all_r[i]["bars"][j]['vw'])
    #    all_avgs.append(s_avg)
    # Result:   all_avgs       contains lists of lists of bar averages. One for each symbol
    #           all_avgs[i]    contains the bar averages for the specified symbol


    # Generate CSV file with averages
    #writer.writerow(symbols)
    #for i in range(len(all_avgs[0])):
    #    row = []
    #    for j in range(len(symbols)):
    #        row.append(all_avgs[j][i])
    #    writer.writerow(row)

    #fout.close()

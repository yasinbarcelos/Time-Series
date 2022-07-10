import yfinance as yf
from pathlib import Path  

def importdata(TS,start, end, interval = "1d",period = None,):

    '''The function takes in a list of tickers, a start date, an end date, an interval, and a period, and
    returns a dataframe of the closing prices of the tickers.
    
    Parameters
    ----------
    TS
        ticker symbol
    start
        The starting date of the time series.
    end
        the end date of the data you want to download.
    interval, optional
        1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
    period
        valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
    
    Returns
    -------
        A dataframe with the closing prices of the stocks in the list.
    
    '''
  
    data = yf.download(  # or pdr.get_data_yahoo(...
            # tickers list or string as well
            tickers = TS,

            # use "period" instead of start/end
            # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
            # (optional, default is '1mo')
            period = period,  
            start = start,
            end=end,          

            # fetch data by interval (including intraday if period < 60 days)
            # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
            # (optional, default is '1d')
            interval = interval,

            # group by ticker (to access via data['SPY'])
            # (optional, default is 'column')
            group_by = 'ticker',

            # adjust all OHLC automatically
            # (optional, default is False)
            auto_adjust = True,

            # download pre/post regular market hours data
            # (optional, default is False)
            prepost = False,

            # use threads for mass downloading? (True/False/Integer)
            # (optional, default is True)
            threads = True,

            # proxy URL scheme use use when downloading?
            # (optional, default is None)
            proxy = None
        )
    return data['Close'] 


def import_indices(index,
            start="2000-01-05",
            end="2021-12-31",
            a=0.1,
            b=0.9):
    indices_importados = []    
    indices_importados_normalizados = []
    for e in index:
        timeseries= importdata(TS=(str("^")+e), start=start,end=end)
        indices_importados.append(timeseries)

        minmaxscaler = MinMax(timeseries,a,b)
        locals()[e]  = minmaxscaler[0]
        indices_importados_normalizados.append(locals()[e])

        # save to file
        filepath = Path(str("Data\Raw") +str("\^")+str(e)+str('.csv'))
        filepath_normalizado = Path(str("data") +str("\normalized\^")+str(e)+str('.csv'))
        filepath.parent.mkdir(parents=True, exist_ok=True)          
        filepath_normalizado.parent.mkdir(parents=True, exist_ok=True)  
        timeseries.to_csv(filepath)          
        pd.DataFrame(locals()[e]).to_csv(filepath_normalizado)  
    return "Done importing"

__all__ = ['register_norgatedata_equities_bundle','register_norgatedata_futures_bundle'] 
from zipline.data.bundles import register
import pandas as pd
from trading_calendars import get_calendar
import norgatedata 
from numpy import empty
from zipline.utils.cli import maybe_show_progress

def normalize_start_end_session(calendar_name,start_session,end_session):
    cal = get_calendar(calendar_name)
    if (not(cal.is_session(start_session))):
        start_session = cal.next_open(start_session).floor(freq='D')
    if (not(cal.is_session(end_session))):
        end_session = cal.previous_close(end_session).floor(freq='D')
    return start_session,end_session

def create_norgatedata_equities_bundle(stock_price_adjustment_setting,watchlists,start_session,end_session):
    def ingest(environ,
               asset_db_writer,
               minute_bar_writer,
               daily_bar_writer,
               adjustment_writer,
               calendar,
               start_session,
               end_session,
               cache,
               show_progress,
               output_dir
               ):
        symbols = determine_symbols(watchlists,start_session)
        dtype = [('start_date', 'datetime64[ns]'),
                  ('end_date', 'datetime64[ns]'),
                  ('auto_close_date', 'datetime64[ns]'),
                  ('symbol', 'object'),
                  ('asset_name', 'object'),
                  ('exchange', 'object'),
                  ('exchange_full', 'object'),
                  ]
        metadata = pd.DataFrame(empty(len(symbols), dtype=dtype))
        sessions = calendar.sessions_in_range(start_session, end_session)    
        daily_bar_writer.write(_pricing_iter_equities(symbols, metadata, 
             sessions, show_progress, stock_price_adjustment_setting, start_session, end_session),
            show_progress=show_progress,
            )
        #metadata['exchange'] = exchange
        asset_db_writer.write(equities=metadata)        

    return ingest

def create_norgatedata_futures_bundle(stock_price_adjustment_setting,watchlists,start_session,end_session):
    print ('Creating Norgate Data bundle with start date ' + start_session.strftime('%Y-%m-%d'))
    def ingest(environ,
               asset_db_writer,
               minute_bar_writer,
               daily_bar_writer,
               adjustment_writer,
               calendar,
               start_session,
               end_session,
               cache,
               show_progress,
               output_dir
               ):
        symbols = determine_symbols(watchlists,start_session)
        dtype = [('start_date', 'datetime64[ns]'),
                  ('end_date', 'datetime64[ns]'),
                  ('auto_close_date', 'datetime64[ns]'),
                  ('symbol', 'object'),
                  ('asset_name', 'object'),
                  ('exchange', 'object'),
                  ('exchange_full', 'object'),
                  ]
        metadata = pd.DataFrame(empty(len(symbols), dtype=dtype))
        sessions = calendar.sessions_in_range(start_session, end_session)    
        daily_bar_writer.write(_pricing_iter_futures(symbols, metadata, 
             sessions, show_progress, stock_price_adjustment_setting, start_session, end_session),
            show_progress=show_progress,
            )
        #metadata['exchange'] = exchange
        asset_db_writer.write(futures=metadata)        
    return ingest
    
def determine_symbols(watchlists,startdate):
    if (len(watchlists) == 0):
        logger.error("No watchlists specified")
        
    symbols = []
    for watchlistname in watchlists:
        print ('Adding symbols from ' + watchlistname)
        symbols.extend(norgatedata.watchlist_symbols(watchlistname))
    symbols = list(set(symbols)) # Remove dupes
    symbols.sort()
    for symbol in reversed(symbols):  # Do in reversed order, because we will be deleting some symbols and this messes up iteration
        lqd = norgatedata.last_quoted_date(symbol);
        if (lqd == "9999-12-31"):
            continue
        lqd = pd.Timestamp(lqd,tz='utc')
        if (lqd < startdate):
            symbols.remove(symbol)    
    return symbols
    
def _pricing_iter_equities(symbols, metadata, sessions, show_progress, stock_price_adjustment_setting, start_session, end_session):
               
    with maybe_show_progress(symbols, show_progress,
                             label='Loading Norgate equities:') as it:
        for sid, symbol in enumerate(it):
            #print ('Grabbing ' + symbol + ' with sid ' + str(sid))
            #sid = norgatedata.assetid(symbol)
            
            #print (symbol)
            
            
            # 1990 is the maximum here - anything before is not defined as a session apparently (!)
            # Padding must be all markte days, otherwise it will bork zipline's expection that there's a bar for every day
            asset_name = norgatedata.security_name(symbol)
            #print (asset_name)
            exchange = norgatedata.exchange_name(symbol)
            exchange_full = norgatedata.exchange_name_full(symbol)
            #ac_date = datetime.strptime(norgatedata.second_last_quoted_date(symbol),'%Y-%m-%d')
            
            #print(df)

            df = norgatedata.price_timeseries(symbol,format='pandas-dataframe-zipline',
                                              start_date=start_session.strftime('%Y-%m-%d'),
                                              end_date=end_session.strftime('%Y-%m-%d'),
                                              
                                              stock_price_adjustment_setting=stock_price_adjustment_setting,
                                              padding_setting=norgatedata.PaddingType.ALLMARKETDAYS,  # Must do this - Zipline can only market day padded data
                                              )
            start_date = df.index[0]
            end_date = df.index[-1]    
            ac_date = end_date + pd.Timedelta(days=1) # The auto_close date is the day after the last trade.  # TOOD: SLQD
            
            # TODO: Modify futures symbols
            
            # align to expected days in the trading calendar
            #valid_dates = [d.date() for d in sessions]
            #df = df.reindex(valid_dates)
            #df.fillna(method='ffill', inplace=True)
            #df = df[start_date:end_date] 
            
            #print (start_date)
            #print (end_date)
            

            metadata.iloc[sid] = start_date, end_date, ac_date, symbol, asset_name, exchange, exchange_full
            #print (metadata.iloc[sid])
            #print (str(sid) + ":" + symbol)
            yield sid, df    

################################################    
    
def _pricing_iter_futures(symbols, metadata, sessions, show_progress, start_session, end_session):
    with maybe_show_progress(symbols, show_progress,
                             label='Loading Norgate futures:') as it:
        for sid, symbol in enumerate(it):
            
            
            #print ('Grabbing ' + symbol + ' with sid ' + str(sid))
            #sid = norgatedata.assetid(symbol)
            
            # 1990 is the maximum here - anything before is not defined as a session apparently (!)
            # Padding must be all markte days, otherwise it will bork zipline's expection that there's a bar for every day
            df = norgatedata.price_timeseries(symbol,format='pandas-dataframe-zipline',start_date='1990-01-01',padding_setting=norgatedata.PaddingType.ALLMARKETDAYS, stock_price_adjustment_setting=StockPriceAdjustmentType.NONE)
            asset_name = norgatedata.security_name(symbol)
            exchange = norgatedata.exchange_name(symbol)
            tick_size = norgatedata.tick_size(symbol)
            notice_date = norgatedata.first_notice_date(symbol)
            expiration_date = norgatedata.last_quoted_date(symbol)
            
            #print(df)
            
            start_date = df.index[0]
            end_date = df.index[-1]
            ac_date = end_date + pd.Timedelta(days=1) # The auto_close date is the day after the last trade.
            
            # TODO: Modify futures symbols
            
            # align to expected days in the trading calendar
            #valid_dates = [d.date() for d in sessions]
            #df = df.reindex(valid_dates)
            #df.fillna(method='ffill', inplace=True)
            #df = df[start_date:end_date] 
            

            metadata.iloc[sid] = start_date, end_date, ac_date, symbol, asset_name, exchange, tick_size, notice_date, expiration_date
            print (metadata.iloc[sid])
            #print (str(sid) + ":" + symbol)
            yield sid, df

def register_norgatedata_equities_bundle(bundlename,stock_price_adjustment_setting,watchlists,start_session,end_session,calendar_name):
    start_session,end_session = normalize_start_end_session(calendar_name,start_session,end_session)
    register(bundlename, 
             create_norgatedata_equities_bundle(stock_price_adjustment_setting,watchlists,start_session,end_session),
             start_session=start_session,
             end_session=end_session,
             calendar_name=calendar_name)

def register_norgatedata_futures_bundle(bundlename,stock_price_adjustment_setting,watchlists,start_session,end_session,calendar_name):
    start_session,end_session = normalize_start_end_session(calendar_name,start_session,end_session)
    register(bundlename, 
             create_norgatedata_futures_bundle(stock_price_adjustment_setting,watchlists,start_session,end_session),
             start_session=start_session,
             end_session=end_session,
             calendar_name=calendar_name)

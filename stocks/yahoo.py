from yql import YQL
from yql import Filter
import datetime
import calendar
import requests

import logging
logger = logging.getLogger('stocks_debug')

JAN = 1
FEB = 2
MAR = 3
ABR = 4
MAY = 5
JUN = 6
JUL = 7
AUG = 8
SEP = 9
OCT = 10
NOV = 11
DEC = 12


class YahooFinanceHistoricalData(object):

    '''
    [results][quotes]{
        u'Volume': u'18979500',
        u'Symbol': u'YHOO',
        u'Adj_Close': u'29.51',
        u'High': u'29.51',
        u'Low': u'28.51',
        u'Date': u'2016-01-29',
        u'Close': u'29.51',
        u'Open': u'29.10'
    }
    '''

    table = 'yahoo.finance.historicaldata'

    def __init__(self, symbol, start_date, end_date):
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date

    def get(self):
        startDate = Filter('startDate', 'eq', self.start_date)
        endDate = Filter('endDate', 'eq', self.end_date)
        symbol = Filter('symbol', 'eq', self.symbol)
        where = symbol + endDate + startDate
        return YQL(self.table).select().where(where).run()


class YahooFinanceQuote(object):

    '''
    [results][quote]{
        u'YearLow': u'26.15',
        u'MarketCapitalization': u'40.74B',
        u'DaysHigh': u'43.76',
        u'symbol': u'YHOO',
        u'DaysLow': u'42.54',
        u'Volume': u'31888521',
        u'StockExchange': u'NMS',
        u'DaysRange': u'42.54 - 43.76',
        u'AverageDailyVolume': u'12189100',
        u'LastTradePriceOnly': u'42.80',
        u'YearHigh': u'44.92',
        u'Symbol': u'YHOO',
        u'Change': u'-1.35',
        u'Name': u'Yahoo! Inc.'
    }
    '''

    table = 'yahoo.finance.quote'

    def __init__(self, symbol):
        self.symbol = symbol

    def get(self):
        f = Filter('symbol', 'eq', self.symbol)
        return YQL(self.table).select().where(f).run()


class YahooFinance(object):

    table = 'yahoo.finance.quote'

    def stock_quote_today(self, symbol, format_='json'):
        return YahooFinanceQuote(symbol).get()

    def stock_quote_ranged(self, symbol, start_date, end_date):
        return YahooFinanceHistoricalData(symbol, start_date, end_date).get()

    def stock_quote_month(self, symbol, year, month, format_='json'):
        last_day = calendar.monthrange(year, month)[1]
        # start_date = '{}-{}-{}'.format(year, month, 1)
        # end_date = '{}-{}-{}'.format(year, month, last_day)
        start_date = datetime.date(year, month, 1).strftime('%Y-%m-%d')
        end_date = datetime.date(year, month, last_day).strftime('%Y-%m-%d')
        return YahooFinanceHistoricalData(symbol, start_date, end_date).get()


class YahooChartApi(object):

    '''
    uri:/instrument/1.0/petr4.sa/chartdata;type=quote;range=1d/csv/ Slightly
    ticker:petr4.sa
    Company-Name:PETROBRAS   PN
    Exchange-Name:SAO
    unit:MIN
    timezone:BRT
    currency:BRL
    gmtoffset:-10800
    previous_close:14.0000
    Timestamp:1474635600,1474660800
    labels:1474635600,1474639200,1474642800,1474646400,1474650000,1474653600,1474657200,1474660800
    values:Timestamp,close,high,low,open,volume
    close:13.5600,13.9700
    high:13.5700,13.9800
    low:13.5400,13.9600
    open:13.5600,13.9800
    volume:300,1290700
    1474635840,13.9700,13.9800,13.9600,13.9800,270300
    '''

    url = 'http://chartapi.finance.yahoo.com/instrument/1.0'
    # /%20Slightly'

    def quote_by_range_raw(self, stock, range_):
        resp = requests.get('{}/{}/chartdata;type=quote;range={}/csv'.format(
            self.url, stock, range_))
        resp = resp.text
        return resp

    def quote_by_range(self, stock, range_):
        resp = self.quote_by_range_raw(stock, range_)
        resp = resp.strip().split('\n')
        ret = {}
        for entry in resp[:16]:
            key, val = entry.split(':')
            ret[key] = val
        ret['quotes'] = []
        for entry in resp[17:]:
            entry = entry.split(',')
            entry[0] = datetime.datetime.utcfromtimestamp(float(entry[0]))\
                .strftime('%Y-%m-%d %H:%M:%S')
            tmp = {}
            for key, val in zip(ret['values'].split(','), entry):
                tmp[key] = val
            ret['quotes'].append(tmp)
        return ret

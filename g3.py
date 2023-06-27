# -*- coding: utf-8 -*-
"""
This is created to watch the market depth of the stock symbol added to the symbol.csv. 
Contact details :
Telegram ID: https://t.me/sureshnandagopal
Gmail ID:   sureshcbe5@gmail.com

Disclaimer: This code is for educational purposes only, so please contact your financial adviser before placing your trade. 
Developer is not responsible for any profit/loss happened due to coding, logical or any type of error.
"""

import pyotp
from kiteext import KiteExt
import time
import pandas as pd
import datetime
import requests
from time import sleep
from tabulate import tabulate
import math
from config import username, password, secret, enctoken

kite = KiteExt()

kite.login_with_credentials(userid=username, password=password, secret=secret)

def isMarketTime() -> bool:
    return datetime.datetime.now().time() >= datetime.time(8, 10) and datetime.datetime.now().time() <= datetime.time (15, 30) and datetime.datetime.now().weekday() <5

def isMarketTime():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    market_start_time = '09:00:00'
    market_end_time = '3:30:00'
    if current_time >= market_start_time and current_time <= market_end_time:
        return True
    else:
        return False

def formatVolume(vol):
    if vol >= 10000000:
        vol_str = str(round(vol/10000000, 2)) + ' Cr'
    else:
        vol_str = str(round(vol/100000, 2)) + ' L'
    return vol_str

# Get quotes for symbols
def getTopGainersAndLosers():
    # read instrument details from CSV
    df = pd.read_csv('symbol.csv')
    instrument_details = df['Symbol'].to_list()
    depth = kite.quote(instrument_details)

    pe_dict = {}
    with open('data.csv', 'r') as file:
        next(file) # skip the header row
        for line in file:
            values = line.strip().split(',')
            pe_dict[values[0]] = {'Stock P/E': values[1], 'No. Eq. Shares': values[2]}
    # Define headers and data list
    headers = ["Symbol","LTP","Percentage","Qty","Volume","OHLC","Stock P/E","No. Eq. Shares"]

    data = []

    # Calculate and append data for each symbol
    for i, row in df.iterrows():
        symbol = row['Symbol']
        pre_close = depth[symbol]['ohlc']['close']
        open_price = depth[symbol]['ohlc']['open']
        high_price = depth[symbol]['ohlc']['high']
        low_price = depth[symbol]['ohlc']['low']
        ltp = depth[symbol]['last_price']
        uc = depth[symbol]['upper_circuit_limit']
        percent_change = ((float(ltp) - float(pre_close)) / float(pre_close)) * 100
        quantity = depth[symbol]['buy_quantity']
        volume = int(quantity)/100000 # converting quantity to lakhs
        ol = ''
        pe_data = pe_dict.get(symbol, {'Stock P/E': 'N/A', 'No. Eq. Shares': 'N/A'})
        stock_pe = pe_data['Stock P/E']
        no_eq_shares = pe_data['No. Eq. Shares']
        if open_price == low_price:
            ol = 'O=L'
        elif open_price == high_price:
            ol = 'O=H'
        if ol == 'O=L':
            data.append({'Symbol': symbol, 'LTP': ltp, 'Percentage': percent_change, 'Qty': quantity, 'Volume': volume, 'OHLC': ol,'Stock P/E': stock_pe, 'No. Eq. Shares': no_eq_shares,'UC': uc, 'Open': open_price, 'High': high_price, 'Low': low_price,'Close': pre_close})
    # Calculate and append data for each symbol

    # Create DataFrame and apply formatting
    df = pd.DataFrame(data)
    df['Percentage'] = df['Percentage'].astype(float) # Convert Percentage column to float
    df = df.sort_values(by=['Percentage', 'LTP', 'Qty'], ascending=[False, False, False])
    df['Percentage'] = df['Percentage'].apply(lambda x: "{:.2f}%".format(x)) # Add Percentage with % symbol


    df = df.head(50)

    # Format Volume column to show 2 decimal places and add 'L' suffix
    df['Volume'] = df['Volume'].apply(lambda x: "{:.2f}L".format(x))

    return df

def getfnoData():
    df = pd.read_csv('fnosymbol.csv')
    instrument_details = df['Symbol'].to_list()
    depth = kite.quote(instrument_details)

    data = []

    for i, row in df.iterrows():
        symbol = row['Symbol']
        pre_close = depth[symbol]['ohlc']['close']
        open_price = depth[symbol]['ohlc']['open']
        high_price = depth[symbol]['ohlc']['high']
        low_price = depth[symbol]['ohlc']['low']
        ltp = depth[symbol]['last_price']
        uc = depth[symbol]['upper_circuit_limit']
        percent_change = ((float(ltp) - float(pre_close)) / float(pre_close)) * 100
        quantity = depth[symbol]['buy_quantity']
        volume = int(quantity)/100000 # converting quantity to lakhs
        ol = ''
        pe_data = row['Stock P/E']
        if open_price == low_price:
            ol = 'O=L'
        elif open_price == high_price:
            ol = 'O=H'
        if ol == 'O=L':
            data.append({'Symbol': symbol, 'LTP': ltp, 'Percentage': percent_change, 'Qty': quantity, 'Volume': volume, 'OHLC': ol,'Stock P/E': pe_data,'UC': uc, 'Open': open_price, 'High': high_price, 'Low': low_price,'Close': pre_close})
    # Calculate and append data for each symbol

    # Create DataFrame and apply formatting
    df1 = pd.DataFrame(data)
    df1['Percentage'] = df1['Percentage'].astype(float) # Convert Percentage column to float
    df1 = df1.sort_values(by=['Percentage', 'LTP', 'Qty'], ascending=[False, False, False])
    df1['Percentage'] = df1['Percentage'].apply(lambda x: "{:.2f}%".format(x)) # Add Percentage with % symbol


    df1 = df1.head(50)

    # Format Volume column to show 2 decimal places and add 'L' suffix
    df1['Volume'] = df1['Volume'].apply(lambda x: "{:.2f}L".format(x))

    return df1


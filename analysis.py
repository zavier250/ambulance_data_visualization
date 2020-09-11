# Author: Zavier
import json
import random

import matplotlib.pyplot as plt
import numpy as np
import requests
import pandas as pd
import calendar
import datetime

from app import *
from sklearn.linear_model import LinearRegression,Ridge,RidgeCV
from sklearn.preprocessing import PolynomialFeatures
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf,plot_pacf

def barchart():
    track_response = db.session.query(earf.EARF_Number,earf.Response_Time).filter(earf.Road_Class=='highway',
                                                                                        earf.Road_Type=='track').all()
    ls = []
    intime_count = 0
    for i in track_response:
        if i.Response_Time<=60:
            if i.Response_Time<=10:
                intime_count+=1
            ls.append(i.Response_Time)
    # plt.hist(x=result_array[0],bins=len(track_response))
    # plt.show()
    print(intime_count)
    plt.bar(range(len(ls)),ls)
    plt.show()

def daily_count_distribution():
    daily_count = db.session.query(daily_case_count.Date,daily_case_count.Count,daily_case_count.Overtime_Count).filter(and_(daily_case_count.Date>'2015-12-31',daily_case_count.Date<'2017-01-01')).all()
    date = []
    ls = []
    over_ls = []
    over_rate = []
    for pair in daily_count:
        date.append(pair.Date)
        ls.append(pair.Count)
        over_ls.append(pair.Overtime_Count)
        over_rate.append((pair.Count - pair.Overtime_Count)/pair.Count)
    # plt.bar(date,ls)
    # plt.bar(date, over_ls)
    # plt.scatter(ls,over_rate)
    plt.bar(date,over_rate)
    plt.show()

def over_rate_regression():
    daily_count = db.session.query(daily_case_count.Date, daily_case_count.Count,
                                   daily_case_count.Overtime_Count).filter(
        and_(daily_case_count.Date > '2015-12-31', daily_case_count.Date < '2017-01-01')).all()

    test_daily_count = db.session.query(daily_case_count.Date, daily_case_count.Count,
                                   daily_case_count.Overtime_Count).filter(
        and_(daily_case_count.Date > '2017-01-01', daily_case_count.Date < '2017-05-31')).all()
    date = []
    ls = []
    over_ls = []
    over_rate = []
    test_ls = []
    test_over_rate = []
    for pair in daily_count:
        date.append([pair.Date])
        ls.append([pair.Count])
        over_ls.append([pair.Overtime_Count])
        over_rate.append([pair.Overtime_Count / pair.Count])

    for pair in test_daily_count:
        test_ls.append([pair.Count])
        test_over_rate.append([pair.Overtime_Count / pair.Count])
    # ls = [ls]
    # over_rate = [over_rate]
    # ls = [[1],[2],[3],[4],[5]]
    # over_rate = [[1],[4],[9],[16],[25]]
    poly = PolynomialFeatures(degree=4)
    X_poly = poly.fit_transform(ls)

    poly.fit(X_poly, over_rate)
    lin2 = LinearRegression()
    lin2.fit(X_poly, over_rate)

    # # Ridge
    # model = RidgeCV(alphas=[0.1, 1.0, 10.0])
    # model.fit(ls,over_rate)

    # # Ridge predict
    # overtime_predicted = model.predict(test_ls)
    # plt.scatter(ls, over_rate, marker='o', color='green', label='Training data')
    # plt.scatter(test_ls, overtime_predicted, marker='*', color='blue', label='Test data')
    # plt.scatter(test_ls, test_over_rate, color = "orange", label = "2017")
    # plt.plot(test_ls, overtime_predicted, c='r')

    print(lin2.predict(poly.fit_transform([[78]])))

    plt.scatter(ls, over_rate, color='blue')

    plt.plot(ls, lin2.predict(poly.fit_transform(ls)), color='red')
    plt.title('Polynomial Regression')

    plt.show()

def arima():
    daily_count = db.session.query(daily_case_count.Date, daily_case_count.Count,
                                   daily_case_count.Overtime_Count).filter(
        and_(daily_case_count.Date > '2015-12-31', daily_case_count.Date < '2017-01-01')).all()
    date = []
    ls = []
    over_ls = []
    over_rate = []
    for pair in daily_count:
        date.append(pair.Date)
        ls.append(pair.Count)
        over_ls.append(pair.Overtime_Count)
        over_rate.append(pair.Overtime_Count / pair.Count)

    df = pd.DataFrame(columns=['Date','Over_rate'])
    for i in range(len(date)):
        df = df.append(
            pd.DataFrame({
                'Date':[date[i]],
                'Over_rate':[over_rate[i]]
            }),ignore_index=True
        )
    df.to_csv('./data/arima-data.csv')
    # print(df)
    # over_rate = df.diff(1)
    # over_rate = over_rate.dropna()
    # print(over_rate)
    # # plt.plot(date,df,color='red')
    # # plt.plot(date,over_rate)
    # # plt.show()
    #
    # # acf = plot_acf(over_rate,lags=20)
    # # plt.title('acf')
    # # plt.show()
    # # q=1
    #
    # # pacf = plot_pacf(over_rate, lags=20)
    # # plt.title('pacf')
    # # plt.show()
    # # p=7
    #
    # model = ARIMA(over_rate,order=(7,1,1),freq=1)
    # result = model.fit()
    #
    # # predict
    # pred = result.predict('2016-12-15','2017-02-01',dynamic=True)
    # print(pred)


# certain_area_filter

def get_ambulance_station():
    station_list = []
    id_set = set()
    count = 0
    Columns = ['Place_id','Name','Business_Status','Lat','Lon']
    df = pd.DataFrame(columns=Columns)
    # location centre
    for i in range(-290,-90,3):
        # print(i)
        lat = float(i/10)
        for j in range(1370,1540,3):
            lon = float(j/10)
            count += 1
            try:
                request_text = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=' + str(lat) + ',' + str(lon) + '&rankby=distance&keyword=ambulance+station&key=AIzaSyDpf-U3kydWGURsa81v2Bo7CGeLqOVguAI'
                print(request_text)
                resources = requests.get(request_text,timeout=60)
            except Exception as e:
                print('----exception----')
                continue
            resources = json.loads(resources.text)
            print(len(resources['results']))
            for item in resources['results']:
                if item['place_id'] not in id_set:
                    station_list.append(item['name'])
                    df = df.append(
                        pd.DataFrame({
                            'Place_id':[item['place_id']],
                            'Name':[item['name']],
                            'Business_Status':[item['business_status']],
                            'Lat':[item["geometry"]['location']['lat']],
                            'Lon': [item["geometry"]['location']['lng']]
                        }),ignore_index=True
                    )
                    id_set.add(item['place_id'])
            while 'next_page_token' in resources:
                print(True)
                try:
                    resources = requests.get('https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken=' + resources['next_page_token'] + '&key=AIzaSyDpf-U3kydWGURsa81v2Bo7CGeLqOVguAI', timeout=60)
                except Exception as e:
                    print('----exception----')
                    continue
                resources = json.loads(resources.text)
                for item in resources['results']:
                    if item['place_id'] not in id_set:
                        station_list.append(item['name'])
                        df = df.append(
                            pd.DataFrame({
                                'Place_id': [item['place_id']],
                                'Name': [item['name']],
                                'Business_Status': [item['business_status']],
                                'Lat': [item["geometry"]['location']['lat']],
                                'Lon': [item["geometry"]['location']['lng']]
                            }), ignore_index=True
                        )
                        id_set.add(item['place_id'])
        print(len(station_list))
    df.to_csv('./data/ambulance_station.csv')
    return station_list

def get_daily_cases(year):
    date = '2015-01-01 00:00:00'
    cal = calendar.Calendar()
    day_filter=set()
    alldaylist = []
    for month in list(range(1, 13)):
        # listday = []
        # 调用calendar类的itermonthdays()方法，返回一个迭代器，含有指定年月的日子
        for day in cal.itermonthdates(year, month):
            # 过滤迭代器中用于填充首尾的0
            if day != 0:
                day = datetime.datetime.strftime(day,"%Y-%m-%d %H:%M:%S")
                if day.startswith(str(year)) and day not in day_filter:
                    # listday.append(day)
                    alldaylist.append(day)
                    day_filter.add(day)
    return alldaylist

def main():
    # r1 = requests.get('https://nominatim.openstreetmap.org/search?format=json&q=' + 'Brisbane Road, Booval, Ipswich, Queensland, 4304, Australia', timeout=60)
    # print(r1)
    # print(type(r1))
    # print(r1.text)
    # r2 = requests.get('https://maps.googleapis.com/maps/api/place/textsearch/json?query=queensland+ambulance+service&key=AIzaSyDpf-U3kydWGURsa81v2Bo7CGeLqOVguAI', timeout=60)
    # print(type(r2))
    # # print(r2.text)
    # r2 = json.loads(r2.text)
    # for i in r2['results']:
    #     print(i['name'])

    # get_ambulance_station()
    # station_ls = get_ambulance_station()
    # print(station_ls)
    # print(len(station_ls))
    # print(len(get_daily_cases(2015)))

    # daily_count_distribution()
    # over_rate_regression()
    arima()

if __name__ == '__main__':
    main()

# AIzaSyDpf-U3kydWGURsa81v2Bo7CGeLqOVguAI


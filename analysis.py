# Author: Zavier
import json
import random

import matplotlib.pyplot as plt
import numpy as np
import requests
# import pandas as pd
import calendar
import datetime

from app import *
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

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
    date = []
    ls = []
    over_ls = []
    over_rate = []
    for pair in daily_count:
        date.append(pair.Date)
        ls.append(pair.Count)
        over_ls.append(pair.Overtime_Count)
        over_rate.append((pair.Count - pair.Overtime_Count) / pair.Count)

    ls = [ls]
    over_rate = [over_rate]
    poly = PolynomialFeatures(degree=4)
    X_poly = poly.fit_transform(ls)

    poly.fit(X_poly, over_rate)
    lin2 = LinearRegression()
    lin2.fit(X_poly, over_rate)

    plt.scatter(ls, over_rate, color='blue')

    plt.plot(ls, lin2.predict(poly.fit_transform(ls)), color='red')
    plt.title('Polynomial Regression')

    plt.show()


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
    over_rate_regression()

if __name__ == '__main__':
    main()

# AIzaSyDpf-U3kydWGURsa81v2Bo7CGeLqOVguAI


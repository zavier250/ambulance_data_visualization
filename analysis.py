# Author: Zavier
import json
import random

import matplotlib.pyplot as plt
import numpy as np
import requests

from app import *

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


    # resources = requests.get('https://maps.googleapis.com/maps/api/place/textsearch/json?query=queensland+ambulance+service&key=AIzaSyDpf-U3kydWGURsa81v2Bo7CGeLqOVguAI', timeout=60)
    # station_list = []
    # resources = json.loads(resources.text)
    # for item in resources['results']:
    #     station_list.append(item['name'])
    # while 'next_page_token' in resources:
    #     print(True)
    #     resources = requests.get('https://maps.googleapis.com/maps/api/place/textsearch/json?pagetoken=' + resources['next_page_token'] + '&key=AIzaSyDpf-U3kydWGURsa81v2Bo7CGeLqOVguAI', timeout=60)
    #     resources = json.loads(resources.text)
    #     for item in resources['results']:
    #         station_list.append(item['name'])
    # return station_list

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
    station_ls = get_ambulance_station()
    print(station_ls)
    print(len(station_ls))

if __name__ == '__main__':
    main()

# AIzaSyDpf-U3kydWGURsa81v2Bo7CGeLqOVguAI


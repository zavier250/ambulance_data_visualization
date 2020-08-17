# Author: Zavier
import pandas as pd
import requests
import json
from numpy import *
import datetime



def max_from_three(a,b,c):
    if len(a)>=len(b):
        if len(a)>=len(c):
            return a
        else:
            return c
    else:
        if len(b)>=len(c):
            return b
        else:
            return c


def load_earf(filename):
    df = pd.read_csv(filename, encoding="UTF-8")
    print(df.shape)
    print(df.head(1))
    columns = ["EARF Number", "EARF Date", "Case Nature Code", "Case Nature", "Dangers", "Street Number",
               "Street Name", "Suburb", "Post Code", "Complete Address", "Road Class", "Road type", "Importance", "Lat", "Lon", "Final Assessment Code",
               "Final Assessment", "Patient Ages",
               "Patient Gender", "Time Received", "Time On Scene", "Response Time", "Response Time Class",
               "Case Comments"]
    df2 = pd.DataFrame(columns=columns)



    for i in range(df.shape[0]):
        r1 = []
        r2 = []
        r3 = []
        Complete_Addr1 = ''
        Complete_Addr2 = ''
        Complete_Addr3 = ''

        r = []
        Complete_Addr = ''

        Road_Class = ''
        Road_Type = ''
        Importance = None

        Lat = 0.0
        Lon = 0.0
        Response_Time = 0
        Response_Time_Class = 'time class'
        print(i)
        # print(type(df['Street Number'][i]))
        # Address format = (Street Number) (Street Name), (Suburb)
        try:
            if str(df['Street Number'][i]) != '0' and str(df['Street Number'][i]) != 'nan':
                Complete_Addr1 = str(df['Street Number'][i]) + ' ' + str(df['Street Name'][i]) + ', ' + str(df['Suburb'][i])
                print("Complete Addr1: " + Complete_Addr1)
                r1 = requests.get('https://nominatim.openstreetmap.org/search?format=json&q=' + Complete_Addr1,timeout=60)
                r1 = json.loads(r1.text)
        except Exception as e:
            r1 = []
            print("----Exception----")
            continue
            # Complete_Addr_rd = str(df['Street Number'][i]) + ' ' + str(df['Street Name'][i]) + ' st, ' + str(
            #     df['Suburb'][i])
            # Complete_Addr_st = str(df['Street Number'][i]) + ' ' + str(df['Street Name'][i]) + ' rd, ' + str(
            #     df['Suburb'][i])
            # Complete_Addr_ave = str(df['Street Number'][i]) + ' ' + str(df['Street Name'][i]) + ' ave, ' + str(
            #     df['Suburb'][i])
            # r1 = requests.get('https://nominatim.openstreetmap.org/search?format=json&q=' + Complete_Addr_rd)
            # r1 = json.loads(r1.text)
            # r2 = requests.get('https://nominatim.openstreetmap.org/search?format=json&q=' + Complete_Addr_st)
            # r2 = json.loads(r2.text)
            # r3 = requests.get('https://nominatim.openstreetmap.org/search?format=json&q=' + Complete_Addr_ave)
            # r3 = json.loads(r3.text)
            # if not (r1 == [] and r2 == [] and r3 == []):
            #     # Take the largest request result
            #     r = max_from_three(r1, r2, r3)
        try:
            if not(str(df['Street Name'][i])=="" or str(df['Street Name'][i])=='nan'):
                Complete_Addr2 = str(df['Street Name'][i]) + ', ' + str(df['Suburb'][i])
                print("Complete Addr2: " + Complete_Addr2)
                r2 = requests.get('https://nominatim.openstreetmap.org/search?format=json&q=' + Complete_Addr2,timeout=60)
                r2 = json.loads(r2.text)
        except Exception as e:
            r2 = []
            print("----Exception----")
            continue
        try:
            if str(df['Street Name'][i]) == str(df['Suburb'][i]):
                Complete_Addr3 = str(df['Street Name'][i])
                print("Complete Addr3: " + Complete_Addr3)
                r3 = requests.get('https://nominatim.openstreetmap.org/search?format=json&q=' + Complete_Addr3,
                                  timeout=60)
                r3 = json.loads(r3.text)
        except Exception as e:
            r3 = []
            print("----Exception----")
            continue

        if not(r1==[] and r2==[] and r3==[]):
            r = max_from_three(r1, r2, r3)
            print(r)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            # print(len(r))
            count = 0
            for location in r:
                if -9.0 >= float(location['lat']) >= -30.0 and 154.0 >= float(location['lon']) >= 137.0:
                    Lat = float(location['lat'])
                    Lon = float(location['lon'])
                    Complete_Addr = str(location['display_name'])
                    Road_Class = str(location['class'])
                    Road_Type = str(location['type'])
                    Importance = location['importance']
                    count += 1
                    if count>0:
                        df2 = df2.append(
                            pd.DataFrame({'EARF Number': [df['EARF Number'][i]], 'EARF Date': [df['EARF Date'][i]],
                                          'Case Nature Code': [df['Case Nature Code'][i]],
                                          'Case Nature': [df['Case Nature'][i]],
                                          'Dangers': [df['Dangers'][i]], 'Street Number': [df['Street Number'][i]],
                                          'Street Name': [df['Street Name'][i]],
                                          'Suburb': [df['Suburb'][i]], 'Post Code': [df['Postcode'][i]],
                                          'Complete Address': [Complete_Addr],
                                          "Road Class": [Road_Class],
                                          "Road type": [Road_Type],
                                          "Importance":[Importance],
                                          'Lat': [Lat],
                                          'Lon': [Lon], 'Final Assessment Code': [df['Final Assessment Code'][i]],
                                          'Final Assessment': [df['Final Assessment'][i]],
                                          'Patient Ages': [df['Patient Age in Years'][i]],
                                          'Patient Gender': [df['Patient Gender'][i]],
                                          'Time Received': [df['Date Received'][i]],
                                          'Time On Scene': [df['Date On Scene'][i]], 'Response Time': [Response_Time],
                                          'Response Time Class': [Response_Time_Class],
                                          'Case Comments': [df['Case Comments'][i]]}), ignore_index=True
                        )
                        break

        # for detail in r:
        #     if -9.0 >= float(detail['lat']) >= -30.0 and 154.0 >= float(detail['lon']) >= 137.0:




    df2.to_csv('./data/earf_cleaned.csv')

RESPONSE_TIME_CLASS=[
    'Less than 7 min',
    '7 min - 10 min',
    '10 min - 20 min',
    '20 min - 30 min',
    '30 min - 60 min',
    'Longer than 60 min'
]
def response_time_calculate(filename):
    df = pd.read_csv(filename, encoding="UTF-8")
    for i in range(df.shape[0]):
    # for i in range(10):
        print("---"+str(i)+"---")
        time1 = df['Time Received'][i]
        time2 = df['Time On Scene'][i]
        if isinstance(time1,str) and isinstance(time2,str):
            dateTime_p1 = datetime.datetime.strptime(time1, '%d/%m/%Y %H:%M:%S')
            dateTime_p2 = datetime.datetime.strptime(time2, '%d/%m/%Y %H:%M:%S')
            print(dateTime_p2-dateTime_p1)
            response_time = dateTime_p2-dateTime_p1
            df['Response Time'][i]=response_time
            if response_time<=datetime.timedelta(minutes=7):
                df['Response Time Class'][i]=RESPONSE_TIME_CLASS[0]
            elif response_time>datetime.timedelta(minutes=7) and response_time<=datetime.timedelta(minutes=10):
                df['Response Time Class'][i]=RESPONSE_TIME_CLASS[1]
            elif response_time > datetime.timedelta(minutes=10) and response_time <= datetime.timedelta(minutes=20):
                df['Response Time Class'][i] = RESPONSE_TIME_CLASS[2]
            elif response_time>datetime.timedelta(minutes=20) and response_time<=datetime.timedelta(minutes=30):
                df['Response Time Class'][i]=RESPONSE_TIME_CLASS[3]
            elif response_time>datetime.timedelta(minutes=30) and response_time<=datetime.timedelta(minutes=60):
                df['Response Time Class'][i]=RESPONSE_TIME_CLASS[4]
            elif response_time>datetime.timedelta(minutes=60):
                df['Response Time Class'][i] = RESPONSE_TIME_CLASS[5]
    df.to_csv('./data/darf_cleaned2.csv')
    print('Cleansing finished')


def load_darf(filename):
    df = pd.read_csv(filename, encoding="UTF-8")
    columns = ["EARF Number", "EARF Date", "Cause of Injury Code", "Cause of Injury", "Dangers", "Street Number",
               "Street Name", "Suburb", "Post Code", "Complete Address", "Road Class", "Road type", "Importance", "Lat",
               "Lon", "Patient Ages",
               "Patient Gender", "Time Received", "Time On Scene", "Response Time", "Response Time Class",
               "Case Comments"]
    df2 = pd.DataFrame(columns=columns)
    for i in range(df.shape[0]):
        r1 = []
        r2 = []
        r3 = []
        Complete_Addr1 = ''
        Complete_Addr2 = ''
        Complete_Addr3 = ''

        r = []
        Complete_Addr = ''

        Road_Class = ''
        Road_Type = ''
        Importance = None

        Lat = 0.0
        Lon = 0.0
        Response_Time = 0
        Response_Time_Class = 'time class'
        print(i)
        # print(type(df['Street Number'][i]))
        # Address format = (Street Number) (Street Name), (Suburb)
        try:
            if str(df['Street Number'][i]) != '0' and str(df['Street Number'][i]) != 'nan':
                Complete_Addr1 = str(df['Street Number'][i]) + ' ' + str(df['Street Name'][i]) + ', ' + str(
                    df['Suburb'][i])
                print("Complete Addr1: " + Complete_Addr1)
                r1 = requests.get('https://nominatim.openstreetmap.org/search?format=json&q=' + Complete_Addr1,
                                  timeout=60)
                r1 = json.loads(r1.text)
        except Exception as e:
            r1 = []
            print("----Exception----")
            continue
            # Complete_Addr_rd = str(df['Street Number'][i]) + ' ' + str(df['Street Name'][i]) + ' st, ' + str(
            #     df['Suburb'][i])
            # Complete_Addr_st = str(df['Street Number'][i]) + ' ' + str(df['Street Name'][i]) + ' rd, ' + str(
            #     df['Suburb'][i])
            # Complete_Addr_ave = str(df['Street Number'][i]) + ' ' + str(df['Street Name'][i]) + ' ave, ' + str(
            #     df['Suburb'][i])
            # r1 = requests.get('https://nominatim.openstreetmap.org/search?format=json&q=' + Complete_Addr_rd)
            # r1 = json.loads(r1.text)
            # r2 = requests.get('https://nominatim.openstreetmap.org/search?format=json&q=' + Complete_Addr_st)
            # r2 = json.loads(r2.text)
            # r3 = requests.get('https://nominatim.openstreetmap.org/search?format=json&q=' + Complete_Addr_ave)
            # r3 = json.loads(r3.text)
            # if not (r1 == [] and r2 == [] and r3 == []):
            #     # Take the largest request result
            #     r = max_from_three(r1, r2, r3)
        try:
            if not (str(df['Street Name'][i]) == "" or str(df['Street Name'][i]) == 'nan'):
                Complete_Addr2 = str(df['Street Name'][i]) + ', ' + str(df['Suburb'][i])
                print("Complete Addr2: " + Complete_Addr2)
                r2 = requests.get('https://nominatim.openstreetmap.org/search?format=json&q=' + Complete_Addr2,
                                  timeout=60)
                r2 = json.loads(r2.text)
        except Exception as e:
            r2 = []
            print("----Exception----")
            continue
        try:
            if str(df['Street Name'][i])==str(df['Suburb'][i]):
                Complete_Addr3_1 = str(df['Street Name'][i])
                print("Complete Addr3_1: " + Complete_Addr3_1)
                Complete_Addr3_2 = str(df['Street Name'][i]) + ' ' + str(df['Street Type'][i]) + ', ' + str(df['Suburb'][i])
                print("Complete Addr3_2: " + Complete_Addr3_2)
                r3_1 = requests.get('https://nominatim.openstreetmap.org/search?format=json&q=' + Complete_Addr3_1,timeout=60)
                r3_2 = requests.get('https://nominatim.openstreetmap.org/search?format=json&q=' + Complete_Addr3_2,timeout=60)
                r3_1 = json.loads(r3_1.text)
                r3_2 = json.loads(r3_2.text)
                if len(r3_1)>=len(r3_2):
                    r3 = r3_1
                else:
                    r3 = r3_2

        except Exception as e:
            r3 = []
            print("----Exception----")
            continue

        if not (r1 == [] and r2 == [] and r3 == []):
            r = max_from_three(r1, r2, r3)
            print(r)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            # print(len(r))
            count = 0
            for location in r:
                if -9.0 >= float(location['lat']) >= -30.0 and 154.0 >= float(location['lon']) >= 137.0:
                    Lat = float(location['lat'])
                    Lon = float(location['lon'])
                    Complete_Addr = str(location['display_name'])
                    Road_Class = str(location['class'])
                    Road_Type = str(location['type'])
                    Importance = location['importance']
                    count += 1
                    if count>0:
                        df2 = df2.append(
                            pd.DataFrame({'EARF Number': [df['EARF Number'][i]], 'EARF Date': [df['EARF Date'][i]],
                                          'Cause of Injury Code': [df['Cause of Injury Code'][i]],
                                          'Cause of Injury': [df['Cause of Injury'][i]],
                                          'Dangers': [df['Danger Type'][i]], 'Street Number': [df['Street Number'][i]],
                                          'Street Name': [df['Street Name'][i]],
                                          'Suburb': [df['Suburb'][i]], 'Post Code': [df['Postcode'][i]],
                                          'Complete Address': [Complete_Addr],
                                          "Road Class": [Road_Class],
                                          "Road type": [Road_Type],
                                          "Importance":[Importance],
                                          'Lat': [Lat],
                                          'Lon': [Lon],
                                          'Patient Ages': [df['Patient Age in Years'][i]],
                                          'Patient Gender': [df['Patient Gender'][i]],
                                          'Time Received': [df['Date Received'][i]],
                                          'Time On Scene': [df['Date On Scene'][i]], 'Response Time': [Response_Time],
                                          'Response Time Class': [Response_Time_Class],
                                          'Case Comments': [df['Narrative'][i]]}), ignore_index=True
                        )
                        break
    df2.to_csv('./data/darf_cleaned.csv')



def main():
    # load_earf("./data/earf.csv")
    response_time_calculate("./data/darf_cleaned.csv")
    # load_darf("./data/darf.csv")


if __name__ == "__main__":
    main()

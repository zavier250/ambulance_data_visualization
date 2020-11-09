# Author: Zavier
import numpy as np
from app import *
from sklearn.cluster import DBSCAN,KMeans
from analysis import *


MinPts_list = [180,80,60,40,20,10,5,4,3,2]

def DB_Scan(MinPts):
    df = pd.read_csv("./data/earf_cleaned_v2_2.csv",encoding='UTF-8')

    coordinate_set = df[["Lat","Lon"]]
    print(coordinate_set.head(5))
    print(coordinate_set.shape)

    dbscan = DBSCAN(eps=0.1,min_samples=MinPts).fit(coordinate_set)
    labels = dbscan.labels_

    for i in range(len(labels)):
        # print(type(coordinate_set["EARF Number"][i]))
        # print(type(labels[i]))
        # print(i)
        db.session.add(
            clustering(EARF_Number=int(df["EARF Number"][i]),
                       Lat=coordinate_set["Lat"][i],
                       Lon=coordinate_set["Lon"][i],
                       Label=int(labels[i])
                       )
        )
    db.session.commit()

    cluster_num = max(labels)

    print("The number of cluster is " + str(cluster_num+1))
    # print(len(labels))

    outliers = 0
    for i in labels:
        if i==-1:
            outliers += 1

    print("The number of outliers is "+str(outliers))

    output = {}
    for i in range(max(labels)+1):
        output[i] = 0
        for j in labels:
            if j==i:
                output[i] += 1

    # print(output)

    over_80_count = 0
    print("The clusters which contain more than 180 points:")
    for i in output.keys():
        if output[i]>=60:
            print("Cluster " + str(i) + " contains" + str(output[i]) + "points.")
            over_80_count += 1

    print("There are " + str(over_80_count) + "clusters contain more than 180 points")
    # print(output)
    print(min(output.values()))
    print(max(output.values()))

    print("-----------------------")

def station_number(number):
    total_case = db.session.query(func.count(clustering.EARF_Number)).scalar()
    label_count = {}
    for i in range(38):
        count = db.session.query(func.count(clustering.EARF_Number)).filter(clustering.Label==i).scalar()
        label_count[i]=round(number * (count/total_case)) + 1

    print(label_count)
    print(sum(label_count.values()))
    return label_count

def k_means(label_count):
    lessthan150 = 0
    for i in range(38):
        print(i)
        k = label_count[i]
        cases = db.session.query(clustering.Lat, clustering.Lon).filter(clustering.Label==i).all()
        case_list = []
        for case in cases:
            case_list.append([case.Lat,case.Lon])
        print(len(case_list))
        print("average:" + str(len(case_list)/k))
        if len(case_list)/k<=150:
            lessthan150 += k
        print("--------")
        case_array = np.array(case_list)
        clf = KMeans(n_clusters=k)
        clf.fit(case_array)

        centroids = clf.cluster_centers_
        labels = clf.labels_


        for i in range(len(centroids)):
            cluster_member = 0
            for j in labels:
                if j==i:
                    cluster_member += 1
            db.session.add(clustering_result_40(Lat=centroids[i][0],
                                             Lon=centroids[i][1],
                                             Count=cluster_member
                                             ))

    db.session.commit()
    print("Number of stations that less than 150 cases assigned:" + str(lessthan150))
    print("Complete")
        # print(centroids)
        # print(labels)

def only_k_means(k):
    cases = db.session.query(earf.Lat,earf.Lon).all()
    case_list = []
    for case in cases:
        case_list.append([case.Lat,case.Lon])
    case_array = np.array(case_list)
    clf = KMeans(n_clusters=k)
    clf.fit(case_array)

    centroids = clf.cluster_centers_
    labels = clf.labels_

    for i in range(len(centroids)):
        cluster_member = 0
        for j in labels:
            if j == i:
                cluster_member += 1
        db.session.add(k_means_result(Lat=centroids[i][0],
                                         Lon=centroids[i][1],
                                         Count=cluster_member
                                         ))
    db.session.commit()
    print("Complete")


def k_means_total_distance(k):
    cases = db.session.query(earf.Lat, earf.Lon).all()
    case_list = []
    for case in cases:
        case_list.append([case.Lat, case.Lon])
    case_array = np.array(case_list)
    clf = KMeans(n_clusters=k)
    clf.fit(case_array)

    centroids = clf.cluster_centers_
    labels = clf.labels_
    total_distance = 0.0

    for i in range(len(cases)):
        case_loc = (cases[i].Lat, cases[i].Lon)
        station_label = labels[i]
        station_loc = (centroids[station_label][0],centroids[station_label][1])
        distance = geo_distance_cal(case_loc,station_loc)
        distance = float(str(distance).split(" ")[0])
        total_distance += distance

    print("The total ambulance dispatching distance of K-means clustering deployment is " + str(total_distance))

def current_total_distance():
    current_station = db.session.query(ambulance_station.Lat,ambulance_station.Lon).all()
    all_cases_loc = db.session.query(earf.Lat,earf.Lon).all()
    total_distance = 0.0

    for case_loc in all_cases_loc:
        distance_list = []
        for station in current_station:
            case_coordinate = (case_loc.Lat, case_loc.Lon)
            station_coordinate = (station.Lat, station.Lon)
            distance = float(str(geo_distance_cal(case_coordinate,station_coordinate)).split(" ")[0])
            distance_list.append(distance)
        total_distance += min(distance_list)
    print("The total ambulance dispatching distance of current station deployment is " + str(total_distance))

def db_scan_total_distance():
    stations = db.session.query(clustering_result.Lat, clustering_result.Lon).all()
    all_cases_loc = db.session.query(earf.Lat, earf.Lon).all()
    total_distance = 0.0

    for case_loc in all_cases_loc:
        print(case_loc.Lat)
        distance_list = []
        for station in stations:
            case_coordinate = (case_loc.Lat, case_loc.Lon)
            station_coordinate = (station.Lat, station.Lon)
            distance = float(str(geo_distance_cal(case_coordinate, station_coordinate)).split(" ")[0])
            distance_list.append(distance)
        total_distance += min(distance_list)
    print("The total ambulance dispatching distance of DB Scan clustering deployment is " + str(total_distance))


def distance_comparison():
    all_cases_loc = db.session.query(earf.EARF_Number,earf.Lat, earf.Lon).all()
    current_station = db.session.query(ambulance_station.Lat, ambulance_station.Lon).all()
    k_means_station = db.session.query(k_means_result.Lat, k_means_result.Lon).all()
    db_180_station = db.session.query(clustering_result_180.Lat, clustering_result_180.Lon).all()
    db_60_station = db.session.query(clustering_result.Lat, clustering_result.Lon).all()
    db_40_station = db.session.query(clustering_result_40.Lat, clustering_result_40.Lon).all()

    for case_loc in all_cases_loc:

        distance_list = []

        case_coordinate = (case_loc.Lat, case_loc.Lon)
        print(case_loc.EARF_Number)
        for station in current_station:
            station_coordinate = (station.Lat, station.Lon)
            distance = float(str(geo_distance_cal(case_coordinate,station_coordinate)).split(" ")[0])
            distance_list.append(distance)
        d_current = min(distance_list)

        k_means_distance_list = []
        for station in k_means_station:
            station_coordinate = (station.Lat, station.Lon)
            distance = float(str(geo_distance_cal(case_coordinate, station_coordinate)).split(" ")[0])
            k_means_distance_list.append(distance)
        d_k_means = min(k_means_distance_list)

        db180_distance_list = []
        for station in db_180_station:
            station_coordinate = (station.Lat, station.Lon)
            distance = float(str(geo_distance_cal(case_coordinate, station_coordinate)).split(" ")[0])
            db180_distance_list.append(distance)
        d_db180 = min(db180_distance_list)

        db60_distance_list = []
        for station in db_60_station:
            station_coordinate = (station.Lat, station.Lon)
            distance = float(str(geo_distance_cal(case_coordinate, station_coordinate)).split(" ")[0])
            db60_distance_list.append(distance)
        d_db60 = min(db60_distance_list)

        db40_distance_list = []
        for station in db_40_station:
            station_coordinate = (station.Lat, station.Lon)
            distance = float(str(geo_distance_cal(case_coordinate, station_coordinate)).split(" ")[0])
            db40_distance_list.append(distance)
        d_db40 = min(db40_distance_list)

        db.session.add(deployment_evaluation(EARF_Number = case_loc.EARF_Number,
                                             Lat = case_loc.Lat,
                                             Lon = case_loc.Lon,
                                             d_current = d_current,
                                             d_k_means = d_k_means,
                                             d_db_180 = d_db180,
                                             d_db_60 = d_db60,
                                             d_db_40 = d_db40
                                             ))

    db.session.commit()
    print("Complete")


def distance_comparison_plot():
    all_distance = deployment_evaluation.query.all()
    timely = 0
    k_means_shorten = 0
    db180_shorten = 0
    db60_shorten = 0
    db40_shorten = 0
    all = float(len(all_distance))
    # print(all)
    for distance in all_distance:
        if distance.d_current > distance.d_k_means:
            # timely += 1
            k_means_shorten += 1
        if distance.d_current > distance.d_db_180:
            db180_shorten += 1
        if distance.d_current > distance.d_db_60:
            db60_shorten += 1
        if distance.d_current > distance.d_db_40:
            db40_shorten += 1
    # size = [timely,all-timely]
    # label = "Timely", "Overtime"
    # plt.pie(size, labels = label, autopct='%1.1f%%')
    # plt.axis("equal")
    # plt.show()

    label = ['K-means','DB_Scan(180)', 'DB_Scan(60)', 'DB_Scan(40)']

    data = [k_means_shorten/all,db180_shorten/all,db60_shorten/all,db40_shorten/all]
    plt.barh(range(len(data)),data,tick_label = label)
    plt.show()




def main():
    # for i in MinPts_list:
    #     print("MinPts: " + str(i))
    #     DB_Scan(i)
    # DB_Scan(40)
    # label_count = station_number(206)
    # k_means(label_count)
    # only_k_means(220)
    # k_means_total_distance(220)
    # current_total_distance()
    # db_scan_total_distance()
    # distance_comparison()
    distance_comparison_plot()

if __name__ == "__main__":
    main()
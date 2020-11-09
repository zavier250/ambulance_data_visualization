# Author: Zavier
from flask import Flask, request, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from sqlalchemy import Table
# from sqlalchemy.ext.compiler import compiles
# from sqlalchemy.sql.expression import Executable, ClauseElement
import datetime
import pandas as pd
from sqlalchemy import func
from analysis import *
from sqlalchemy import and_,or_,tuple_
from sqlalchemy import distinct

RESPONSE_TIME_CLASS = {
    'Less than 7 min':1,
    '7 min - 10 min':2,
    '10 min - 20 min':3,
    '20 min - 30 min':4,
    '30 min - 60 min':5,
    'Longer than 60 min':6
}

RESPONSE_TIME_CLASS_2 = {
    1:'Less than 7 min',
    2:'7 min - 10 min',
    3:'10 min - 20 min',
    4:'20 min - 30 min',
    5:'30 min - 60 min',
    6:'Longer than 60 min'
}


FINAL_ASS_CODE = {

}

CASE_PRIORITY = {
    "Delta":"D",
    "Bravo":"B",
    "Alpha":"A",
    "Omega":"O"
}

app = Flask(__name__)
app.config.from_object('settings')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(64),index = True, unique=True, nullable=False)

    def __repr__(self):
        return f'<{self.name}>'


class earf(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    EARF_Number = db.Column(db.Integer, index=True, unique=False, nullable=False)
    AMPDS_Code = db.Column(db.String(100), index = True, unique = False, nullable = True)
    Protocol = db.Column(db.Integer, index=True, unique=False, nullable=False)
    Priority = db.Column(db.String(100), index = True, unique = False, nullable = True)
    Sub_Category = db.Column(db.String(100), index = True, unique = False, nullable = True)
    EARF_Date = db.Column(db.DateTime, index = True, unique = False, nullable = True)
    Case_Nature_Code = db.Column(db.String(100), index = True, unique = False, nullable = True)
    Case_Nature = db.Column(db.String(300), index = True, unique = False, nullable = True)
    Dangers = db.Column(db.Text, index = False, unique = False, nullable = True)
    Address = db.Column(db.String(500), index = True, unique = False, nullable = True)
    Road_Class = db.Column(db.String(100), index = True, unique = False, nullable = True)
    Road_Type = db.Column(db.String(100), index = True, unique = False, nullable = True)
    Road_Importance = db.Column(db.Float, index = True, unique = False, nullable = True)
    Lat = db.Column(db.Float, index=True, unique=False, nullable=True)
    Lon = db.Column(db.Float, index=True, unique=False, nullable=True)
    Final_Assessment_Code = db.Column(db.String(100),index = True, unique = False, nullable = True)
    Final_Assessment = db.Column(db.String(300),index = True, unique = False, nullable = True)
    Patient_Ages = db.Column(db.Integer, index = True, unique = False, nullable = True)
    # 16
    Patient_Gender = db.Column(db.Integer, index = True, unique = False, nullable = True)
    Time_Received = db.Column(db.DateTime, index = True, unique = False, nullable = True)
    Time_On_Scene = db.Column(db.DateTime, index = True, unique = False, nullable = True)
    Response_Time = db.Column(db.Integer, index = True, unique = False, nullable = True)
    Response_Time_Class = db.Column(db.Integer, index = True, unique = False, nullable = True)
    Case_Comments = db.Column(db.Text(), index = False, unique = False, nullable = True)

class final_ass_count(db.Model):
    Final_Assessment_Code = db.Column(db.String(100), primary_key = True)
    Final_Assessment = db.Column(db.String(300), index=True, unique=False, nullable=True)
    Count = db.Column(db.Integer, index = True, unique = False, nullable = False)

class response_time_count(db.Model):
    Response_Time_Class = Response_Time_Class = db.Column(db.Integer, primary_key = True)
    Count = db.Column(db.Integer, index=True, unique=False, nullable=False)

class overtime_fa_count(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Final_Assessment_Code = db.Column(db.String(100), index=True, unique=False, nullable=True)
    Response_Time_Class = db.Column(db.Integer, index=True, unique=False, nullable=True)
    Count = db.Column(db.Integer, index=True, unique=False, nullable=False)

class ambulance_station(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Location_id = db.Column(db.String(500),index=True, unique=True, nullable=True)
    Station_Name = db.Column(db.String(300),index=True, unique=False, nullable=True)
    Status = db.Column(db.String(100),index=True, unique=False, nullable=True)
    Lat = db.Column(db.Float, index=True, unique=False, nullable=True)
    Lon = db.Column(db.Float, index=True, unique=False, nullable=True)

class daily_case_count(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Date = db.Column(db.DateTime, index = True, unique = False, nullable = True)
    Count = db.Column(db.Integer, index=True, unique=False, nullable=False)
    Overtime_Count = db.Column(db.Integer, index=True, unique=False, nullable=True)

class ampds(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    EARF_Number = db.Column(db.Integer, index=True, unique=False, nullable=False)
    AMPDS_Code = db.Column(db.String(100), index=True, unique=False, nullable=True)
    Protocol = db.Column(db.Integer, index=True, unique=False, nullable=False)
    Priority = db.Column(db.String(100), index=True, unique=False, nullable=True)
    Sub_Category = db.Column(db.String(100), index=True, unique=False, nullable=True)


class clustering(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    EARF_Number = db.Column(db.Integer, index=True, unique=False, nullable=False)
    Lat = db.Column(db.Float, index=True, unique=False, nullable=True)
    Lon = db.Column(db.Float, index=True, unique=False, nullable=True)
    Label = db.Column(db.Integer, index=True, unique=False, nullable=False)

class clustering_result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Lat = db.Column(db.Float, index=True, unique=False, nullable=True)
    Lon = db.Column(db.Float, index=True, unique=False, nullable=True)
    Count = db.Column(db.Integer, index=True, unique=False, nullable=False)

class clustering_result_180(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Lat = db.Column(db.Float, index=True, unique=False, nullable=True)
    Lon = db.Column(db.Float, index=True, unique=False, nullable=True)
    Count = db.Column(db.Integer, index=True, unique=False, nullable=False)

class clustering_result_40(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Lat = db.Column(db.Float, index=True, unique=False, nullable=True)
    Lon = db.Column(db.Float, index=True, unique=False, nullable=True)
    Count = db.Column(db.Integer, index=True, unique=False, nullable=False)

class k_means_result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Lat = db.Column(db.Float, index=True, unique=False, nullable=True)
    Lon = db.Column(db.Float, index=True, unique=False, nullable=True)
    Count = db.Column(db.Integer, index=True, unique=False, nullable=False)

class deployment_evaluation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    EARF_Number = db.Column(db.Integer, index=True, unique=False, nullable=False)
    Lat = db.Column(db.Float, index=True, unique=False, nullable=True)
    Lon = db.Column(db.Float, index=True, unique=False, nullable=True)
    d_current = db.Column(db.Float, index=True, unique=False, nullable=True)
    d_k_means = db.Column(db.Float, index=True, unique=False, nullable=True)
    d_db_180 = db.Column(db.Float, index=True, unique=False, nullable=True)
    d_db_60 = db.Column(db.Float, index=True, unique=False, nullable=True)
    d_db_40 = db.Column(db.Float, index=True, unique=False, nullable=True)

def upload_earf():
    df = pd.read_csv("./data/earf_cleaned_v2_2.csv", encoding="UTF-8", error_bad_lines=False)
    df = df.astype(object).where(pd.notnull(df), None)
    df = df.values.tolist()
    # print(df[1])
    for record in df:
        if record[25]!=None and record[26]!=None and str(record[27]).find('day')==-1:
            # 1 for Male and 2 for Female
            if record[24]=='MALE':
                record[24]=1
            elif record[24]=='FEMALE':
                record[24]=2
            elif record[24]=='INDETERMNT':
                record[24]=3
            rtl = record[27].split(':')
            response_time = int(rtl[0])*60 + int(rtl[1])
            # print(record[3])
            db.session.add(earf(EARF_Number = record[2],
                                    EARF_Date = datetime.datetime.strptime(str(record[3]), '%d/%m/%Y %H:%M:%S'),
                                    AMPDS_Code = record[4],
                                    Protocol = record[5],
                                    Priority = record[6],
                                    Sub_Category = record[7],
                                    Case_Nature_Code = record[8],
                                    Case_Nature = record[9],
                                    Dangers = record[10],
                                    Address = record[15],
                                    Road_Class = record[16],
                                    Road_Type = record[17],
                                    Road_Importance = record[18],
                                    Lat = record[19],
                                    Lon = record[20],
                                    Final_Assessment_Code = record[21],
                                    Final_Assessment = record[22],
                                    Patient_Ages = record[23],
                                    Patient_Gender = record[24],
                                    Time_Received = datetime.datetime.strptime(record[25], '%d/%m/%Y %H:%M:%S'),
                                    Time_On_Scene = datetime.datetime.strptime(record[26], '%d/%m/%Y %H:%M:%S'),
                                    Response_Time = response_time,
                                    Response_Time_Class = RESPONSE_TIME_CLASS[record[28]],
                                    Case_Comments = record[29]
                                    ))
    db.session.commit()
    print('earf uploaded')

def upload_ambulance_station():
    df = pd.read_csv("./data/ambulance_station.csv", encoding="UTF-8")
    df = df.values.tolist()
    for record in df:
        db.session.add(ambulance_station(Location_id=record[1],
                                         Station_Name=record[2],
                                         Status=record[3],
                                         Lat=record[4],
                                         Lon=record[5]
                                         ))
    db.session.commit()
    print('ambulance_station_uploaded.')


def upload_daily_case_count():
    for year in [2015,2016,2017,2018]:
        year_li = get_daily_cases(year)
        print(len(year_li))
        for day in year_li:
            count = db.session.query(func.count(earf.EARF_Number)).filter(earf.EARF_Date==day).scalar()
            overtime_count = db.session.query(func.count(earf.EARF_Number)).filter(and_(earf.EARF_Date==day, earf.Response_Time_Class!=1, earf.EARF_Number!=2)).scalar()
            db.session.add(daily_case_count(Date=day,
                                            Count=count,
                                            Overtime_Count=overtime_count))
    db.session.commit()
    print('daily case count uploaded')


def upload_ampds():
    df = pd.read_csv('./data/earf_ampds.csv', encoding="UTF-8")
    for i in range(df.shape[0]):
        db.session.add(ampds(EARF_Number = int(df['EARF Number'][i]),
                             AMPDS_Code = df['AMPDS Code'][i],
                             Protocol = int(df['Protocol'][i]),
                             Priority = df['Priority'][i],
                             Sub_Category = df['Sub_Category'][i]
                             ))
    db.session.commit()
    print('Ampds uploaded.')

@app.route('/')
def helloworld():
    return 'Hello World'

@app.route('/home',methods=['GET','POST'])
def home():
    # GET
    # name = request.form.get('name')
    # if name:
    #     user = User(name=name)
    #     db.session.add(user)
    #     db.session.commit()
    earf_number = request.form.get("earf_number")
    mpds = request.form.get("mpds")
    earf_date = request.form.get("earf_date")
    print(earf_number)
    print(mpds)
    print(earf_date)
    # users = User.query.order_by(User.name).all()
    # print(type(users))
    # print(users)
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    whole_final2 = final_ass_count.query.all()
    response_count = response_time_count.query.all()
    # response_finalass_count = overtime_fa_count.query.all()
    overtime_fa_count_dir = {}
    top_6_code = db.session.query(final_ass_count.Final_Assessment_Code).limit(6).all()
    # print(top_6_code)
    for i in top_6_code:
        code = i.Final_Assessment_Code
        # print(code)
        dir = {}
        for r_class in [3,4,5,6]:
            count = db.session.query(func.count(earf.EARF_Number)).filter(earf.Final_Assessment_Code==code, earf.Response_Time_Class==r_class).scalar()
            # print(count)
            dir[r_class]=count
        overtime_fa_count_dir[code]=dir
    addr_list = db.session.query(earf.Lat, earf.Lon).filter(earf.Response_Time_Class!=1, earf.Response_Time_Class!=2).all()
    # print(addr_list)

    # road_type = db.session.query()

    # print(type(response_finalass_count))
    # print(whole_final2)
    data_dic = {}
    data_dic['whole_final'] = whole_final2
    data_dic['response_count'] = response_count
    data_dic['response_class'] = RESPONSE_TIME_CLASS_2
    data_dic['top_6_code'] = top_6_code
    data_dic['response_finalass_count'] = overtime_fa_count_dir
    data_dic['addr_list'] = addr_list
    # data_dic['response_finalass_count'] = response_finalass_count

    return render_template('dashboard2.html', data=data_dic)

@app.route('/g-map')
def g_map():
    ambulance_station_loc = ambulance_station.query.all()
    k_means_loc = db.session.query(k_means_result.Lat, k_means_result.Lon).all()
    mix_clustering_loc = db.session.query(clustering_result.Lat,clustering_result.Lon).all()
    # print(len(k_means_loc))
    # case_location = db.session.query(earf.Lat,earf.Lon).all()

    all_case_loc = {}
    response_class_count = {}
    for response_class in RESPONSE_TIME_CLASS_2:
        case_loc = db.session.query(earf.Lat,earf.Lon).filter(earf.Response_Time_Class==response_class).all()
        all_case_loc[response_class] = case_loc
        response_class_count[response_class] = len(case_loc)

    # print(len(all_case_loc[1]))

    outliers = db.session.query(clustering.Lat,clustering.Lon).filter(clustering.Label==-1).all()
    print(len(outliers))
    data_dic={}
    data_dic['ambulance_station']=ambulance_station_loc
    data_dic['k-means-result']=k_means_loc
    data_dic['mix-clustering-result']=mix_clustering_loc
    # data_dic['case_loc'] = case_location
    data_dic['all_case_loc'] = all_case_loc
    data_dic['response_time_class'] = RESPONSE_TIME_CLASS_2
    data_dic['response_class_count'] = response_class_count
    data_dic['outliers'] = outliers
    return render_template('g-map.html',data=data_dic)

@app.route('/cluster-map')
def cluster_map():
    addr_list = db.session.query(earf.Lat, earf.Lon).filter(earf.Response_Time_Class != 1,
                                                            earf.Response_Time_Class != 2).all()
    data_dic={}
    data_dic['addr_list'] = addr_list
    return render_template('cluster-map.html',data=data_dic)

@app.route('/daily-case-map/<date>')
def daily_case_map(date):
    daily_case = db.session.query(earf.Lat,earf.Lon).filter(earf.EARF_Date==(str(date)+' 00:00:00')).all()
    track_case = db.session.query(earf.Lat,earf.Lon).filter(earf.Road_Type=='track').all()
    data_dic = {}
    data_dic['daily_case'] = daily_case
    data_dic['track_case'] = track_case
    return render_template('daily-case-map.html',data=data_dic)

@app.route('/road-type-map/<type>')
def road_type_map(type):
    type_case = db.session.query(earf.Lat, earf.Lon).filter(earf.Road_Type == type).all()
    ambulance_station_loc = ambulance_station.query.all()
    data_dic = {}
    data_dic['type_case'] = type_case
    data_dic['ambulance_station'] = ambulance_station_loc
    return render_template('road-type-map.html', data=data_dic)

@app.route('/priority-analysis', methods=["GET","POST"])
def priority_analysis():
    P_D = db.session.query(func.count(earf.EARF_Number)).filter(earf.Priority == "D").scalar()
    P_B = db.session.query(func.count(earf.EARF_Number)).filter(earf.Priority == "B").scalar()
    P_A = db.session.query(func.count(earf.EARF_Number)).filter(earf.Priority == "A").scalar()
    P_O = db.session.query(func.count(earf.EARF_Number)).filter(earf.Priority == "O").scalar()
    priority_distribution = {"D":P_D,"B":P_B,"A":P_A,"O":P_O}

    priority_definition = []
    priority_definition.append(["Delta","Life threatening other than cardiac or respiratory arrest",12700])
    priority_definition.append(["Bravo","Serious not life threatening – urgent",23849])
    priority_definition.append(["Alpha","Non serious or life threatening",125])
    priority_definition.append(["Omega","Minor illness or injury",394])

    overall_count={}
    for i in RESPONSE_TIME_CLASS_2:
        overall_count[i] = db.session.query(func.count(earf.Response_Time_Class)).filter(earf.Response_Time_Class==i).scalar()

    A_count={}
    for i in RESPONSE_TIME_CLASS_2:
        A_count[i] = db.session.query(func.count(earf.Response_Time_Class)).filter(and_(earf.Response_Time_Class==i,earf.Priority=='A')).scalar()

    B_count = {}
    for i in RESPONSE_TIME_CLASS_2:
        B_count[i] = db.session.query(func.count(earf.Response_Time_Class)).filter(
            and_(earf.Response_Time_Class == i, earf.Priority == 'B')).scalar()

    D_count = {}
    for i in RESPONSE_TIME_CLASS_2:
        D_count[i] = db.session.query(func.count(earf.Response_Time_Class)).filter(
            and_(earf.Response_Time_Class == i, earf.Priority == 'D')).scalar()

    O_count = {}
    for i in RESPONSE_TIME_CLASS_2:
        O_count[i] = db.session.query(func.count(earf.Response_Time_Class)).filter(
            and_(earf.Response_Time_Class == i, earf.Priority == 'O')).scalar()

    data_dic={}
    data_dic['overall_count'] = overall_count
    data_dic['A_count'] = A_count
    data_dic['B_count'] = B_count
    data_dic['D_count'] = D_count
    data_dic['O_count'] = O_count
    data_dic['response_time_class'] = RESPONSE_TIME_CLASS_2
    data_dic['priority_distribution'] = priority_distribution
    data_dic['priority_definition'] = priority_definition

    # current_priority = request.form.get("priority")
    # if current_priority:
    #     # data_dic['current_count'] = A_count
    #     # print(data_dic["current_count"][1])
    #     new_data = {}
    #     new_data["Alpha"] = A_count
    #     json.dumps(new_data)
    return render_template('priority-analysis.html',data=data_dic)

@app.route("/low-priority-geo/<priority>")
def low_priority_geo(priority):
    low_priority_cases = db.session.query(earf.EARF_Number,earf.Lat,earf.Lon,earf.Priority,earf.Time_Received,earf.Response_Time).filter(and_(earf.Priority==priority,or_(earf.Response_Time_Class==1,earf.Response_Time_Class==2))).all()
    case_collection={}
    for case in low_priority_cases:
        case_oc_time = case.Time_Received
        # case_oc_time_str = str(case_oc_time).split(" ")[0]
        case_collection[case.EARF_Number]={}
        case_collection[case.EARF_Number]['self']=case
        case_collection[case.EARF_Number]['hp_cases']={}
        # print(case.Lat)
        # print(type(case_oc_time))
        one_h_bf = case_oc_time + datetime.timedelta(hours=-1)
        close_time_hp_cases = db.session.query(earf.EARF_Number,earf.Lat,earf.Lon,earf.Priority,earf.Time_Received,earf.Response_Time).filter(and_(and_(earf.Time_Received>one_h_bf,earf.Time_Received<case_oc_time),or_(earf.Priority=='B',earf.Priority=='D'))).all()
        for hp_case in close_time_hp_cases:
            case_collection[case.EARF_Number]['hp_cases'][hp_case.EARF_Number] = hp_case
        print(case_collection[case.EARF_Number])

    data_dic = {}
    data_dic['case_collection'] = case_collection
    return render_template('low-priority-geo.html',data=data_dic)

@app.route("/clustering-result")
def clustering_result_():
    clustering_result_2 = db.session.query(clustering_result.Lat,clustering_result.Lon,clustering_result.Count).all()
    data_dic = {}
    data_dic["clustering_result"] = clustering_result_2
    return render_template('clustering_result.html',data=data_dic)


@app.route("/k-means-result")
def kmeans_result_():
    kmeans_result_2 = db.session.query(k_means_result.Lat,k_means_result.Lon,k_means_result.Count).all()
    data_dic = {}
    data_dic["kmeans_result"] = kmeans_result_2
    return render_template('k-means.html',data=data_dic)

if __name__ == '__main__':
    # Data upload
    # upload_earf()
        # upload_ambulance_station()
    # upload_daily_case_count()
    # upload_ampds()

    #App run
    app.run(debug=True)

    # flask db init
    # flask db migrate
    # flask db upgrade

    # Error 48
    # sudo lsof -i:5000
    # kill pid
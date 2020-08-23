# Author: Zavier
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from sqlalchemy import Table
# from sqlalchemy.ext.compiler import compiles
# from sqlalchemy.sql.expression import Executable, ClauseElement
import datetime
import pandas as pd
from sqlalchemy import func

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



def upload_earf():
    df = pd.read_csv("./data/earf_cleaned2.csv", encoding="UTF-8")
    df = df.astype(object).where(pd.notnull(df), None)
    df = df.values.tolist()
    for record in df:
        if record[19]!=None and record[20]!=None and str(record[21]).find('day')==-1:
            # 1 for Male and 2 for Female
            if record[18]=='MALE':
                record[18]=1
            elif record[18]=='FEMALE':
                record[18]=2
            elif record[18]=='INDETERMNT':
                record[18]=3
            rtl = record[21].split(':')
            response_time = int(rtl[0])*60 + int(rtl[1])
            db.session.add(earf(EARF_Number = record[0],
                                    EARF_Date = datetime.datetime.strptime(record[1], '%d/%m/%Y %H:%M'),
                                    Case_Nature_Code = record[2],
                                    Case_Nature = record[3],
                                    Dangers = record[4],
                                    Address = record[9],
                                    Road_Class = record[10],
                                    Road_Type = record[11],
                                    Road_Importance = record[12],
                                    Lat = record[13],
                                    Lon = record[14],
                                    Final_Assessment_Code = record[15],
                                    Final_Assessment = record[16],
                                    Patient_Ages = record[17],
                                    Patient_Gender = record[18],
                                    Time_Received = datetime.datetime.strptime(record[19], '%d/%m/%Y %H:%M'),
                                    Time_On_Scene = datetime.datetime.strptime(record[20], '%d/%m/%Y %H:%M'),
                                    Response_Time = response_time,
                                    Response_Time_Class = RESPONSE_TIME_CLASS[record[22]],
                                    Case_Comments = record[23]
                                    ))
    db.session.commit()
    print('earf uploaded')




@app.route('/')
def helloworld():
    return 'Hello World'

@app.route('/home',methods=['GET','POST'])
def home():
    # GET
    name = request.form.get('name')
    if name:
        user = User(name=name)
        db.session.add(user)
        db.session.commit()

    users = User.query.order_by(User.name).all()
    print(type(users))
    print(users)
    return render_template('index.html',users = users)

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

if __name__ == '__main__':
    # upload_earf()
    app.run(debug=True)

    # flask db init
    # flask db migrate
    # flask db upgrade

    # Error 48
    # sudo lsof -i:5000
    # kill pid
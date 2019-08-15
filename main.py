from flask import Flask, render_template, request, redirect
import os
import datetime
import ibm_db
import json
import urllib
import math

app = Flask(__name__)

port = int(os.getenv("PORT", 5000))

db2cred = {
  "hostname": "dashdb-txn-sbox-yp-dal09-03.services.dal.bluemix.net",
  "password": "7z9pm-zzgm26ftsj",
  "https_url": "https://dashdb-txn-sbox-yp-dal09-03.services.dal.bluemix.net",
  "port": 50000,
  "ssldsn": "DATABASE=BLUDB;HOSTNAME=dashdb-txn-sbox-yp-dal09-03.services.dal.bluemix.net;PORT=50001;PROTOCOL=TCPIP;UID=rzg77856;PWD=7z9pm-zzgm26ftsj;Security=SSL;",
  "host": "dashdb-txn-sbox-yp-dal09-03.services.dal.bluemix.net",
  "jdbcurl": "jdbc:db2://dashdb-txn-sbox-yp-dal09-03.services.dal.bluemix.net:50000/BLUDB",
  "uri": "db2://rzg77856:7z9pm-zzgm26ftsj@dashdb-txn-sbox-yp-dal09-03.services.dal.bluemix.net:50000/BLUDB",
  "db": "BLUDB",
  "dsn": "DATABASE=BLUDB;HOSTNAME=dashdb-txn-sbox-yp-dal09-03.services.dal.bluemix.net;PORT=50000;PROTOCOL=TCPIP;UID=rzg77856;PWD=7z9pm-zzgm26ftsj;",
  "username": "rzg77856",
  "ssljdbcurl": "jdbc:db2://dashdb-txn-sbox-yp-dal09-03.services.dal.bluemix.net:50001/BLUDB:sslConnection=true;"
}
@app.route('/')
def index():
    return render_template('countall.html')


# This function will retrieve all data for specific magnitude  
@app.route('/countall', methods = ['GET','POST'])
def getnames(name=None):
    
    try:
        if request.method == "POST":
            mag = request.form['mag']
            #connect to db
            conn = ibm_db.connect("DATABASE="+db2cred['db']+";HOSTNAME="+db2cred['hostname']+";PORT="+str(db2cred['port'])+";UID="+db2cred['username']+";PWD="+db2cred['password']+";","","")
            if conn:
                print("in if loop")
                sql='select * from RZG77856.ALL_MONTH where "MAG">?'
                prep = ibm_db.prepare(conn,sql)
                ibm_db.bind_param(prep, 1, mag)
                ibm_db.execute(prep)
                rows = []
                
                print("conn 2")
            # fetching the result
                result = ibm_db.fetch_assoc(prep)
                while result != False:
                 
                    rows.append(result.copy())
                    result = ibm_db.fetch_assoc(prep)
            # close database connection
                ibm_db.close(conn)
                print("conn 3")
                return render_template('cresult.html', rows=rows)
            else:
                print("no connection established")
                return render_template('main.html')
    except Exception as e:
        print(e)
        return "<html><body><p>In Exception</p></body></html>"
 
 

#Function for Specified range of magnitudes in given range of days 
@app.route('/getrange', methods = ['GET','POST'])
def getrangeall(name=None):  
    try:
        if request.method == "POST":
            uppermag = request.form['uppermag']
            lowermag = request.form['lowermag']
            startdate = request.form['startdate']
            enddate = request.form['enddate']
            
            #connect to db
            conn = ibm_db.connect("DATABASE="+db2cred['db']+";HOSTNAME="+db2cred['hostname']+";PORT="+str(db2cred['port'])+";UID="+db2cred['username']+";PWD="+db2cred['password']+";","","")
            if conn:
                print("in if loop")
                sql='select * from RZG77856.ALL_MONTH where "MAG" between ? and ? and "DATE" between ? and?'
                prep = ibm_db.prepare(conn,sql)
                ibm_db.bind_param(prep, 1, uppermag)
                ibm_db.bind_param(prep, 2, lowermag)
                ibm_db.bind_param(prep, 3, startdate)
                ibm_db.bind_param(prep, 4, enddate)
                ibm_db.execute(prep)
                rows = []
                
                print("conn 2")
            # fetching the result
                result = ibm_db.fetch_assoc(prep)
                while result != False:
                 
                    rows.append(result.copy())
                    result = ibm_db.fetch_assoc(prep)
            # close database connection
                ibm_db.close(conn)
                print("conn 3")
                return render_template('rangeresult.html', rows=rows)
            else:
                print("no connection established")
                return render_template('main.html')
    except Exception as e:
        print(e)
        return "<html><body><p>In Exception</p></body></html>"


@app.route('/getdistance', methods = ['GET','POST'])
def getdistance(name=None):  
    try:
        if request.method == "POST":
            lati = request.form['lati']
            longi = request.form['longi']
            dis = request.form['dis']
            #connect to db
            conn = ibm_db.connect("DATABASE="+db2cred['db']+";HOSTNAME="+db2cred['hostname']+";PORT="+str(db2cred['port'])+";UID="+db2cred['username']+";PWD="+db2cred['password']+";","","")
            if conn:
                print("in if loop")
                sql=' SELECT * FROM GZR53090.QUIZ '
                prep = ibm_db.prepare(conn,sql)
                #ibm_db.bind_param(prep, 1, lati)
                #ibm_db.bind_param(prep, 2, longi)
                ibm_db.execute(prep)
                rows = []
                r1 = []
                count = 0
                distance = 0
                print("conn 2")
            # fetching the result
                result = ibm_db.fetch_assoc(prep)
                while result != False:  
                    
                    rows.append(result.copy())
                    result = ibm_db.fetch_assoc(prep)    
            # close database connection
                ibm_db.close(conn)
                for row in rows:
                    distance = (float(row['LATITUDE']) - float(lati))**2 + (float(row['LONGITUDE']) - float(longi))**2 
                    d = math.sqrt(distance)*111.2
                    
                    if(d < float(dis)):
                        
                        count = count + 1
                        r1.append(row)
                
                print(count)
                return render_template('distance.html', r1=r1, count = count )
            else:
                print("no connection established")
                return render_template('main.html')
    except Exception as e:
        print(e)
        return "<html><body><p>In Exception</p></body></html>"



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)

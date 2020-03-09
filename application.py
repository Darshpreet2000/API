from tokenize import String
import json
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

application=app = Flask(__name__)
application.config['MYSQL_USER'] = 'admin'
application.config['MYSQL_PASSWORD'] = ''
application.config['MYSQL_HOST'] = 'database-1.csh4odvd9r2v.us-east-2.rds.amazonaws.com'
application.config['MYSQL_DB'] = 'hospital'
application.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(application)

@application.route('/api/',methods = ['GET'])
def get_all_hospital_names():
    cur = mysql.connection.cursor()
    cur.execute("SELECT information_schema.TABLES.TABLE_NAME FROM information_schema.TABLES where table_schema='hospital'")
    results = cur.fetchall()
    return jsonify({'data':results})

@application.route('/api/<string:hospital>',methods = ['GET'])
def get_by_name(hospital):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM `"+hospital+"`")
    results = cur.fetchall()
    return jsonify({hospital:results})

@application.route('/api/search/<string:search>',methods = ['POST'])
def compare(search):
    cur = mysql.connection.cursor()
    text = json.loads(request.data)
    query=" SELECT * , "
    length=len(text)
    start=0
    for i in text:
        start=start+1
        query+="'"+i["name"]+"'"+" as name from "+"`"+i["name"]+"`" +" where "+ "`"+i["name"]+"`"+".description like "+"'"+search+"%'"
        if start!=length:
         query+=" union SELECT * , "
    print(query)
    cur.execute(query)
    results = cur.fetchall()
    return jsonify({'data':results})


if __name__ == '__main__':
    application.run()

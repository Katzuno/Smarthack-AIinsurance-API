import flask
from flask import request, json, jsonify
import urllib.error as AzureError
import urllib.request as applyAzureML
import json
from flaskext.mysql import MySQL
import sqlite3
import pandas
from pandas.io.json import json_normalize
#3HuSM125xtKD
app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['JSON_SORT_KEYS'] = False

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'smarthack'
app.config['MYSQL_DATABASE_PASSWORD'] = 'smarthack'
app.config['MYSQL_DATABASE_DB'] = 'smarthack'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_THREAD_SAFETY'] = 1
mysql.init_app(app)

conn = mysql.connect()
cursor =conn.cursor()

url_insurance = 'https://ussouthcentral.services.azureml.net/workspaces/f5fc16490a664ce8b70642058a1d276e/services/51e6605bfb07422e82d0bdee8c10d63e/execute?api-version=2.0&format=swagger'
api_key_insurance = 'LThPOPcQAlCWJXmotkvY0hgOkX5QjeptrksuVoBrFIMihoolyah4IdC5Si7vhcowFiPR6dogZ2MmOYOtxU33sw==' # Replace this with the API key for the web service
headers_insurance = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key_insurance)}

url_driver = 'https://ussouthcentral.services.azureml.net/workspaces/f5fc16490a664ce8b70642058a1d276e/services/eaf97ce8a0fa4d2aa3e3a77297d81017/execute?api-version=2.0&format=swagger'
api_key_driver = 'skdCk6jeBnlM3CEjPojqbSeXpduedm1pGzOlGZs3dUYahxwgBvAzYUMkKZmB6iXUDq+vdcIRtGYhSoAGhXHVbw==' # Replace this with the API key for the web service
headers_driver = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key_driver)}

url_credit = 'https://ussouthcentral.services.azureml.net/workspaces/f5fc16490a664ce8b70642058a1d276e/services/a652ca1bd4194b648b6caabf7e286fdb/execute?api-version=2.0&format=swagger'
api_key_credit = '//fLz8naTtPxyBXC5PXddPff+P8r8gJV3idWmAGGU5RUWtrcwMevsMjCnnPNWwJO+HUKUGCnHYOMkqgLnIctEg==' # Replace this with the API key for the web service
headers_credit = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key_credit)}


def insert(fields_to_insert = "", table_name = "", value1 = "", value2 = ""):
    str_to_format = "INSERT INTO %s(%s) VALUES ('%s','%s')"
    sql_query = str_to_format % (table_name, fields_to_insert, value1, value2)
    print (sql_query)
    if cursor.execute(sql_query):
        conn.commit()
        return {'Status':'Success'}
    else:
        return ""

def select(fields_selected = "", table_name = "", where_clause = "", limit = ""):
	sql_query = "SELECT " + fields_selected + " FROM " + table_name + " WHERE " + where_clause + " LIMIT " + limit
	if limit == "":
		sql_query = sql_query[:-7]
	if where_clause == "":
		sql_query = sql_query[:-7]
	cursor.execute(sql_query)
	return cursor.fetchall()

def select_assoc(fields_selected = "", table_name = "", where_clause = "", limit = ""):
    sql_query = "SELECT " + fields_selected + " FROM " + table_name + " WHERE " + where_clause
    if where_clause == "":
        sql_query = sql_query[:-7]
    if limit != "":
        sql_query = sql_query + " LIMIT " + limit
    cursor.execute(sql_query)
    data = cursor.fetchall()
    print(data)
    if data != '()':
        return data[0][0]
    else:
        return ""


def selectAsJson(column_names = "*", table_name = "Users", car_id = "1", limit = "1"):
    sql_query = "SELECT %s FROM %s WHERE car_id = %s LIMIT %s" % (column_names, table_name, car_id, limit)
    print (sql_query)
    cursor.execute(sql_query)
    data = cursor.fetchall()
    assoc_data = {}
    assoc_row = {}
    columnNames = []
    for tuplu in cursor.description:
        columnNames.append(tuplu[0])
    rowCount = 0
    for row in data:
        for i in range(len(row)):
            assoc_row[columnNames[i]] = str(row[i])
        assoc_data[rowCount] = assoc_row.copy()
        rowCount = rowCount + 1
 #   print (assoc_data)
    return assoc_data

def selectCarboxDatas(column_names = "*", table_name = "Users", car_id = "1"):
    sql_query = "SELECT %s FROM %s WHERE CarID = %s LIMIT 5000" % (column_names, table_name, car_id)
#    print (sql_query)
    cursor.execute(sql_query)
    data = cursor.fetchall()
    assoc_data = []
    assoc_row = {}
    columnNames = []
    for tuplu in cursor.description:
        columnNames.append(tuplu[0])
    rowCount = 0
    for row in data:
        for i in range(len(row)):
            assoc_row[columnNames[i]] = str(row[i])
        assoc_data.append(assoc_row.copy())
        rowCount = rowCount + 1
 #   print (assoc_data)
    return assoc_data

def selectUsersAsJson(column_names = "*", table_name = "Users"):
    sql_query = "SELECT %s FROM %s" % (column_names, table_name)
    print (sql_query)
    cursor.execute(sql_query)
    data = cursor.fetchall()
    assoc_data = {}
    assoc_row = {}
    columnNames = []
    for tuplu in cursor.description:
        columnNames.append(tuplu[0])
    rowCount = 0
    for row in data:
        for i in range(len(row)):
            assoc_row[columnNames[i]] = str(row[i])
        assoc_data[rowCount] = assoc_row.copy()
        rowCount = rowCount + 1
 #   print (assoc_data)
    return assoc_data

@app.route('/', methods=['GET'])
def showWelcome():
    return flask.Response("Welcome to Credit Cards assesment API ")

@app.route('/api/v1/getCarID', methods=['POST'])
def getCarID():
    id = request.form.get('user_id')
    where_clause = 'id = ' + str(id)
    car_id = select_assoc('car_id', 'Users', where_clause)
    car_id = int(car_id)
    return jsonify({'Car_id':car_id})


@app.route('/api/v1/getUserCarData', methods=['POST'])
def getUserCarData():
    car_id = str(request.form.get('car_id'))
    return jsonify(selectAsJson('*', 'cars_data', car_id, '1'))

@app.route('/api/v1/addUser', methods=['POST'])
def addUser():
    user = request.form.get('user')
    passw = request.form.get('pass')
    where_clause = 'user =\'' + str(user) + '\' AND ' + ' pass = \'' + str(passw) + '\''
    if not select_assoc('id, user, pass', 'Users', where_clause, str(1)):
        if insert('user, pass', 'Users', user, passw) != "":
            return jsonify({'Status':'Success'})
    else:
        return jsonify({'Status':'Error in insert'})

@app.route('/api/v1/login', methods=['POST'])
def loginUser():
    user = request.form.get('user')
    passw = request.form.get('pass')
    where_clause = 'user =\'' + str(user) + '\' AND ' + ' pass = \'' + str(passw) + '\''
    id = select_assoc('id, user, pass', 'Users', where_clause, str(1))
    print(id)
    if id:
        return jsonify({'Status':'Success','User_id':id})
    else:
        return jsonify({'Status':'Username or password could not be found'})

@app.route('/api/v1/getCarboxDatas', methods=['GET'])
def getCarboxDatas():
    car_id = request.args.get('car_id')
    where_clause = 'CarID = ' + str(car_id)
    result = selectCarboxDatas('CarID, CodeID, ViewVal, ViewStr, Timestamp', 'carbox', car_id)
    return jsonify(result)

@app.route('/api/v1/getDriverBehaviour', methods=['POST'])
def predictDrivingBehaviour():
    car_id = request.form.get('car_id')
    car_data = selectCarboxDatas('SpeedVal, RpmVal, AccPressVal, ok', 'carbox', car_id)
    '''
    json_result = request.data
    json_result = json_result.decode('utf8').replace("'", '"')
    print(json_result)
    '''
    # Load the JSON to a Python list & dump it back out as formatted JSON
    
    data = {
            "Inputs": {
                    "input1":
                    [ ],
            },
        "GlobalParameters":  {
        }
    }
    data["Inputs"]["input1"] = car_data
   # return jsonify(data)
    body = str.encode(json.dumps(data))

    req = applyAzureML.Request(url_driver, body, headers_driver)

    try:
        response = applyAzureML.urlopen(req)
        result = response.read()
        json_result = result.decode('utf8').replace("'", '"')
        data = json.loads(json_result)
        data = data['Results']['output1']
           # if key != 'Scored Probabilities':
                #result[key] = float("%.2f" % float(data[key]))
        df = json_normalize(data)
        counter = 0
        sum = 0
        for row in data:
            sum = sum + int(row['Scored Labels'])
            counter = counter + 1
        percentage = sum / counter
        result = {'RawData':data, 'Score_percent': percentage}
        '''
        for key in data:
            if key == 'Scored Labels':
                result['Credit-Received'] = data[key]
            elif key == 'Scored Probabilities':
                result['Probability'] = data[key]
        del data
        '''
#        print(result)
#        s = json.dumps(data, indent=4, sort_keys=True)
        return jsonify(result)
    except AzureError.HTTPError as error:
        status = "The request failed with status code: " + str(error.code)
        error_info = error.info()
        error_msg = error.read().decode("utf8", 'ignore')
        return error_msg



@app.route('/api/v1/getInsurancePrice', methods=['POST'])
def predictInsurance():
    car_id = request.form.get('car_id')
#    data = json.dumps(selectAsJson('*', 'cars_data', car_id))
#    data = json.loads(data)
    data = selectAsJson('*', 'cars_data', car_id)
    car_data = data[0]
#    print(data)
#    return jsonify({'Status':'Good'})
#    print(workclass)

    data = {
            "Inputs": {
                "input1": [],
        },
        "GlobalParameters":  {
        }
    }
    del car_data['car_id']
    data["Inputs"]["input1"].append(car_data)
#    print(data)
#    return jsonify(data)
#    print(type(data["Inputs"]["input1"]))
#    return jsonify({'Status':'Good'})
    body = str.encode(json.dumps(data))

    req = applyAzureML.Request(url_insurance, body, headers_insurance)

    try:
        response = applyAzureML.urlopen(req)
        result = response.read()
        
        json_result = result.decode('utf8').replace("'", '"')
        print(json_result)
        data = json.loads(json_result)
        data = data['Results']['output1'][0]
        result = {}
        
        for key in data:
            if key == 'Scored Labels':
                result['Insurance_price'] = int(float(data[key]) / 100)
        del data
        
#        print(result)
#        s = json.dumps(data, indent=4, sort_keys=True)
        return jsonify(result)
    except AzureError.HTTPError as error:
        status = "The request failed with status code: " + str(error.code)
        error_info = error.info()
        error_msg = error.read().decode("utf8", 'ignore')
        return error_msg

@app.route('/api/v1/getCreditScore', methods=['POST'])
def predict_eligible():
    age = request.form.get('age')
    workclass = request.form.get('workclass')
    education = request.form.get('education')
    married = request.form.get('married')
    relationship = request.form.get('relationship')
    occupation = request.form.get('occupation')
    sex = request.form.get('sex')
    wage = request.form.get('wage')
    loss = request.form.get('loss')
    hours_per_week = request.form.get('hours-per-week')
    country = request.form.get('country')
    total_anual_income = request.form.get('total-anual-income')
    
#    print(workclass)
    data = {
            "Inputs": {
                    "input1":
                    [
                        {
                            'age': age,   
                            'workclass': workclass,   
                            'fnlwgt': "77516",   
                            'education': education,   
                            'education-num': "13",   
                            'marital-status': married,   
                            'occupation': occupation,   
                            'relationship': relationship,   
                            'race': "White",   
                            'sex': sex,   
                            'capital-gain': wage,   
                            'capital-loss': loss,   
                            'hours-per-week': hours_per_week,   
                            'native-country': country,   
                            'income': total_anual_income,   
                            'recived': "0",   
                        }
                    ],
            },
        "GlobalParameters":  {
        }
    }

    body = str.encode(json.dumps(data))

    req = applyAzureML.Request(url_credit, body, headers_credit)

    try:
        response = applyAzureML.urlopen(req)
        result = response.read()
        json_result = result.decode('utf8').replace("'", '"')
        print(json_result)
        # Load the JSON to a Python list & dump it back out as formatted JSON
        data = json.loads(json_result)
        data = data['Results']['output1'][0]
        result = {}
        for key in data:
            if key == 'Scored Labels':
                result['Credit-Received'] = data[key]
            elif key == 'Scored Probabilities':
                result['Probability'] = data[key]
        del data
#        print(result)
#        s = json.dumps(data, indent=4, sort_keys=True)
        return jsonify(result)
    except AzureError.HTTPError as error:
        status = "The request failed with status code: " + str(error.code)
        error_info = error.info()
        error_msg = error.read().decode("utf8", 'ignore')
        return error_msg

app.run("gdcb.ro", 2)

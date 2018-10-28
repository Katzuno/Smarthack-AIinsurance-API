# Smarthack-AIinsurance-API
Api for auto insurance application of BitLords team - Smarthack 2018

DOCUMENTATIE API:
DOCUMENTATIE API:

1)
@app.route('/api/v1/getCarID', methods=['POST'])
	PARAM: user_id
    return jsonify({'Car_id':car_id})

2)
@app.route('/api/v1/getUserCarData', methods=['POST'])
	PARAM: car_id
	return jsonify(selectAsJson('*', 'cars_data', car_id, '1'))
	
3)
@app.route('/api/v1/addUser', methods=['POST'])
		return jsonify({'Status':'Success'})
    else:
        return jsonify({'Status':'Error in insert'})
		
4)
@app.route('/api/v1/login', methods=['POST'])
	PARAMS: user, pass
		return jsonify({'Status':'Success','User_id':id})
    else:
        return jsonify({'Status':'Username or password could not be found'})

5)
@app.route('/api/v1/getCarboxDatas', methods=['GET'])
	PARAM: car_id
	return jsonify(selectCarboxDatas('CarID, CodeID, ViewVal, ViewStr, Timestamp', 'carbox', car_id))

6)
@app.route('/api/v1/getInsurancePrice', methods=['POST'])
	PARAM: car_id
	RETURNEAZA: JSON: 'Insurance_price'

7)
@app.route('/api/v1/getCreditScore', methods=['POST'])
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
	
	RETURNEAZA JSON CU FIELDS: Credit-Received, Probability
	

8)
@app.route('/api/v1/getDriverBehaviour', methods=['POST'])
	PARAM: car_id
	RETURNEAZA: RawData cu parametrii Speed, Rpm, AccelerationPress percent
		

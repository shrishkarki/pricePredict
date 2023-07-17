from flask_cors import CORS, cross_origin
from flask import Flask, render_template, request,jsonify


app=Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
# cors_config={
#     "origins":["http://localhost:3000/*"]
# }
# CORS(app,resources={
#      r"/*":cors_config
# })
# CORS(app)
# cors=CORS(app, resources={
#     r"/*": {"origins":"*"}});
# CORS(app, methods=['GET', 'POST'], headers=['Content-Type'], max_age=3600)

import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
@cross_origin()
def predict():
    Fuel_Type_Diesel=0
    if request.method == 'POST':

        # print(request.get_json())
        # response = {'message': 'Success!'}
        # return jsonify(response), 200 
        data = request.get_json()
        predictedValue = request.get_json()
        
        print(data)
        Year = int(data['Year'])
        Present_Price=float(data['Present_Price'])
        Kms_Driven=int(data['Kms_Driven'])
        Kms_Driven2=np.log(Kms_Driven)
        Owner=int(data['Owner'])
        # Fuel_Type_Petrol=request.form['Fuel_Type_Petrol']
        Fuel_Type_Petrol=data['Fuel_Type_Petrol']
        if(Fuel_Type_Petrol=='Petrol'):
                Fuel_Type_Petrol=1
                Fuel_Type_Diesel=0
        else:
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=1
        Year=2023-Year
        Seller_Type_Individual=data['Seller_Type_Individual']
        if(Seller_Type_Individual=='Individual'):
            Seller_Type_Individual=1
        else:
            Seller_Type_Individual=0	
        Transmission_Mannual=data['Transmission_Mannual']
        if(Transmission_Mannual=='Mannual'):
            Transmission_Mannual=1
        else:
            Transmission_Mannual=0
        print(Present_Price,Kms_Driven2,Owner,Year,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Individual,Transmission_Mannual)
        
        prediction=model.predict([[Present_Price,Kms_Driven2,Owner,Year,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Individual,Transmission_Mannual]])
        print(prediction)
        output=round(prediction[0],2)
        if output<0:
            predictedValue ={'price':0}
            return jsonify(predictedValue)
            return render_template('index.html',prediction_texts="Sorry you cannot sell this car")
        else:
            predictedValue={'price':output}
           
            return jsonify(predictedValue)
            return render_template('index.html',prediction_text="You Can Sell The Car at {}".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True) 
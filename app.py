from flask import Flask, jsonify, render_template, request
import joblib
import os
import numpy as np

app = Flask(__name__)
# hello


@app.route("/")
def index():
    return render_template("home.html")

@app.route('/predict',methods=['POST','GET'])
def result():

    # item_weight= float(request.form['item_weight'])
    # item_fat_content=float(request.form['item_fat_content'])
    item_visibility= float(request.form['item_visibility'])
    item_type= float(request.form['item_type'])
    item_mrp = float(request.form['item_mrp'])
    outlet_establishment_year= float(request.form['outlet_establishment_year'])
    outlet_size= float(request.form['outlet_size'])
    outlet_location_type= float(request.form['outlet_location_type'])
    outlet_type= float(request.form['outlet_type'])

    # X= np.array([[ item_weight,item_fat_content,item_visibility,item_type,item_mrp,
    #               outlet_establishment_year,outlet_size,outlet_location_type,outlet_type ]])
    X= np.array([[item_visibility,item_type,item_mrp,outlet_establishment_year,outlet_size,outlet_location_type,outlet_type ]])

    scaler_path= r'./models/sc.sav'

    sc=joblib.load(scaler_path)

    X_std= sc.transform(X)

    model_path=r'./models/best_xgb_model.sav'

    model= joblib.load(model_path)

    Y_pred=model.predict(X_std)
    
    result= Y_pred
    if(Y_pred<0):
        result=abs(Y_pred)
        

    # return jsonify({'Prediction': float(Y_pred)})
    return render_template('prediction_result.html', prediction=result)

if __name__ == "__main__":
    app.run(debug=True, port=9457)

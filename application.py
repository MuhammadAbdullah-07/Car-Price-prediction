import pickle
from flask import Flask,request,jsonify,render_template
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

application = Flask(__name__)
app= application

### Import models
linreg=pickle.load(open('models/linreg.pkl','rb'))
scaler=pickle.load(open('models/scaler.pkl','rb'))

@app.route("/")
def home():
     return render_template('home.html')


@app.route('/predictionpage',methods=['GET','POST'])
def prediction():
     if request.method=='POST':
          year=float(request.form.get('year'))
          present_price=float(request.form.get('present_price'))
          kms_driven=float(request.form.get('kms_driven'))
          seller_type=float(request.form.get('seller_type'))
          transmission=float(request.form.get('transmission'))
          owner=float(request.form.get('owner'))

          
          data=[[
               year,
               present_price,
               kms_driven,
               seller_type,
               transmission,
               owner
               ]]
          scaled_data=scaler.transform(data)
          prediction=linreg.predict(scaled_data)

          return render_template('prediction.html', result=prediction[0])

     else:
          return render_template('prediction.html')
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
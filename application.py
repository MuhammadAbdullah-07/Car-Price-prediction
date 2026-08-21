from flask import Flask,request,jsonify,render_template
import pandas as pd
import numpy as np
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

application = Flask(__name__)
app= application


@app.route("/")
def home():
     return render_template('index.html')


@app.route('/predict',methods=['GET','POST'])
def prediction():
     if request.method=='GET':
          return render_template('home.html')
     else:
          data=CustomData(
               year=int(request.form.get('year')),
               present_price=float(request.form.get('present_price')),
               kms_driven=int(request.form.get('kms_driven')),
               seller_type=request.form.get('seller_type'),
               transmission=request.form.get('transmission'),
               owner=int(request.form.get('owner')),
               fuel_type=request.form.get('fuel_type'),
               car_age=int(request.form.get('car_age'))
          )

          pred_df= data.get_data_as_dataframe()
          pipeline=PredictPipeline()
          results= pipeline.Predict(pred_df)
          return render_template('home.html', result=round(results[0],2))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
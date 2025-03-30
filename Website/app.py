from flask import Flask, render_template, request
import pandas as pd
import pickle
import numpy as np
import joblib

with open('models/model.pkl', 'rb') as file:
    loaded_model = pickle.load(file)

scaler = joblib.load('scalers/scaler.pkl')

#X = [1.23672422, -0.28621769, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0 ,1 ,1 ,0]
#X = [-1.23672422, 0.19736523, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0 ,0 ,0 ,1]
#X = np.array(X).reshape(1, -1)

app = Flask(__name__) 

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/prever")
def prever():
    #res = loaded_model.predict(X)
    #print("A previsão foi :"+ str(res))
    
    return render_template("previsao.html")


@app.route("/previsao", methods=["POST"])
def previsao():
    
    #Receber os dados do Forms
    data = {
        "tenure": [request.form["tenure"]],
        "MonthlyCharges": [request.form["monthlyCharges"]],


        "Contract_Month-to-month": [1 if request.form["contract"].lower() == "monthly" else 0],
        "Contract_One year": [1 if request.form["contract"].lower() == "one_year" else 0],
        "Contract_Two year": [1 if request.form["contract"].lower() == "two_year" else 0],


        "InternetService_DSL": [1 if request.form["internetService"].lower() == "dsl" else 0],
        "InternetService_Fiber optic": [1 if request.form["internetService"].lower() == "fiber_optic" else 0],
        "InternetService_No": [1 if request.form["internetService"].lower() == "none" else 0],


        "PaymentMethod_Bank transfer (automatic)": [1 if request.form["paymentMethod"].lower() == "credit_card" else 0],
        "PaymentMethod_Credit card (automatic)": [1 if request.form["paymentMethod"].lower() == "bank_transfer" else 0],
        "PaymentMethod_Electronic check": [1 if request.form["paymentMethod"].lower() == "electronic_check" else 0],
        "PaymentMethod_Mailed check": [1 if request.form["paymentMethod"].lower() == "mailed_check" else 0],


        "TechSupport_Yes": [1 if request.form["techSupport"].lower() == "yes" else 0],
        "Dependents_Yes": [1 if request.form["dependents"].lower() == "yes" else 0],
        "OnlineSecurity_Yes": [1 if request.form["onlineSecurity"].lower() == "yes" else 0],
        "PaperlessBilling_Yes": [1 if request.form["paperlessBilling"].lower() == "yes" else 0]
    }
    X = pd.DataFrame(data)

    #Normalização dos atributos numéricos
    columns_to_normalize = ['tenure', 'MonthlyCharges']
    X[columns_to_normalize] = scaler.transform(X[columns_to_normalize])

    #Fazer previsao
    res = loaded_model.predict(X)
    print("A previsão foi :"+ str(res))


    #Mandar os resultados da previsao para o frotend
    res = "Churn" if res == 1 else "Retenção"

    return render_template("previsao_resultado.html", data=res)


@app.route("/contacto")
def contacto():
    return render_template("contacto.html")

@app.route("/sobre")
def sobre():
    return render_template("sobre.html")

if __name__ == "__main__":
    app.run(debug=True)
    #app.run(host="0.0.0.0", port=5000)

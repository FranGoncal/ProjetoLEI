from flask import Flask, render_template, request, send_file, redirect, url_for, flash, jsonify
import pandas as pd
from azure.cosmos import CosmosClient, PartitionKey
import pickle
import numpy as np
import joblib
from io import BytesIO
import dill
import io
import matplotlib.pyplot as plt
import requests
import os
from dotenv import load_dotenv
from uuid import uuid4

loaded_models = {}

with open('models/model.pkl', 'rb') as file:
    loaded_models['xgboost'] = pickle.load(file)

with open('models/DT_model.pkl', 'rb') as file:
    loaded_models['dt'] = pickle.load(file)

with open('models/LR_model.pkl', 'rb') as file:
    loaded_models['lr'] = pickle.load(file)

with open('models/NB_model.pkl', 'rb') as file:
    loaded_models['nb'] = pickle.load(file)

with open('models/RF_model.pkl', 'rb') as file:
    loaded_models['rf'] = pickle.load(file)

with open('models/SVM_model.pkl', 'rb') as file:
    loaded_models['svm'] = pickle.load(file)

with open('explainers/lime_explainer.pkl', 'rb') as f:
    explainer = dill.load(f)

scaler = joblib.load('scalers/scaler.pkl')
#tipo_do_modelo = type(loaded_model).__name__

#X = [1.23672422, -0.28621769, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0 ,1 ,1 ,0]
#X = [-1.23672422, 0.19736523, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0 ,0 ,0 ,1]
#X = np.array(X).reshape(1, -1)

z = 0

app = Flask(__name__) 

load_dotenv()
app.secret_key = os.getenv("SECRET_KEY")
COSMOS_ENDPOINT = "https://accfran.documents.azure.com:443/"
COSMOS_KEY = os.getenv("COSMOS_KEY")
DATABASE_NAME = "databaseFran"
CONTAINER_NAME = "dados"

client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
database = client.create_database_if_not_exists(id=DATABASE_NAME)
container = database.create_container_if_not_exists(
    id=CONTAINER_NAME,
    partition_key=PartitionKey(path="/nome"),
    offer_throughput=400
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/prever")
def prever():
    #res = loaded_model.predict(X)
    #print("A previsão foi :"+ str(res))
    
    return render_template("previsao.html")

@app.route("/prever-csv")
def preverCsv():
    return render_template("previsao_csv.html")

@app.route("/previsao-csv", methods=["POST"])
def previsaoCsv():
    ### Captcha ###
    captcha_response = request.form.get('g-recaptcha-response')
    load_dotenv()
    secret = os.environ.get('RECAPTCHA_SECRET')
    verify_url = 'https://www.google.com/recaptcha/api/siteverify'
    payload = {'secret': secret, 'response': captcha_response}
    r = requests.post(verify_url, data=payload)
    result = r.json()

    if not result.get('success', False):
        flash("Falha na verificação do CAPTCHA. Tente novamente.")
        return redirect(url_for('preverCsv'))
    
    
    if "csvfile" not in request.files:
        return "Ficheiro CSV não enviado", 400

    ficheiro = request.files["csvfile"]
    modelo_escolhido = request.form["modeloEscolhido"].lower()

    # Verifica se o nome do ficheiro está vazio (nenhum ficheiro selecionado)
    if ficheiro.filename == "":
        return "Nenhum ficheiro selecionado", 400


    # Lê o CSV usando pandas
    try:
        df = pd.read_csv(ficheiro)
        print("CSV Recebido:")
        print(df.head())  # Mostra as primeiras linhas do DataFrame no terminal
    except Exception as e:
        print("Erro ao ler CSV:", e)
        return "Erro ao processar o ficheiro CSV", 500
    
    

    #verificar formato do ficheiro
    

    #fazer previsão
    loaded_model=loaded_models[modelo_escolhido]
    X = preprocess_data(df)

    y_pred = loaded_model.predict(X)
    df["churn"] = y_pred

    # Cria buffer para guardar CSV em memória
    output = io.BytesIO()
    df.to_csv(output, index=False)
    output.seek(0)

    # Envia CSV como ficheiro para download
    return send_file(
        output,
        mimetype='text/csv',
        as_attachment=True,
        download_name="resultado_previsao.csv"
    )


def preprocess_data(df):
    return df



@app.route("/previsao", methods=["POST"])
def previsao():
    
    #Receber os dados do Forms
    data = {
        "tenure": [request.form["tenure"]],
        "MonthlyCharges": [request.form["monthlyCharges"]],

        "InternetService_DSL": [1 if request.form["internetService"].lower() == "dsl" else 0],
        "InternetService_Fiber optic": [1 if request.form["internetService"].lower() == "fiber_optic" else 0],
        "InternetService_No": [1 if request.form["internetService"].lower() == "none" else 0],

        "Contract_Month-to-month": [1 if request.form["contract"].lower() == "monthly" else 0],
        "Contract_One year": [1 if request.form["contract"].lower() == "one_year" else 0],
        "Contract_Two year": [1 if request.form["contract"].lower() == "two_year" else 0],

        

        "PaymentMethod_Bank transfer (automatic)": [1 if request.form["paymentMethod"].lower() == "credit_card" else 0],
        "PaymentMethod_Credit card (automatic)": [1 if request.form["paymentMethod"].lower() == "bank_transfer" else 0],
        "PaymentMethod_Electronic check": [1 if request.form["paymentMethod"].lower() == "electronic_check" else 0],
        "PaymentMethod_Mailed check": [1 if request.form["paymentMethod"].lower() == "mailed_check" else 0],
        "Dependents_Yes": [1 if request.form["dependents"].lower() == "yes" else 0],
        "OnlineSecurity_Yes": [1 if request.form["onlineSecurity"].lower() == "yes" else 0],

        "TechSupport_Yes": [1 if request.form["techSupport"].lower() == "yes" else 0],
        "PaperlessBilling_Yes": [1 if request.form["paperlessBilling"].lower() == "yes" else 0]
    }
    X = pd.DataFrame(data)

    #Normalização dos atributos numéricos
    columns_to_normalize = ['tenure', 'MonthlyCharges']
    #columns_to_normalize = ['MonthlyCharges']
    X[columns_to_normalize] = scaler.transform(X[columns_to_normalize])

    modelo_escolhido = request.form["modeloEscolhido"].lower()

    match modelo_escolhido:
        case "xgboost":
            print("Usando XGBoost")
        case "rf":
            print("Usando Random Forest")
        case "nb":
            print("Usando Naïve Bayes")
        case "dt":
            print("Usando Decision Tree")
        case "lr":
            print("Usando Logistic Regression")
        case "svm":
            print("Usando Suport Vector Machine")
        case _:
            print("Modelo desconhecido")

    loaded_model=loaded_models[modelo_escolhido]

    #Fazer previsao
    res = loaded_model.predict(X)
    proba = loaded_model.predict_proba(X)
    probabilidade = round(proba[0][res[0]] * 100, 2)  
    print("A previsão foi :"+ str(res)+ " com probabilidade de -> "+str(proba))


    #Mandar os resultados da previsao para o frotend
    res_label = "Churn" if res == 1 else "Retenção"


    # Generate LIME explanation
    exp = explainer.explain_instance(
        data_row=X.iloc[0].values,
        predict_fn=lambda x: loaded_model.predict_proba(pd.DataFrame(x, columns=X.columns))
    )

    fig = exp.as_pyplot_figure()

    prediction = loaded_model.predict(X)[0]
    plt.suptitle(f"Explicação LIME para a predição: {'Churn' if prediction == 1 else 'No Churn'}")
    fig.tight_layout()
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)


    # Convert the image buffer to a base64 string to embed in HTML
    import base64
    img_str = base64.b64encode(img_buffer.getvalue()).decode('utf-8')

    #global z
    #z=X
    return render_template("previsao_resultado.html", res=res_label, probabilidade=probabilidade, img_data=img_str)

'''
@app.route('/lime_explanation', methods=['POST'])
def lime_explanation():
    #image_path = 'static\icon_web_1.png'
    #return send_file(image_path, mimetype='image/png')
    print("Z =====> "+str(z))


    fig = exp.as_pyplot_figure()
    prediction = loaded_model.predict(z)[0]
    plt.title(f"Explicação LIME para a predição: {'Churn' if prediction == 1 else 'No Churn'}")

    # Salvar a figura em um buffer de bytes
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)

    # Retornar a imagem
    return send_file(img_buffer, mimetype='image/png')
'''

@app.route("/contacto")
def contacto():
    return render_template("contacto.html")

@app.route("/sobre")
def sobre():
    return render_template("sobre.html")


from flask import send_from_directory
@app.route('/service-worker.js')
def service_worker():
    return send_from_directory('.', 'service-worker.js')

@app.route('/manifest.json')
def manifest():
    return send_from_directory('static', 'manifest.json')





@app.route('/submit-data', methods=['POST'])
def submit_data():
    data = request.form
    dados = {
        'id': str(uuid4()),
        'nome': data.get('name'),
        'cc_nif': data.get('ccnif'),
        'dependents': data.get('dependents'),
        'tenure': data.get('tenure'),
        'internetService': data.get('internetService'),
        'onlineSecurity': data.get('onlineSecurity'),
        'techSupport': data.get('techSupport'),
        'contract': data.get('contract'),
        'paperlessBilling': data.get('paperlessBilling'),
        'paymentMethod': data.get('paymentMethod'),
        'monthlyCharges': data.get('monthlyCharges'),
        'churn': data.get('churn')
    }

    try:
        container.create_item(body=dados)
        return jsonify({"mensagem": "dados guardados!"}), 201
    except Exception as e:
        print(e)
        return jsonify({"erro": "Falha ao guardar dados."}), 500

if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host="0.0.0.0", port=5000)

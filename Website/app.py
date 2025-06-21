from flask import Flask, render_template, request, send_file, redirect, url_for, flash, jsonify, session
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
'''
client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
database = client.create_database_if_not_exists(id=DATABASE_NAME)
container = database.create_container_if_not_exists(
    id=CONTAINER_NAME,
    partition_key=PartitionKey(path="/nome"),
    offer_throughput=400
)'''

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
    '''captcha_response = request.form.get('g-recaptcha-response')
    load_dotenv()
    secret = os.environ.get('RECAPTCHA_SECRET')
    verify_url = 'https://www.google.com/recaptcha/api/siteverify'
    payload = {'secret': secret, 'response': captcha_response}
    r = requests.post(verify_url, data=payload)
    result = r.json()

    if not result.get('success', False):
        flash("Falha na verificação do CAPTCHA. Tente novamente.", "error")
        return redirect(url_for('preverCsv'))'''
    
    
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

    try:
        y_pred = loaded_model.predict(X)
    except Exception as e:
        flash("Erro ao processar o ficheiro CSV. Consulte o template disponivel nesta página.", "error")
        return redirect(url_for('preverCsv'))
    
    df["churn"] = y_pred

    # Cria buffer para guardar CSV em memória
    output = io.BytesIO()
    df.to_csv(output, index=False)
    output.seek(0)

    download_id = str(uuid4())
    session[f"csv_{download_id}"] = output.getvalue()

    # Flash e redireciona para página de resultado com o ID
    flash("Previsão feita, o resultado será descarregado automaticamente.", "success")
    return redirect(url_for('resultadoCsv', download_id=download_id))

@app.route("/resultado-csv")
def resultadoCsv():
    return render_template("previsao_csv.html", download_id=request.args.get("download_id"))


@app.route("/download-csv/<download_id>")
def downloadCsv(download_id):
    csv_data = session.get(f"csv_{download_id}")
    if not csv_data:
        return "Arquivo expirado ou inválido", 404

    output = io.BytesIO(csv_data)
    return send_file(
        output,
        mimetype="text/csv",
        as_attachment=True,
        download_name="resultado_previsao.csv"
    )


def preprocess_data(df):
    return df



@app.route("/previsao", methods=["POST"])
def previsao():
    
    try:
        tenure_val = float(request.form["tenure"])
        monthly_val = float(request.form["monthlyCharges"])

        internet_service = request.form["internetService"]
        contract = request.form["contract"]
        payment_method = request.form["paymentMethod"]
        dependents = request.form["dependents"]
        online_security = request.form["onlineSecurity"]
        tech_support = request.form["techSupport"]
        paperless_billing = request.form["paperlessBilling"]
        modelo_escolhido_test = request.form["modeloEscolhido"].lower()

    except KeyError as e:
        return f"Campo '{e.args[0]}' é obrigatório", 400
    except ValueError:
        return "Valores inválidos para tenure ou monthlyCharges", 400

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
    #Validar se modelo existe
    if modelo_escolhido not in list(loaded_models.keys()):
        return f"Modelo desconhecido: {modelo_escolhido}", 400    
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


@app.route("/contacto")
def contacto():
    return render_template("contacto.html")

@app.route("/sobre")
def sobre():
    return render_template("sobre.html")

@app.route("/contribuir")
def contribuir():
    return render_template("contribuir.html")

from flask import send_from_directory
@app.route('/service-worker.js')
def service_worker():
    return send_from_directory('.', 'service-worker.js')

@app.route('/manifest.json')
def manifest():
    return send_from_directory('static', 'manifest.json')




@app.route('/submit-data', methods=['POST'])
def submit_data():
    ### Captcha ###
    captcha_response = request.form.get('g-recaptcha-response')
    load_dotenv()
    secret = os.environ.get('RECAPTCHA_SECRET')
    verify_url = 'https://www.google.com/recaptcha/api/siteverify'
    payload = {'secret': secret, 'response': captcha_response}
    r = requests.post(verify_url, data=payload)
    result = r.json()

    if not result.get('success', False):
        flash("Falha na verificação do CAPTCHA. Tente novamente.", "error")
        return redirect(url_for('contribuir'))

    ### CosmosBD ###
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
        flash("Informação Submetida. Obrigado pela sua contribuição!", "success")
        return redirect(url_for('contribuir'))
    except Exception as e:
        print(e)
        return jsonify({"erro": "Falha ao guardar dados."}), 500

if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host="0.0.0.0", port=5000)

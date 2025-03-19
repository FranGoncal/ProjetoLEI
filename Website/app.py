from flask import Flask, render_template
import pickle
import numpy as np

with open('models/model.pkl', 'rb') as file:
    loaded_model = pickle.load(file)

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

@app.route("/contacto")
def contacto():
    return render_template("contacto.html")

@app.route("/sobre")
def sobre():
    return render_template("sobre.html")

if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host="0.0.0.0", port=5000)

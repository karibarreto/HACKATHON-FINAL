from flask import Flask, render_template, Request
import json

app = Flask(__name__)

@app.route('/inicio')
def index ():
    return render_template('inicio_b.html')

@app.route("/registro")
def registro():
    return render_template("registro.html")

@app.route("/escuelas")
def escuelas():
    return render_template("escuelas.html")

if __name__ =="__main__":
    app.run(debug = True)
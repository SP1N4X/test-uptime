from flask import Flask, request
import cal_result

app = Flask('')


@app.route('/')

def index():
    return "<h1>Welcome to our server !!</h1>"


@app.route('/post', methods=['POST'])

def result():
    ale = request.get_json()
    risultato = cal_result.cal(ale)
    return risultato

from flask import Flask
import os

app = Flask(__name__)

port = int(os.getenv("PORT", 4999))

@app.route('/')
def hello_world():
    return '<h1>Hello, Flask on Predix!</h1>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)  #alt, when running locally use host=127.0.0.1

from flask import Flask

app = Flask(__name__)

@app.route('/route_name')
def method_name():
    pass
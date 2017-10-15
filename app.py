from flask import Flask, request
from flask_restful import Resource, Api
import customer_predict;


app = Flask(__name__)
api = Api(app)


@app.route('/')
def index():
	return "Hello"


@app.route('/predict/<string:customer_id>', methods=['GET'])
def predict(customer_id):
	return customer_predict.get_customer_return_status(customer_id)
	

if __name__ == '__main__':
     app.run(port='3004')
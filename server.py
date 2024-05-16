import os
from flask import Flask, request, jsonify
from prometheus_client import Counter, start_http_server
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

insert_counter = Counter('insert_operations_total', 'Total insert operations')
delete_counter = Counter('delete_operations_total', 'Total delete operations')
update_counter = Counter('update_operations_total', 'Total update operations')
get_counter = Counter('get_operations_total', 'Total get operations')


mongo_host = os.environ.get('MONGO_HOST', 'localhost')
mongo_port = int(os.environ.get('MONGO_PORT', '27017'))
mongo_user = os.environ.get('MONGO_USER')
mongo_password = os.environ.get('MONGO_PASSWORD')
mongo_database = os.environ.get('MONGO_DATABASE', 'test')

mongo_client = MongoClient(mongo_host, mongo_port, username=mongo_user, password=mongo_password)
mongo_db = mongo_client[mongo_database]
mongo_collection = mongo_db['students']

prometheus_port = os.environ.get('PROMETHEUS_PORT', '9090')
start_http_server(int(prometheus_port))

@app.route('/insert', methods=['POST'])
def insert_data():
    data = request.json
    result = mongo_collection.insert_one(data)
    insert_counter.inc()
    app.logger.info(f"Inserted data: {data}")
    return jsonify({"id": str(result.inserted_id)})

@app.route('/update/<string:student_id>', methods=['PUT'])
def update_data(student_id):
    data = request.json
    result = mongo_collection.update_one({'_id': student_id}, {'$set': data})
    update_counter.inc()  
    app.logger.info(f"Updated data with ID: {student_id}")
    return "Data updated successfully"

@app.route('/delete/<string:student_id>', methods=['DELETE'])
def delete_data(student_id):
    result = mongo_collection.delete_one({'_id': student_id})
    delete_counter.inc()  
    app.logger.info(f"Deleted data with ID: {student_id}")
    return "Data deleted successfully"

@app.route('/select/<string:student_id>', methods=['GET'])
def select_data(student_id):
    get_counter.inc()
    data = mongo_collection.find_one({'_id': ObjectId(student_id)})
    if data:
        student_info = {
            "id": str(data['_id']),
            "student_name": data.get('student_name'),
            "student_age": data.get('student_age')
        }
        return jsonify(student_info)
    else:
        return "Data not found", 404

if __name__ == '__main__':
    app.run(debug=True)


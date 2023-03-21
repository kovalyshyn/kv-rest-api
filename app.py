import os
import dataset
from flask import Flask, jsonify, make_response, request

app = Flask(__name__)
if not os.path.exists("db"):
    os.makedirs("db")
db = dataset.connect('sqlite:///db/kv.db')

'''
Examples:
GET request to /api/kv returns all records
POST request to /api/kv creates a record
Sample request body -
{
  "key": "1",
  "value": "380990000000",
  "data": "Bla-bla-bla"
}
GET request to /api/kv/1 returns the details of record 1
PUT request to /api/kv/1 to update fields of record 1
DELETE request to /api/kv/1 deletes record 1
'''

table = db['storage']

def fetch_db(key):
    return table.find_one(key=key)

def fetch_db_all():
    kvs_list = []
    for kvs in table:
        kvs_list.append(kvs)
    return kvs_list

@app.route('/api/kv', methods=['GET', 'POST'])
def api_kv():
    if request.method == "GET":
        return make_response(jsonify(fetch_db_all()), 200)
    elif request.method == "POST":
        content = request.get_json()
        key = content['key']
        table.insert(content)
        return make_response(jsonify(fetch_db(key)), 201)  # 201 = Created


@app.route('/api/kv/<key>', methods=['GET', 'PUT', 'DELETE'])
def api_each_key(key):
    if request.method == "GET":
        kv_obj = fetch_db(key)
        if kv_obj:
            return make_response(jsonify(kv_obj), 200)
        else:
            return make_response(jsonify(kv_obj), 404)
    elif request.method == "PUT":
        content = request.json
        table.update(content, ['key'])
        kv_obj = fetch_db(key)
        return make_response(jsonify(kv_obj), 200)
    elif request.method == "DELETE":
        table.delete(id=key)
        return make_response(jsonify({}), 204)


if __name__ == '__main__':
    app.run(host='0.0.0.0')

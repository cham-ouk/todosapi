from flask import Flask, jsonify, request
import json
from datetime import datetime

app = Flask(__name__)


@app.route("/todos", methods=['GET'])
def get_todos():
    return jsonify(load_json('./todos.json'))


@app.route("/todo", methods=['POST'])
def post_todo():
    my_todos = load_json('./todos.json')

    id = len(my_todos) + 1

    client_payload = request.json
    # 2020-02-05 19:26:32
    client_payload["id"] = id
    created_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    client_payload["created_timestamp"] = created_timestamp
    client_payload["updated_timestamp"] = created_timestamp

    my_todos.append(client_payload)

    write_json("./todos.json", my_todos)

    return "Todo created"


def load_json(file_path):
    with open(file_path) as fl:
        return json.load(fl)


def write_json(file_path, payload):
    with open(file_path, 'w') as fl:
        json.dump(payload, fl)


if __name__ == '__main__':
    app.run()

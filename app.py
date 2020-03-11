from flask import Flask, jsonify, request
import json
from datetime import datetime

app = Flask(__name__)

app.config['JSON_SORT_KEYS'] = False


@app.route("/todos", methods=['GET'])
def get_todos():
    return jsonify(load_json('./todos.json'))


@app.route("/todo", methods=['POST'])
def post_todo():
    my_todos = load_json('./todos.json')

    id = len(my_todos) + 1

    client_payload = request.json

    created_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    temp_dict = dict()
    temp_dict["id"] = id
    temp_dict["task"] = client_payload["task"]
    temp_dict["status"] = client_payload["status"]
    temp_dict["created_timestamp"] = created_timestamp
    temp_dict["updated_timestamp"] = created_timestamp

    my_todos.append(temp_dict)

    write_json("./todos.json", my_todos)

    return "Todo created"


@app.route("/todo/<todo_id>", methods=['GET'])
def get_todo_by_id(todo_id):
    my_todos = load_json('./todos.json')

    for todo in my_todos:
        if 'id' in todo and todo['id'] == int(todo_id):
            return jsonify(todo)

    return '{id} does not exist in the database'.format(id=todo_id)


@app.route("/todo/<todo_id>", methods=['DELETE'])
def delete_todo_by_id(todo_id):
    my_todos = load_json('./todos.json')
    print(my_todos)
    for todo in my_todos:
        if 'id' in todo and todo['id'] == int(todo_id):
            my_todos.remove(todo)

    write_json("./todos.json", my_todos)
    return 'deleted'


@app.route("/todo/<todo_id>", methods=['PUT'])
def update_todo_by_id(todo_id):
    client_payload = request.json

    my_todos = load_json('./todos.json')
    created_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for todo in my_todos:
        if 'id' in todo and todo['id'] == int(todo_id):
            idx = my_todos.index(todo)
            todo["status"] = client_payload["status"]
            todo["updated_timestamp"] = created_timestamp
            my_todos[idx] = todo

    write_json("./todos.json", my_todos)
    return 'Updated'


def load_json(file_path):
    with open(file_path) as fl:
        return json.load(fl)


def write_json(file_path, payload):
    with open(file_path, 'w') as fl:
        json.dump(payload, fl)


if __name__ == '__main__':
    app.run()

import flask
from app import app
from .command import Command

command = Command()

@app.route('/add_transaction', methods = ['POST'])
def add_transaction():
    request = flask.request.get_json()
    receiver = request['receiver']
    amount = request['amount']
    data = command.add_transaction(receiver, amount)
    return flask.jsonify({'data': data}), 201

@app.route('/remove_pending_transaction', methods = ['POST'])
def remove_pending_transaction():
    request = flask.request.get_json()
    id = request['id']
    message = command.remove_pending_transaction(id)
    return flask.jsonify({'message': message}), 201

@app.route('/list_pending_transactions', methods = ['GET'])
def list_pending_transactions():
    transactions = command.list_pending_transactions()
    return flask.jsonify({'data': transactions}), 201

@app.route('/list_completed_transactions', methods = ['GET'])
def list_completed_transactions():
    transactions = command.list_completed_transactions()
    return flask.jsonify({'data': transactions}), 201

@app.route('/list_all_transactions', methods = ['GET'])
def list_all_transactions():
    transactions = command.list_all_transactions()
    return flask.jsonify({'data': transactions}), 201

@app.route('/list_transactions_by_address/<address>', methods = ['GET'])
def list_transactions_by_address(address: str):
    transactions = command.list_transactions_by_address(address)
    return flask.jsonify({'data': transactions}), 201

@app.route('/generate_wallet', methods = ['POST'])
def generate_wallet():
    message = command.generate_wallet()
    return flask.jsonify({'message': message}), 201

@app.route('/mine', methods = ['POST'])
def mine():
    message = command.mine()
    return flask.jsonify({'message': message}), 201

@app.route('/check_balance', methods = ['GET'])
def check_balance():
    message = command.check_balance()
    return flask.jsonify({'message': message}), 201

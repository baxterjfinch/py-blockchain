import os
import sys
import random
from uuid import *
from blockchain import *
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

node_identifier=str(uuid4()).replace('-', '')

# Initialize Blockchain
blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # Reward the miner for their contribution. 0 means a new coin has been mined
    blockchain.new_transaction(
        sender = "0",
        recipient = node_identifier,
        amount = 1,
    )

    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "Block mined successfully",
        'block': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }

    return jsonify(response), 200



@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    required = ['sender', 'recipient', 'amount']

    # Verify all required values are present
    if not all(k in values for k in required):
        return f"Missing Value: {k}", 400

    # Create a new transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
    response = {'message': f'Transaction is scheduled to be add to Block No. {index}'}

    return jsonify(response), 201

@app.route('/chain', methods=['GET'])

def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }

    return jsonify(response), 200



# @app.route("/")
# def index():
#     url = random.choice(images)
#     return render_template("index.html", url=url)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

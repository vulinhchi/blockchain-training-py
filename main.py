import blockchain
from flask import Flask, jsonify

app = Flask(__name__)
app.config.from_object(__name__)

app.blocks = [blockchain.GENESIS]
app.peers = {}
app.json_encoder = blockchain.JSONEncoder


@app.route('/blocks', methods=['GET'])
def list_blocks():
    return jsonify(app.blocks)


@app.route('/peers', methods=['GET'])
def list_peers():
    return jsonify(app.peers)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2345)

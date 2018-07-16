import json
from datetime import datetime

from flask import Flask, jsonify


class Block(object):
    def __init__(self, index, previous_hash, timestamp, data, nonce, hashvalue=''):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.nonce = nonce
        self.hash = hashvalue

    def calculate_hash(self):
        # TODO
        pass

    @staticmethod
    def from_previous(block, data):
        return Block(block.index + 1, block.hash, datetime.now(), data, 0)

    @staticmethod
    def from_json(block):
        block = Block(**block)
        assert block.calculate_hash() == block.hash
        return block

    def __repr__(self):
        return str(self.__dict__)


GENESIS = Block(
    0, '', 1522983367254, None, 0,
    'e063dac549f070b523b0cb724efb1d4f81de67ea790f78419f9527aa3450f64c'
)


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__


class Server(object):
    def __init__(self):
        self.blocks = [GENESIS]
        self.peers = {}

        self.app = Flask(__name__)
        self.app.config.from_object(self)
        self.app.json_encoder = JSONEncoder
        self.app.route('/blocks', methods=['GET'])(self.list_blocks)
        self.app.route('/peers', methods=['GET'])(self.list_peers)

    def list_blocks(self):
        return jsonify(self.blocks)

    def list_peers(self):
        return jsonify(self.peers)

    def run(self):
        self.app.run(host='0.0.0.0', port=2345)

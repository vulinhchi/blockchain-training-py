import json
import logging
import socket
import time
from datetime import datetime
from threading import Thread
import hashlib
from flask import Flask, jsonify
from Crypto.PublicKey import RSA
from Crypto import Random

class Block(object):
    def __init__(self, index, previous_hash, timestamp, data, nonce, hashvalue=''):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.nonce = nonce
        self.hash = hashvalue

    def calculate_hash(self):
        t = str(self.index)+str(self.previous_hash) +str(self.timestamp) +str(self.data) +str(self.nonce )
        t = t.encode()
        k = hashlib.sha256(t).hexdigest()
        # sha = hasher.sha256()
        # sha.update(str(self.index)+
        #                 str(self.previous_hash) +
        #                 str(self.timestamp) +
        #                 str(self.data) +
        #                 str(self.nonce ))
        # self.hash = sha.hexdigest()
        # return sha.hexdigest()
        self.hash = k
        return k
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
    '8f6f732cd654d627d1d6bb532deb86a33653546a1741b2c179559466a6504f20'
)


# blockchain = [GENESIS]
#
# print ('block dau tien ',GENESIS.hash)
# for i in range(0,4):
#     previous_block = blockchain[-1]
#     print ('hash block trk ', Block.calculate_hash(previous_block))
#     block_to_add =Block.from_previous(previous_block, "data")
#     block_to_add.hash=Block.calculate_hash(block_to_add) # tinh toan hash cua block hien tai
#     blockchain.append(block_to_add)
#     #previous_block = block_to_add
#     print ('stt {}'.format(block_to_add.index))
#     print ('HASH: {}'.format(block_to_add.hash))


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__


class Server(object):
    def __init__(self):
        self.blocks = [GENESIS]
        self.peers = {}

        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.udp_logger = logging.getLogger('UDP')

        self.http = Flask(__name__)
        self.http.config.from_object(self)
        self.http.json_encoder = JSONEncoder
        self.http.route('/blocks', methods=['GET'])(self.list_blocks)
        self.http.route('/peers', methods=['GET'])(self.list_peers)
        self.http.route('/blocks', methods=['POST'])(self.add_blocks)
        self.http.route('/transactions', methods=['POST'])(self.add_transactions)

    def list_blocks(self):
        return jsonify(self.blocks)

    def list_peers(self):
        return jsonify(self.peers)

    def proof_of_work(self, block):
        block.nonce = 0
        block.hash = Block.calculate_hash(block)
        while not block.hash.startswith('000'):
            block.nonce +=1
            block.hash = Block.calculate_hash(block)
        return block.hash #return ve 1 hash hop le proof_of_work
    def add_blocks(self):

        previous_block = blocks[-1]
        current_block = Block.from_previous(previous_block, "ahihi") # tao ra 1 block moi

        # start with '000' >> proof-of-work
        current_block.hash = self.proof_of_work(current_block)
        #if current_block.hash.startswith('000'): pass
        #check : so sanh vs hash cua block trk
        if previous_block.hash == current_block.previous_hash and current_block.index > previous_block.index:
            blocks.append(current_block)


    def add_transactions(self):
        # TODO
        pass

    def createAccount(self):
        #generate key pair based on password
        #WITH NO PASSWORD :'(
        # a = Random.new().read
        # print (a)
        private_key = RSA.generate(1024, Random.new().read)
        public_key = private_key.publickey()
        return public_key.exportKey(),private_key.exportKey()

    def run(self, host='0.0.0.0'):
        logging.info('Starting...')
        self.udp.bind((host, 2346))
        udp_listen = Thread(target=self.udp_listen)
        udp_broadcast = Thread(target=self.udp_broadcast)
        udp_listen.start()
        udp_broadcast.start()

        self.http.run(host=host, port=2345)
        udp_listen.join()
        udp_broadcast.join()

    def udp_broadcast(self):
        while True:
            self.udp.sendto(b'hello', ('255.255.255.255', 2346))
            time.sleep(1)

    def udp_listen(self):
        while True:
            message, remote = self.udp.recvfrom(8)
            address, _ = remote
            self.udp_logger.debug([message, remote])
            if message == b'hello' and address not in self.peers:
                self.peers[address] = remote
                self.udp_logger.info('Peer discovered: %s', remote)

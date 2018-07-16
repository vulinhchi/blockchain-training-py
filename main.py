from flask import Flask

# from . import blockchain

app = Flask(__name__)
app.config.from_object(__name__)

app.blocks = []
app.peers = {}


@app.route('/blocks', methods=['GET'])
def list_blocks():
    return app.blocks


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2345)

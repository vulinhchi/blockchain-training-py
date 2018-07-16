import logging
import sys

import blockchain

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

if __name__ == '__main__':
    server = blockchain.Server()
    server.run()

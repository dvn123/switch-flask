import os

from switch import create_app

PORT = os.environ.get('PORT') or 4000
IP = os.environ.get('IP') or "127.0.0.1"

if __name__ == '__main__':
    create_app().run(host=IP, port=int(PORT))

#TODO - try catch converter em objectId, testes, transação
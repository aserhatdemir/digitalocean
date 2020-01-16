#bin#!/bin/bash
echo "Hello World"
apt update
ufw allow 5000
apt install -y python3
apt install -y python3-pip
git clone https://github.com/aserhatdemir/increment-get.git
cd increment-get
pip3 install -r requirements.txt
export PYTHONDONTWRITEBYTECODE=1
export FLASK_APP="web.py"
export FLASK_ENV="development"
export FLASK_DEBUG=True
fuser -n tcp -k 5000
flask run --host=0.0.0.0 &
echo "done"
## Binance Trader Bot
### Install
Clone the folder, go inside, create a virtual environment for Python with virtualenv (*!!! maybe you have to install [virtualenv](https://virtualenv.pypa.io/en/stable/) !!!*), activate it, and install all necessary dependencies ([python-binance](https://github.com/sammchardy/python-binance)):
```shell
$ git clone https://github.com/JBthePenguin/BinanceTraderBot.git
$ cd BinanceTraderBot
$ virtualenv -p python3 env
$ source env/bin/activate
(env)$ pip install -r requirements.txt
```
Create a file *api_keys.py* and set your Binance API keys:
```python
API_KEY = "your api key"
SECRET = "your secret key"
```
### Run
Start the trader bot:
```shell
(env)$ python trader.py
```
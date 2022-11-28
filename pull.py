import discord
import requests
import  json
import time
from discord import *
from discord.ext import commands

client_id = config['client_id']
client_secret = config['client_secret']
redirect_uri = config['redirect_uri']
token = config['bot_token']

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
  return requests.post("https://discord.com/api/v8/oauth2/token" , data=data, headers=headers).json()

def add_to_guild(access_token, user_id , guild_id):
        data = {
        "access_token" : access_token,
    }
        headers = {
        "Authorization" : f"Bot {token}",
        'Content-Type': 'application/json'

    }
        response = requests.put(f"https://discord.com/api/v8/guilds/{guild_id}/members/{user_id}", headers=headers, json=data)
        if response.status_code == 429:
          time.sleep(3)
          return add_to_guild(access_token, user_id, guild_id)
        print(response.text)

gid = input("guild id: ")
for user in open('codes.txt', 'r').read().splitlines():
  add_to_guild(access_token=user.split(':')[1], user_id=user.split(':')[0],guild_id=gid)

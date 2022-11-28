import discord
import requests
import  json
import time
from discord import *
from discord.ext import commands

CLIENT_ID = '1032041484045787146'
CLIENT_SECRET = 'DXqIdk3jHkn0uvYfV0W4PlMHK1ndS_5C'
REDIRECT_URI = 'https://discord.com/api/oauth2/authorize?client_id=1032041484045787146&redirect_uri=http%3A%2F%2F209.126.82.205%3A5000%2Fauthenticate&response_type=code&scope=identify%20guilds.join' 

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
        "Authorization" : f"Bot {botToken}",
        'Content-Type': 'application/json'

    }
        response = requests.put(f"https://discord.com/api/v8/guilds/{guild_id}/members/{user_id}", headers=headers, json=data)
        if response.status_code == 429:
          time.sleep(3)
          return add_to_guild(access_token, user_id, guild_id)
        print(response.text)

for user in open('codes.txt', 'r').read().splitlines():
  add_to_guild(access_token=user.split(':')[1], userID=user.split(':')[0],guild_Id="1034897497698598923")

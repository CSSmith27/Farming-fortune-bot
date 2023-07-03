import os
import discord
import requests

API_KEY = os.environ['API']

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)

def get_uuid(name):
    data = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{name}").json()
    return data['id']

def get_farming_fortune(name):
    uuid = get_uuid(name)
    data = requests.get(f"https://api.hypixel.net/player?key={API_KEY}&name={name}").json()

    # Check if the 'profiles' key is in the response data
    if 'profiles' in data:
        profiles = data['profiles']
        # Assuming using the first profile, ideally you should let the user specify which profile to use
        # The farming fortune might be nested deeper, you need to check the API response
        if profiles and uuid in profiles[0]["members"]:
            farming_fortune = profiles[0]["members"][uuid].get("farming_fortune", "No farming fortune data")
        else:
            farming_fortune = "Could not find farming fortune data"
    else:
        farming_fortune = "Could not find profiles in response data"
    
    return farming_fortune


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    msg = message.content

    # New command for fetching farming fortune
    if msg.startswith('fjfortune '):
        name = msg.split("fjfortune ", 1)[1]
        farming_fortune = get_farming_fortune(name)
        await message.channel.send(f'Farming Fortune for {name}: {farming_fortune}')

    if msg.startswith('genlink '):
        name = msg.split("genlink ", 1)[1]
        await message.channel.send(f'https://api.hypixel.net/player?key={API_KEY}&name={name}')

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

# Retrieve the bot token from the environment variable 'TOKEN'
my_secret = os.environ['TOKEN']

# Start the bot
client.run(my_secret)

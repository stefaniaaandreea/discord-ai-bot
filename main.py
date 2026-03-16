import discord
import requests
import os

API_KEY = os.getenv("OPENAI_API_KEY")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

API_URL = "https://api.openai.com/v1/chat/completions"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

def generateRequest(question):
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant in a discord server"},
            {"role": "user", "content": question}
        ],
        "temperature": 1
    }
    return data

def sendRequestAPI(question):
    data = generateRequest(question)
    response = requests.post(API_URL, headers=headers, json=data)

    if response.status_code == 200:
        response_json = response.json()
        assistant_message = response_json["choices"][0]["message"]["content"]
        return assistant_message
    else:
        print(f"Error: {response.status_code} - {response.text}")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message:
        await message.channel.send(sendRequestAPI(message.content))


client.run(DISCORD_TOKEN)
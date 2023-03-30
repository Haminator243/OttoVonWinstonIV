#This is where the fun begins
import requests
from bs4 import BeautifulSoup
import time
import discord
import os
from dotenv import load_dotenv
import threading

#Web Page URLs
RECCE_RIG_URL = "https://onwardresearch.com/recce-rig/"
SIMP_POUCH_URL = "https://onwardresearch.com/simp-pouch/"
GORILLA_MIND_SMOOTH_URL = "https://gorillamind.com/products/gorilla-mind-smooth"

#Declaraion of global item stock messages.
RECCE_RIG_STOCK_STATUS = "RECCE RIG not in stock. :("
SIMP_POUCH_STOCK_STATUS = "SIMP Pouch not in stock. :("
GORILLA_MIND_SMOOTH_STOCK_STATUS = "SIMP Pouch not in stock. :("

#TODO: Create url .json

#Creating discord client object
intents=discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

#Grab environment variables
load_dotenv()

def main():
    botThread = threading.Thread(target= bot_func)
    
    # discord event to check when the bot is online 
    @client.event
    async def on_ready():
        print(f'{client.user} is now online!')   
    botThread.start()

    while(1):
        global RECCE_RIG_STOCK_STATUS
        global SIMP_POUCH_STOCK_STATUS
        global GORILLA_MIND_SMOOTH_STOCK_STATUS

        print("Searching web pages...")
        #Page Requests
        recceRigPageRequest = requests.get(RECCE_RIG_URL)
        recceRigBeautifulSoupObject = BeautifulSoup(recceRigPageRequest.text, 'html.parser')

        simpPouchPageRequest = requests.get(SIMP_POUCH_URL)
        simpPouchBeautifulSoupObject = BeautifulSoup(simpPouchPageRequest.text, 'html.parser')

        gorillaMindSmoothPageRequest = requests.get(GORILLA_MIND_SMOOTH_URL)
        gorillaMindSmoothBeautifulSoupObject = BeautifulSoup(gorillaMindSmoothPageRequest.text, 'html.parser') 

        time.sleep(300)

 
def bot_func():
    global RECCE_RIG_STOCK_STATUS
    global SIMP_POUCH_STOCK_STATUS
    global GORILLA_MIND_SMOOTH_STOCK_STATUS

    global RECCE_RIG_URL
    global SIMP_POUCH_URL
    global GORILLA_MIND_SMOOTH_URL
    @client.event
    async def on_message(message): 
        # make sure bot doesn't respond to it's own messages to avoid infinite loop
        if message.author == client.user:
            return  
        if "+otto" in message.content.lower():
            messageSent = False
            helpMessage = ("To check the stock on the RECCE Rig type:\n    +Otto recce\n"
                           "To check the stock on the SIMP Pouch type:\n    +Otto simp\n"
                           "To check the stock on Gorilla Mind Smooth type:\n    +Otto gorilla\n    +Otto mind\n    +Otto smooth\n"
                           "To check all items type:\n    +Otto all\n")
            messageContent = message.content.lower()
            messageList = messageContent.split(" ")
            for input in messageList:
                if "all" in input:
                    await message.channel.send(
                        f"{RECCE_RIG_STOCK_STATUS}\n{RECCE_RIG_URL}\n\n"
                        f"{SIMP_POUCH_STOCK_STATUS}\n{SIMP_POUCH_URL}\n\n"
                        f"{GORILLA_MIND_SMOOTH_STOCK_STATUS}\n{GORILLA_MIND_SMOOTH_URL}\n"
                        )
                    messageSent = True
                if "help" in input:
                    await message.channel.send(f"{helpMessage}\n")
                    messageSent = True
                if "recce" in input:
                    await message.channel.send(f"{RECCE_RIG_STOCK_STATUS}\n{RECCE_RIG_URL}\n")
                    messageSent = True
                if "simp" in input:
                    await message.channel.send(f"{SIMP_POUCH_STOCK_STATUS}\n{SIMP_POUCH_URL}\n")
                    messageSent = True
                if ("gorilla" in input) or ("mind" in input) or ("smooth" in input):
                    await message.channel.send(f"{GORILLA_MIND_SMOOTH_STOCK_STATUS}\n{GORILLA_MIND_SMOOTH_URL}\n")
                    messageSent = True
            if not messageSent:
                await message.channel.send(f"I wasn't able to find what you were asking\nThese are my only commands:\n{helpMessage}\n")

    client.run(os.getenv('TOKEN'))


if __name__ == "__main__":
    main()
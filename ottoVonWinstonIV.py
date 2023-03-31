#This is where the fun begins
import time
import discord
import os
from dotenv import load_dotenv
import threading
import json
import webScrape

#Creating discord client object
intents=discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

#Grab environment variables
load_dotenv()

#initialize global variable
itemCatalog = {}

def main():
    botThread = threading.Thread(target= bot_func)
    
    # discord event to check when the bot is online 
    @client.event
    async def on_ready():
        print(f'{client.user} is now online!')
    botThread.start()

    while(1):
        jsonFile = open("config.json")
        websiteData = json.load(jsonFile)
        global itemCatalog
        for website in websiteData:
            for item in websiteData[website]:
                #Page request
                soupObject = webScrape.page_request(websiteData[website][item]["url"])
                #Check if item is in stock
                stockStatus = webScrape.stock_request(soupObject, websiteData[website][item]["stockCheckType"])
                #Add item to the catalog
                itemCatalog[item] = (f"{item} is {stockStatus}", websiteData[website][item]["url"])
        time.sleep(60)

 
def bot_func():
    global itemCatalog
    @client.event
    async def on_message(message): 
        # make sure bot doesn't respond to it's own messages to avoid infinite loop
        if message.author == client.user:
            return  
        if "+otto" in message.content.lower():
            messageSent = False
            messageContent = message.content.lower()
            messageList = messageContent.split(" ")
            for input in messageList:
                if "all" in input:
                    response = ""
                    for item in itemCatalog:
                        response = response + f"{itemCatalog[item][0]}\n{itemCatalog[item][1]}\n\n"
                    await message.channel.send(response)    
                    messageSent = True
                if "help" in input:
                    helpMessage = ""
                    for item in itemCatalog:
                        helpMessage = helpMessage + f"To check the stock on {item} type:\n"
                        for name in item.split(" "):
                            helpMessage = helpMessage + f"    +Otto {name.lower()}\n"
                        helpMessage = helpMessage + "\n\n"
                    await message.channel.send(f"{helpMessage}\n")
                    messageSent = True
                for item in itemCatalog:
                    if input in item.lower(): #This may become problematic as the list of items grows.
                      await message.channel.send(f"{itemCatalog[item][0]}\n{itemCatalog[item][1]}\n") 
                      messageSent = True 
            if not messageSent:
                await message.channel.send(f"I wasn't able to find what you were asking\nPlease type \"+Otto help\" to see a list of my commands.\n")

    client.run(os.getenv('TOKEN'))


if __name__ == "__main__":
    main()
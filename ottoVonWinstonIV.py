#This is where the fun begins
import time
import discord
import os
from dotenv import load_dotenv
import threading
import json
import webScrape
import asyncio

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

    global itemCatalog
    global client

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
                        response = response + f"{itemCatalog[item][0]}\n{itemCatalog[item][1]}\n{itemCatalog[item][2]}\n\n"
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
                      await message.channel.send(f"{itemCatalog[item][0]}\n{itemCatalog[item][1]}\n{itemCatalog[item][2]}\n\n") 
                      messageSent = True 
            if not messageSent:
                await message.channel.send(f"I wasn't able to find what you were asking\nPlease type \"+Otto help\" to see a list of my commands.\n")

    async def recceInStockMessage():
        channel = client.get_channel(int(os.getenv('OTTO_CHANNEL')))
        while(0): #Keeping this as an example on how to send messages to a channel without a prompt
            await asyncio.sleep(10)
            if itemCatalog["RECCE Rig"][0] == "RECCE Rig is in stock!":
                await channel.send(itemCatalog["RECCE Rig"][0] + "\n\n")
                print(itemCatalog["RECCE Rig"][0] + "\n\n")
            else:
                print(itemCatalog["RECCE Rig"][0] + "\n\n")

    async def inStockMessage():
        channel = client.get_channel(int(os.getenv('OTTO_CHANNEL')))
        await asyncio.sleep(5)
        oldCatalog = itemCatalog
        while(1): 
            await asyncio.sleep(1)
            for item in itemCatalog:
                try:
                    if (
                        (oldCatalog[item][0] != itemCatalog[item][0])
                        and not 
                        (("Please contact bot administrator." in oldCatalog[item][0]) or ("Please contact bot administrator." in itemCatalog[item][0])) 
                        and not 
                        ((f"failed to correctly get {item} stock status." in oldCatalog[item][0]) or (f"failed to correctly get {item} stock status." in itemCatalog[item][0]))
                        ):
                        await channel.send("**Stock Change Alert!**\n" + f"{itemCatalog[item][0]}\n{itemCatalog[item][1]}\n{itemCatalog[item][2]}\n\n")
                except Exception as error:
                    print(f"Failed to send stock alert message. Failed with error: {error}")
            
            oldCatalog = itemCatalog           


    async def fridaySpecial():
        channel = client.get_channel(int(os.getenv('GAME_CHAT_CHANNEL')))
        fridaySpecialPath = os.getcwd() + "\FridaySpecial.mov"
        fridaySpecialFile = discord.File(fridaySpecialPath, filename = "FridaySpecial.mov")
        while(1):
            await asyncio.sleep(60*5)
            currentTime = time.localtime()
            if (currentTime.tm_wday == 4) and (currentTime.tm_hour == 9) and (currentTime.tm_min < 10):
                try:
                    await channel.send(file=fridaySpecialFile)
                except Exception as error:
                    print(f"Failed to send Friday Special. Error output is {error}")

                await asyncio.sleep(60*5 + 1)

    # discord event to check when the bot is online 
    @client.event
    async def on_ready():
        print(f'{client.user} is now online!')
        await recceInStockMessage()
        await inStockMessage()
        await fridaySpecial()
    botThread.start()

    while(1):
        jsonFile = open("config.json")
        websiteData = json.load(jsonFile)
        for website in websiteData:
            for item in websiteData[website]:
                #Page request
                url = websiteData[website][item]["url"]
                try:
                    soupObject = webScrape.page_request(url)
                except Exception as error:
                    print(f"Failed to get web page html for {item} with url: {url}\nError given: {error}\n\n")
                #Check if item is in stock
                try:
                    stockStatus = webScrape.stock_request(soupObject, websiteData[website][item]["stockCheckType"])
                except Exception as error:
                    print(f"Failed to parse web page html for {item}.\nError given: {error}\n\n")
                    stockStatus = f"failed to correctly get {item} stock status."
                #Add item to the catalog
                itemCatalog[item] = (f"**{item}** is {stockStatus}", f"Time of search: {time.asctime()}", websiteData[website][item]["url"])
        time.sleep(60)

 
def bot_func():  
    client.run(os.getenv('TOKEN'))


if __name__ == "__main__":
    main()
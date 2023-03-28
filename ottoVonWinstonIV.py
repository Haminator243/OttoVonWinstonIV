#This is where the fun begins
import webbrowser
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

#Creating discord client object
intents=discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

#Grab environment variables
load_dotenv()

def main():
    #test = webbrowser.open(RECCE_RIG_URL, new=1) #This opens a web browser for the user. It doesn't grab the html.
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
        gorillaMindSmootBeautifulSoupObject = BeautifulSoup(gorillaMindSmoothPageRequest.text, 'html.parser')

        #Checking the product availability 
        if onward_research_item_stock_check(recceRigBeautifulSoupObject):
            print("RECCE Rig in stock!\n")
            RECCE_RIG_STOCK_STATUS = "RECCE Rig in stock!"
        else:
            print("RECCE Rig not in stock. :(\n")
            RECCE_RIG_STOCK_STATUS = "RECCE Rig not in stock. :("

        if onward_research_item_stock_check(simpPouchBeautifulSoupObject):
            print("SIMP Pouch in stock!\n")
            SIMP_POUCH_STOCK_STATUS = "SIMP Pouch in stock!"
        else:
            print("SIMP Pouch not in stock. :(\n")
            SIMP_POUCH_STOCK_STATUS = "SIMP Pouch not in stock. :("

        if gorilla_mind_item_stock_check(gorillaMindSmootBeautifulSoupObject):
            print("Gorilla Mind Smooth in stock!\n")
            GORILLA_MIND_SMOOTH_STOCK_STATUS = "Gorilla Mind Smooth in stock!"
        else:
            print("Gorilla Mind Smooth not in stock. :(\n")
            GORILLA_MIND_SMOOTH_STOCK_STATUS = "Gorilla Mind Smooth not in stock. :("    

        time.sleep(300)
    

def clean_html_text(htmlText):
    """Cleaning the "undesirables" out of your html"""
    htmlText = htmlText.replace("\n", "")
    htmlText = htmlText.replace("\xa0", "")

    return htmlText


def onward_research_item_stock_check(soupObject):
    tempDict = {"class": "product-quantity-submit"}
    tempSoupStorage = soupObject.find("div", tempDict)
    productQuantitySubmitClassText = tempSoupStorage.text
    if "Add to Bag" in productQuantitySubmitClassText:
        return True
    elif "Sold Out" in productQuantitySubmitClassText:
        return False
    else:
        print("Unable to find purchase button info")
        return False
    
def gorilla_mind_item_stock_check(soupObject):
    tempDict = {"class": "product__price"}
    tempSoupStorage = soupObject.find("div", tempDict)
    productPriceClassText = tempSoupStorage.text
    if "Add to Cart" in productPriceClassText:
        return True
    elif "Sold Out" in productPriceClassText:
        return False
    else:
        print("Unable to find purchase button info")
        return False

 
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
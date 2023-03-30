import requests
from bs4 import BeautifulSoup

def page_request(URL):
    pageRequest = None
    pageRequest = requests.get(URL)
    beautifulSoupObject = BeautifulSoup(pageRequest.text, 'html.parser')
    return pageRequest


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
    
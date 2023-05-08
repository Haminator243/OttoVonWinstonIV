import requests
from bs4 import BeautifulSoup

def page_request(URL):
    pageRequest = None
    pageRequest = requests.get(URL)
    beautifulSoupObject = BeautifulSoup(pageRequest.text, 'html.parser')
    return beautifulSoupObject


def stock_request(soupObject, key):
    match key:
        case 0:
            return onward_research_item_stock_check(soupObject)
        case 1:
            return gorilla_mind_item_stock_check(soupObject)


def onward_research_item_stock_check(soupObject):
    tempDict = {"class": "product-quantity-submit"}
    tempSoupStorage = soupObject.find("div", tempDict)
    productQuantitySubmitClassText = tempSoupStorage.text
    if "Add to Bag" in productQuantitySubmitClassText:
        return "in stock!"
    elif "Sold Out" in productQuantitySubmitClassText:
        return "not in stock :("
    else:
        print("Unable to find purchase button info")
        return "unable to successfully find stock status. Please contact bot administrator."
    

def gorilla_mind_item_stock_check(soupObject):
    tempDict = {"class": "product__price"} #When item is out of stock
    tempSoupStorage = soupObject.find("div", tempDict)
    productPriceClassText = tempSoupStorage.text
    
    if "Add to Cart" in productPriceClassText:
        return "in stock!"
    elif "Sold Out" in productPriceClassText:
        return "not in stock :("
    
    tempDict = {"class":"product-form__group"} #When item is in stock
    tempSoupStorage = soupObject.find("div", tempDict)
    productPriceClassText = tempSoupStorage.text   

    if "Add to Cart" in productPriceClassText:
        return "in stock!"
    elif "Sold Out" in productPriceClassText:
        return "not in stock :("
    else:
        print("Unable to find purchase button info")
        return "unable to successfully find stock status. Please contact bot administrator."
    
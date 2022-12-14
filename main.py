import requests
from bs4 import BeautifulSoup
import json

directory = "recipes/"

def scrapeRecipe():
    link = input("Insert you recipe here -> ")
    page = requests.get(link)
    # print("\nURL:", link)
    # print("******************")

    ingredients = []
    title = []

    soup = BeautifulSoup(page.text, 'html.parser')
    titleText = soup.find_all("h1", {"class": "tdb-title-text"})
    for ti in titleText:
        title.append("Titlu reteta")
        title.append(ti.text)

    ingred = soup.find_all("div", {"class": "wprm-recipe-ingredient-group"})
    for ing in ingred:
        ingredients.append("Ingrediente")
        ingredients.append(ing.text)

    # print(title, "\n", ingredients, "\n")
    return title, ingredients

def convertListToDictionary(lst):
    res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return res_dct

def createJsonFile():
    title, ingredients = scrapeRecipe()
    dictionary = {}
    dictionary.update(convertListToDictionary(title))
    dictionary.update(convertListToDictionary(ingredients))
    jsonString = json.dumps(dictionary, indent=2)
    jsonFile = open(directory + "shoppingCart.json", "w")
    jsonFile.write(jsonString)
    print("Check your ShoppingCart.json file! :)")

createJsonFile()


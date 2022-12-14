import requests
from bs4 import BeautifulSoup
import json

directory = "recipes/"
# https://jamilacuisine.ro/dovlecei-pane-in-crusta-de-pesmet-si-in-aluat/

def scrapeRecipe():
    link = input("Insert you recipe here -> ")
    page = requests.get(link)
    # print("\nURL:", link)
    # print("******************")
    soup = BeautifulSoup(page.text, 'html.parser')

    ingredientName = []
    ingredientAmount = []
    ingredientUnit = []

    # titlul retetei
    title = soup.select('.tdb-title-text')[0].text.strip().replace("/", "").split("–")[0]
    print("recipe name :", title)

    # grupele de ingrediente -> ex. vezi reteta cu dovlecei, are 2 : pt dovlecei in aluat/crusta de pesmet
    ingredient_groups = soup.select('.wprm-recipe-ingredient-group')
    print("ingredient group(s) :", ingredient_groups)


    ingName = soup.find_all("span", {"class": "wprm-recipe-ingredient-name"})
    for i in ingName:
        ingredientName.append(i.text)

    print("ingredient name :", ingredientName)

    ingAmount = soup.find_all("span", {"class": "wprm-recipe-ingredient-amount"})
    for i in ingAmount:
        ingredientAmount.append(i.text)

    print("ingredient amount :", ingredientAmount)

    ingUnit = soup.find_all("span", {"class": "wprm-recipe-ingredient-unit"})
    for i in ingUnit:
        ingredientUnit.append(i.text)

    print("ingredient unit :", ingredientUnit)



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

scrapeRecipe()


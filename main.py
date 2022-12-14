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

    if len(ingredient_groups) == 1:
        try:
            # linia pe care se afla un ingredient dintr un grup de ingrediente
            ingredients_unparsed = ingredient_groups[0].select('.wprm-recipe-ingredients > .wprm-recipe-ingredient')
        except:
            return
        
    #      extragem informatiile despre fiecare ingredient: amount, unit, name
        for i in ingredients_unparsed:
            # ingredient amount
            ingredient_amount = i.select('.wprm-recipe-ingredient-amount')
            ingredient_amount_parsed = ''
            if ingredient_amount:
                ingredient_amount_parsed = i.select('.wprm-recipe-ingredient-amount')[0].text.strip()

            # ingredient unit
            ingredient_unit = i.select('.wprm-recipe-ingredient-unit')
            ingredient_unit_parsed = ''
            if ingredient_unit:
                ingredient_unit_parsed = i.select('.wprm-recipe-ingredient-unit')[0].text.strip()

            # ingredient name
            ingredient_name = i.select('.wprm-recipe-ingredient-name')
            ingredient_name_parsed = ''
            if ingredient_name:
                ingredient_name_parsed = i.select('.wprm-recipe-ingredient-name')[0].text.strip()




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


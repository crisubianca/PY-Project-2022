from bs4 import BeautifulSoup
import requests
from re import sub
import re
import json
import pdb

directory = "recipes/"

recipe = {} # it's not an actual recipe, more like a list of shopping cart

def custom_merge(dictionary, subdictionary, ingredient_name):
    if ingredient_name in dictionary and dictionary[ingredient_name]['unit'] == subdictionary['unit']:
        try:
            dictionary[ingredient_name]['amount'] = float(dictionary[ingredient_name]['amount']) + float(subdictionary['amount'])
        except ValueError:
            pass
    else:
        dictionary[ingredient_name] = subdictionary

def scrapeRecipe(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.text, 'html.parser')

    # titlul retetei
    title = soup.select('.tdb-title-text')[0].text.strip().replace("/", "").split("–")[0]
    print("recipe name :", title)

    # grupele de ingrediente -> ex. vezi reteta cu dovlecei, are 2 : pt dovlecei in aluat/crusta de pesmet
    ingredient_groups = soup.select('.wprm-recipe-ingredient-group')

    for j in ingredient_groups:
        group_ingredients_unparsed = j.select('.wprm-recipe-ingredients > .wprm-recipe-ingredient')
        for i in group_ingredients_unparsed:
            ingredient_amount = i.select('.wprm-recipe-ingredient-amount')
            ingredient_amount_parsed = ''
            if ingredient_amount:
                ingredient_amount_parsed = i.select('.wprm-recipe-ingredient-amount')[0].text.strip()

            ingredient_unit = i.select('.wprm-recipe-ingredient-unit')
            ingredient_unit_parsed = ''
            if ingredient_unit:
                ingredient_unit_parsed = i.select('.wprm-recipe-ingredient-unit')[0].text.strip()

            ingredient_name = i.select('.wprm-recipe-ingredient-name')
            ingredient_name_parsed = ''
            if ingredient_name:
                ingredient_name_parsed = i.select('.wprm-recipe-ingredient-name')[0].text.strip()

            # construim ingredientul
            ingredient = {'amount': ingredient_amount_parsed, 'unit': ingredient_unit_parsed}
            # i = ingredient_amount_parsed + " " + ingredient_unit_parsed + " " + ingredient_name_parsed

            custom_merge(recipe, ingredient, ingredient_name_parsed)


def writeInJson(shopping_cart):
    json_string = json.dumps(shopping_cart, indent=4)
    with open(f"recipes/ShoppingCart", "w") as out_file:
        out_file.write(json_string)


def main():
    links = ['https://jamilacuisine.ro/dovlecei-pane-in-crusta-de-pesmet-si-in-aluat/',
             'https://jamilacuisine.ro/chec-pufos-cu-cacao-reteta-video/',
             'https://jamilacuisine.ro/budinca-de-dovlecei-cu-bacon-reteta-video/']
    for link in links:
        scrapeRecipe(link)

    writeInJson(recipe)


main()


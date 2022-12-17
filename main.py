from bs4 import BeautifulSoup
import requests
from re import sub
import re
import json
import pdb

directory = "recipes/"

# "dovlecei": [{"unit":"lingura", "qty":"3"},
#              {"unit":"kg","qty":5"}]

recipe = {} # it's not an actual recipe, more like a list of shopping cart


def custom_merge(dictionary, subdictionary, ingredient_name):
    if ingredient_name in dictionary:
        for i in range(len(dictionary[ingredient_name])):
            if dictionary[ingredient_name][i]['unit'] == subdictionary['unit']:
                try:
                    dictionary[ingredient_name][i]['amount'] = float(dictionary[ingredient_name][i]['amount']) + float(
                        subdictionary['amount'])
                except ValueError as error:
                    print(error)
                break
            if i == len(dictionary[ingredient_name]) - 1 and dictionary[ingredient_name][i]['unit'] != subdictionary[
                'unit']:
                dictionary[ingredient_name].append(subdictionary)
                dictionary[ingredient_name][-1]['amount'] = float(dictionary[ingredient_name][-1]['amount'])


    else:

        dictionary[ingredient_name] = [subdictionary]
        dictionary[ingredient_name][-1]['amount'] = float(dictionary[ingredient_name][-1]['amount'])


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

            # verificam daca avem 3-4 in amount
            try:
                ingredient_amount_parsed = ingredient_amount_parsed.split('-')[-1]
            except ValueError:
                print(ValueError)

            if ingredient_amount_parsed == 'putina' or ingredient_amount_parsed == 'putin':
                ingredient_amount_parsed = 1
            ingredient = {'amount': ingredient_amount_parsed if ingredient_amount_parsed else 1,
                          'unit': ingredient_unit_parsed if ingredient_unit_parsed else 'bucata'}

            custom_merge(recipe, ingredient, ingredient_name_parsed)


def writeInJson(shopping_cart):
    json_string = json.dumps(shopping_cart, indent=4)
    with open(f"recipes/ShoppingCart", "w") as out_file:
        out_file.write(json_string)


def main():
    links = ['https://jamilacuisine.ro/dovlecei-pane-in-crusta-de-pesmet-si-in-aluat/',
             'https://jamilacuisine.ro/budinca-de-dovlecei-cu-bacon-reteta-video/',
             'https://jamilacuisine.ro/dovlecei-cu-sos-de-smantana-reteta-video/']
    for link in links:
        scrapeRecipe(link)

    writeInJson(recipe)


main()


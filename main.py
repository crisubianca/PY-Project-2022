from bs4 import BeautifulSoup
import requests
from re import sub
import re
import json

directory = "recipes/"
# https://jamilacuisine.ro/dovlecei-pane-in-crusta-de-pesmet-si-in-aluat/

def snake_case(s):
    return '-'.join(
        sub('([A-Z][a-z]+)', r' \1',
            sub('([A-Z]+)', r' \1',
                s.replace('-', ' '))).split()).lower()

def scrapeRecipe():
    link = input("Insert you recipe here -> ")
    page = requests.get(link)
    # print("\nURL:", link)
    # print("******************")
    soup = BeautifulSoup(page.text, 'html.parser')

    recipe = {}

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

        all_ingredients = []
        
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

            # construim ingredientul
            ingredient = ingredient_amount_parsed + " " + ingredient_unit_parsed + " " + ingredient_name_parsed
            # adaugam ingredientul construit in lista de ingrediente
            all_ingredients.append(ingredient)

        #   reteta cu toate ingredientele
        recipe['recipeName'] = title
        recipe['ingredients'] = all_ingredients

    # similar pt retetele cu mai multe grupuri -> ex. vezi reteta cu dovlecei, are 2 : pt dovlecei in aluat/crusta de pesmet
    if len(ingredient_groups) > 1:

        for j in ingredient_groups:
            try:
                group_name = j.select('.wprm-recipe-group-name')[0].text.strip()
            except:
                return
            group_ingredients_unparsed = j.select('.wprm-recipe-ingredients > .wprm-recipe-ingredient')
            group_ingredients = []
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

                i = ingredient_amount_parsed + " " + ingredient_unit_parsed + " " + ingredient_name_parsed
                group_ingredients.append(i)

            recipe['recipeName'] = title.split("–")[0]
            recipe[group_name] = group_ingredients

    json_string = json.dumps(recipe, indent=4)
    with open(f"recipes/{snake_case(title)}", "w") as out_file:
        out_file.write(json_string)


scrapeRecipe()


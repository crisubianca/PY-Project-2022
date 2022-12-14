import requests
from bs4 import BeautifulSoup

directory = "testRecipes/"

def scrapeRecipe():
    link = input("Insert you recipe here -> ")
    recipesLinks = []
    page = requests.get(link)
    # pageSource = page.text
    # pageSource = pageSource.split('\n')
    print("\nURL:", link)
    print("******************")

    ingredients = []
    title = ""

    soup = BeautifulSoup(page.text, 'html.parser')
    titleText = soup.find_all("h1", {"class": "tdb-title-text"})
    for ti in titleText:
        # print(ti.text)
        title += ti.text

    ingred = soup.find_all("div", {"class": "wprm-recipe-ingredient-group"})
    for ing in ingred:
        ingredients.append(ing.text)

    print(title, "\n", ingredients, "\n")
    return title, ingredients

def writeInFile():
    title, ingredients = scrapeRecipe()
    # print(title, "\n", ingredients)
    fileName =  "shoppingCart.txt"
    # print(fileName)
    f = open(directory + fileName, 'w', encoding='utf-8')
    f.write(title + '\n')

    f.write("Ingrediente:\n")
    for i in ingredients:
        if i:
            f.write(i + '\n')

    f.close()

writeInFile()

import requests
from bs4 import BeautifulSoup
import re

directory = "recipes/"
# f = open(directory + "test.txt", 'w')
#
# f.write("test")
# f.close()
recipesLinksFile = "links.txt"
categories = ['aperitive', 'ciorbe-si-supe', 'conserve-muraturi', 'dulciuri', 'mancaruri', 'paine', 'salate', 'torturi',
              'diverse']


def getRecipesLinksByCategory(category):
    link = "https://jamilacuisine.ro/retete-video/" + category
    recipesLinks = []
    page = requests.get(link)
    # pageSource = page.text
    # pageSource = pageSource.split('\n')
    print("URL:", link)
    print("******************\n")

    soup = BeautifulSoup(page.text, 'html.parser')
    for line in soup.find_all("div", {"class": "tdb_module_loop td_module_wrap td-animation-stack td-cpt-post"}):
        # for line in soup.find_all("a"):
        #     data = line.get('href')
        #     print(str(data))
        result = re.search('(?<=href=").*?(?=" rel=)', str(line))
        recipesLinks.append(result.group())
        # print(result.group())
    # print(recipesLinks)

    return recipesLinks


def getRecipesLinks():
    recipesLinks = []

    for c in categories:
        recipesLinks.extend(getRecipesLinksByCategory(c))

    return recipesLinks


def writeLinks():
    recipesLinks = getRecipesLinks()
    f = open(directory + recipesLinksFile, 'w')

    for c in recipesLinks:
        f.write(c + '\n')

    f.close()


# recipeUsed = "https://jamilacuisine.ro/dovlecei-pane-in-crusta-de-pesmet-si-in-aluat/"
recipeUsed = "https://jamilacuisine.ro/ciorba-de-fasole-verde-de-post-reteta-video/"

def scrapeRecipe(recipeUsed):
    page = requests.get(recipeUsed)
    print("URL:", recipeUsed)
    print("******************\n")
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

    # print(title, "\n", ingredients)
    return title, ingredients

def writeInFile(recipeUsed):
    title, ingredients = scrapeRecipe(recipeUsed)
    # print(title, "\n", ingredients)
    fileName = title + ".txt"
    # print(fileName)
    f = open(fileName, 'w', encoding='utf-8')
    f.write(title + '\n')

    f.write("Ingrediente:\n")
    for i in ingredients:
        # print(i)
        f.write(i + '\n')

    f.close()




writeInFile(recipeUsed)

# scrapeRecipe(recipeUsed)
# getRecipesLinksByCategory('aperitive')
# writeLinks()

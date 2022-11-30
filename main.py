import requests

directory = "recipes/"
# f = open(directory + "test.txt", 'w')
#
# f.write("test")
# f.close()

categories = ['aperitive', 'ciorbe-si-supe', 'conserve-muraturi', 'dulciuri', 'mancaruri', 'paine', 'salate', 'torturi', 'diverse']

def getRecipesLinksByCategory(category):
    link = "https://jamilacuisine.ro/retete-video/" + category
    page = requests.get(link)
    pageSource = page.text
    pageSource = pageSource.split('\n')
    print("URL:", link)
    print("******************\n")

    for line in pageSource:
        if line.find("<div class=\"tdb_module_loop td_module_wrap td-animation-stack td-cpt-post\"") != -1:
            if line.find("<div class=\"td-module-container td-category-pos-\"") != -1:
                if line.find("<div class=\"td-image-container\"") != -1:
                    if line.find("<div class=\"td-module-thumb\"") != -1:
                        if line.find("<a href=\"https://jamilacuisine.ro/") != -1:
                            # line = line[26:]
                            # line = line[:len(line) - 274]
                            print(line)

def getRecipesLinks():
    recipesLinks= []

    for c in categories:
        recipesLinks.extend(getRecipesLinks(c))

    return recipesLinks

def writeLinks():
    recipesLinks = getRecipesLinks()
    f = open(directory + "links.txt", 'a')

    for c in categories:
        f.write(c + '\n')

    f.close()


getRecipesLinksByCategory('aperitive')


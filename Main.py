import requests
from bs4 import BeautifulSoup

url = "https://www.bbcgoodfood.com/recipes/"


class BBCGoodFoodAPI:

    def __init__(self, name):
        self.name = name
        self.soup = self.makeSoup()


    def sendRequest(self):
        response = requests.get(f"{url}/{self.name}")
        if response.status_code == 200:
            print("HTTP request successful")
        else:
            print("HTTP request unsuccessful\ncould not find URL")

        return response

    def getIngredientsFromHTML(self):


        all_ingredients = []

        ingredients_section_container = self.soup.find('div', class_='tabbed-list recipe__ingredients-nutrition')
        if ingredients_section_container:
            ingedient_lists = ingredients_section_container.find_all('ul', class_='ingredients-list list')

            for ul in ingedient_lists:
                parent_section = ul.find_parent('section')
                heading_tag = parent_section.find('h3', class_='ingredients-list__heading')
                if heading_tag:
                    all_ingredients.append(heading_tag.get_text(strip=True) + ":")

                for li_item in ul.find_all('li', class_='ingredients-list__item'):
                    ingredient_text = li_item.get_text(strip=True, separator=" ")
                    all_ingredients.append(ingredient_text)

        return all_ingredients

    def getMethodfromHTML(self):

        all_method_steps = []
        method_section_container = self.soup.find('section', class_='method-steps mb-lg')
        if method_section_container:

            method_header = method_section_container.find("h2", class_='method-steps__heading heading-3')
            method_list = method_section_container.find_all("ul", class_='method-steps__list')
            for ul in method_list:
                for method_list_item in ul.find_all('li', class_='method-steps__list-item'):
                    method_text = method_list_item.get_text(strip=True, separator=" ")
                    all_method_steps.append(method_text)

        return all_method_steps

    def printMethod(self):

        all_method_steps = self.getMethodfromHTML()

        for step in all_method_steps:
            print(step)

    def printIngredients(self):

        all_ingredients = self.getIngredientsFromHTML()

        for ingredient in all_ingredients:
            print(ingredient)

    def makeSoup(self):

        response = self.sendRequest()

        soup = BeautifulSoup(response.text, 'html.parser')

        return soup

    def printRating(self):

        rating_div = self.soup.find("div", class_='rating__values')
        if rating_div:
            ratings = rating_div.find_all("span", class_='sr-only')
            ratings_num = rating_div.find_all("span", class_='rating__count-text body-copy-small')
            if ratings:
                for rating in ratings:
                    rating_text = rating.get_text(strip=True, separator=" ")
                    print(rating_text)
            if ratings_num:
                for rating in ratings_num:
                    rating_text = rating.get_text(strip=True, separator=" ")
                    print(rating_text)

    def printDescription(self):

        div_container = self.soup.find("div", class_='editor-content body-copy-small')
        if div_container:
            print("container found")
            description = div_container.find_all("p")
            for description_item in description:
                description_text = description_item.get_text(strip=True, separator=" ")
                print(description_text)


    def pintAspects(self):

        details_headers = ["servings", "difficulty", "prep", "cook"]

        detailsDict = {

            "servings": "",
            "difficulty": "",
            "prep": "",
            "cook": ""

        }

        all_items = []

        div_container = self.soup.find("div", class_='post-header__body oflow-x-hidden post-header__body--recipe')
        if div_container:
            div_items = div_container.find_all("strong")
            if div_items:
                for item in div_items:
                    item_text = item.get_text(strip=True, separator=" ")
                    all_items.append(item_text)



        for i in range(4):
            detailsDict[details_headers[i]] = all_items[i]

        for i in range(4):
            print(detailsDict[details_headers[i]])


recipeInput = input()
recipeName = recipeInput.replace(" ", "-")
api = BBCGoodFoodAPI(recipeName)
api.printIngredients()
api.printMethod()
api.printRating()
api.printDescription()


api.pintAspects()

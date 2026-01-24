import requests
from bs4 import BeautifulSoup


class recipe:
    def __init__(self, title: str, macro: dict, cooking_time: float, number_of_portions: str, diet: list[str],
                 ingredients: list[str]):
        self.title = title
        self.macro = macro
        self.cooking_time = cooking_time
        self.number_of_portions = str(number_of_portions)
        self.diet = diet
        self.ingredients = ingredients

    def __repr__(self) -> str:
        return f"{self.title}:\nMacro: {self.macro}\nCzas gotowania: {self.cooking_time} minut\nLiczba porcji: {self.number_of_portions}\nDieta: {', '.join(self.diet)}\nSkładniki: {', '.join(self.ingredients)}"

    # Returns True if both class objects have the exact same attributes and values
    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False

        return self.__dict__ == other.__dict__


def create_soup(recipe_name: str) -> BeautifulSoup:
    """
    Sends an HTTP GET request to the aniagotuje urls and gets the site's content

    Args:
        recipe_name: name of the recipe that program appends to the base url

    Returns:
        BeautifulSoup: an object containing the parsed HTML of the recipe page
    """
    aniagotuje_url = "https://aniagotuje.pl/przepis/"
    response = requests.get(aniagotuje_url + recipe_name)
    response.raise_for_status()

    return BeautifulSoup(response.content, 'html.parser')


def get_recipe_info(soup: BeautifulSoup) -> tuple | str:
    """
    Parses the recipe page to extract portions, diet type, cooking time, and macros

    Args:
        soup: the BeautifulSoup object representing the parsed HTML of the recipe page

    Returns:
        tuple: collection of extracted data - portions (str), diet (list), cooking_time (int), macros (dict)
        str: message about an error
    """
    # Locates the main recipe info container in site's content
    recipe_info = soup.find('p', class_='recipe-info')
    if not recipe_info:
        return "Nie znaleziono informacji o przepisie"

    # Extracts clean text from recipe info container
    full_text = recipe_info.get_text(" ", strip=True)

    # Initializes default results structure
    results = {
        "portions": "Nie podano",
        "diet": [],
        "cooking_time": 0,
        "macros": {}
    }

    # Extracts cooking time
    if "Czas przygotowania:" in full_text:
        # Cuts out whats after "Czas przygotowania:" and before "Liczba porcji:"
        time_raw = full_text.split("Czas przygotowania:")[1].split("Liczba porcji:")[0].strip()
        parts = time_raw.split()
        # If there's a numeric value
        if parts[0].isdigit():
            val = int(parts[0])
            # If it's about hours ("godzina"/"godziny/"godzin"), it turns this value into minutes (x * 600)
            if "godz" in time_raw:
                results["cooking_time"] = val * 60
            else:
                results["cooking_time"] = val

    # Extracts portions
    if "Liczba porcji:" in full_text:
        # Cuts out whats after "Liczba porcji:" and before "W 100"
        results["portions"] = full_text.split("Liczba porcji:")[1].split("W 100")[0].strip()

    # Extracts diet type
    if "Dieta:" in full_text:
        # Cuts out whats after "Dieta:"
        diet_val = full_text.split("Dieta:")[1].strip()
        if diet_val:
            # Splits string into list elements (e.g. 'bezglutenowa, wegańska' -> ['bezglutenowa', 'wegańska'])
            results["diet"] = [d.strip().lower() for d in diet_val.split(',') if d.strip()]
        else:
            # Sets diet to standard value, if there's nothing after "Diet:"
            results["diet"] = ["standardowa"]
    else:
        # Sets diet to standard value, if there's no "Diet:" info on the site
        results["diet"] = ["standardowa"]

    # Macronutrients (structured approach using itemprop attributes)
    macro_map = {
        'calories': 'Kalorie (kcal)',
        'carbohydrateContent': 'Węglowodany (g)',
        'sugarContent': 'Cukry (g)',
        'proteinContent': 'Białko (g)',
        'fatContent': 'Tłuszcze (g)'
    }

    for item_prop, label in macro_map.items():
        # Find specific meta-tags or spans based on Schema.org microdata
        element = soup.find(attrs={"itemprop": item_prop})
        if element:
            raw_text = element.get_text(strip=True)
            # Split to separate the number from the unit
            parts = raw_text.split(" ")

            if len(parts) > 0:
                # aniagotuje site uses commas for decimals, so the program converts it to dots for float compatibility
                first_part = parts[0].replace(",", ".")

                try:
                    value = float(first_part)
                    results["macros"][label] = value
                except ValueError:
                    # Sets dict value to 0 if there's an error in data parsing
                    results["macros"][label] = 0

    return results["portions"], results["diet"], results["cooking_time"], results["macros"]


def get_recipe_ingredients(soup: BeautifulSoup) -> str | list[str]:
    """
    Parses the recipe page to extract ingredients

    Args:
        soup: the BeautifulSoup object representing the parsed HTML of the recipe page

    Returns:
        list: extracted ingredients data
        str: message about an error
    """
    items = soup.find_all(attrs={"itemprop": "recipeIngredient"})
    if not items:
        return "Nie znaleziono informacji o składnikach przepisu"

    # Processes each found element into a clean list element
    ingredients_list = [item.get_text(" ", strip=True) for item in items]

    return ingredients_list


def get_recipe_title(soup: BeautifulSoup) -> str | None:
    """
    Parses the recipe page to extract title

    Args:
        soup: the BeautifulSoup object representing the parsed HTML of the recipe page

    Returns:
        str: extracted title data or a message about an error
    """
    # Searches for a h1 tag with Schema.org 'itemprop="name"' attribute
    title_tag = soup.find('h1', attrs={'itemprop': 'name'})

    # If title_tag is None, searches for a generic h1 tag
    if not title_tag:
        title_tag = soup.find('h1')
        # If title_tag is still None, returns an error message
        if not title_tag:
            return "Nie znaleziono informacji o tytule przepisu"

    return title_tag.get_text(strip=True)


def get_recipe(recipe_name: str) -> recipe:
    """
    Combines the scraping process to create a new recipe object

    Args:
        recipe_name: name of the recipe used to build the target url

    Returns:
        recipe: class object for the given recipe
    """
    soup = create_soup(recipe_name)

    number_of_portions, diet, cooking_time, macro = get_recipe_info(soup)
    ingredients = get_recipe_ingredients(soup)
    title = get_recipe_title(soup)

    return recipe(title, macro, cooking_time, number_of_portions, diet, ingredients)



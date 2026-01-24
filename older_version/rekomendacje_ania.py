import csv
import requests
import os
from bs4 import BeautifulSoup


cookbook = []

def validate_number(message: str) -> int:
    """
    Gets the numeric input and checks if it's correct, so if it's an integer and if it's higher than zero.

    Args:
        message: message that the user gets while asked for input

    Returns:
        int:  validated value given by the user
    """
    while True:
        try:
            value = int(input(message).strip())
            if value <= 0:
                print("Błąd: Wartość musi być większa od zera.")
                continue
            return value

        except ValueError:
            print("Błąd: Podana wartość musi być liczbą.")


def validate_selection(message: str, possible_options: list[str]) -> str:
    """
    Gets the user's chosen option and checks if it's correct, so if it's in the list of possible options.

    Args:
        message: message that the user gets while asked for input

    Returns:
        str:  validated option given by the user
    """
    while True:
        wybor = input(f"{message} ({'/'.join(possible_options)}): ").strip().lower()
        if wybor in possible_options:
            return wybor

        print(f"Błąd: Wybierz jedną z opcji: {'/'.join(possible_options)}")


def get_users_input() -> tuple:
    """
    Gets and validates all of the user's inputs needed for all the program's calculations.

    Args:

    Returns:
        tuple:  all of the user's inputs
    """
    sex = validate_selection("Podaj swoją płeć", ['k', 'm'])
    age = validate_number("Podaj swój wiek: ")
    weight = validate_number("Podaj swoją wagę (kg): ")
    height = validate_number("Podaj swój wzrost (cm): ")

    # Connects options to numeric values, so it gets easier for the user to type in their activity level
    act_levels = {
        '1': "Brak ćwiczeń",
        '2': "Lekka aktywność (1-3 dni)",
        '3': "Umiarkowana (3-5 dni)",
        '4': "Duża (6-7 dni)"
    }

    print(
        "\nPoziomy aktywności: 1. Brak ćwiczeń, 2. Lekka aktywność (1-3 dni), 3. Umiarkowana (3-5 dni), 4. Duża (6-7 dni)")
    act_index = validate_selection("Wybierz poziom aktywności (numer)", ['1', '2', '3', '4'])
    phys_act = act_levels[act_index]
    diet_type = validate_selection("Podaj typ diety", ['bezglutenowa', 'wegańska', 'wegetariańska', 'standardowa'])
    goal = validate_selection("Podaj swój cel", ['przytyć', 'schudnąć', 'utrzymać wagę'])

    return sex, age, weight, height, phys_act, diet_type, goal


class recipe:
    def __init__(self, title: str, macro: dict, cooking_time: float, number_of_portions: str, diet: list[str],
                 ingredients: list[str]):
        self.title = title
        self.macro = macro
        self.cooking_time = cooking_time
        self.number_of_portions = str(number_of_portions)
        self.diet = diet
        self.ingredients = ingredients
        cookbook.append(self) if self not in cookbook else None

    def __repr__(self) -> str:
        return f"{self.title}:\nMacro: {self.macro}\nCzas gotowania: {self.cooking_time} minut\nLiczba porcji: {self.number_of_portions}\nDieta: {', '.join(self.diet)}\nSkładniki: {', '.join(self.ingredients)}"

    # Returns True if both class objects have the exact same attributes and values
    def __eq__(self, other):
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


def find_best_match(cookbook: list, goals: dict, target_diet: str = 'standardowa') -> recipe | None:
    """
    Finds the most suitable recipe based on nutritional goals and dietary preferences.

    It uses a weighted sum of squared differences to calculate a 'distance' score.
    The recipe with the lowest score is returned

    Args:
        cookbook: list of recipe objects
        goals: dictionary containing target values for calories, carbs, sugar, protein, and fat
        target_diet: diet type to filter by -'standardowa' by default

    Returns:
        recipe: class object that best matches the provided goals
        None: if no match is found
    """
    best_recipe = None
    # Initializes with infinity so any first valid recipe will have a lower score
    min_score = float('inf')

    # Links internal goal keys to the keys used in the recipe macro dictionary (like {macro_goal : self.macro[smth]})
    macro_map = {
        'calories': 'Kalorie (kcal)',
        'carbs': 'Węglowodany (g)',
        'sugar': 'Cukry (g)',
        'protein': 'Białko (g)',
        'fat': 'Tłuszcze (g)'
    }

    # Normalize the scale differences with weights (calories are hundreds, macros are tens)
    weights = {
        'calories': 0.1,
        'carbs': 1.0,
        'sugar': 1.0,
        'protein': 1.0,
        'fat': 1.0
    }

    for recipe in cookbook:
        # Checks if the user has diet type other than 'standardowa'
        if target_diet != 'standardowa':
            # If so, then checks if the user's diet type is in recipe description.
            # If not, then it goes to the next recipe
            if target_diet not in recipe.diet:
                continue

        score = 0
        for goal_key, macro_key in macro_map.items():
            # Gets values as floats for mathematical operations
            val = float(recipe.macro.get(macro_key, 0))
            goal = float(goals[goal_key])

            # Weighted Least Squares formula: (goal - actual) * weight, then squared
            diff = (goal - val) * weights[goal_key]
            score += diff ** 2

        # If this recipe's total score is lower than the current minimum, it becomes the new best match
        if score < min_score:
            min_score = score
            best_recipe = recipe

    return best_recipe





# Example code that could be in main.py

# recipies_base = load_recipes_from_file("recipes.csv")

# for recipe_name in recipies_base:
#     get_recipe(recipe_name)
#
# # imagine it's the result of calculations in other part of the project
# my_goals = {
#     'calories': 250,
#     'carbs': 10,
#     'sugar': 7,
#     'protein': 12,
#     'fat': 25
# }
#
# match = find_best_match(cookbook, my_goals)
# print(f"Najlepszy dopasowany przepis to: {match.title}")
# print(f"Jego makro: {match.macro}")
# # maybe ask if the user wants to see the ingredients needed for this recipe?
# # or let him skip this recipe and show the second best recipe? or top5?
#
# my_goals = {
#     'calories': 250,
#     'carbs': 10,
#     'sugar': 7,
#     'protein': 12,
#     'fat': 25
# }
#
# match = find_best_match(cookbook, my_goals, "wegańska")
# print(f"Najlepszy dopasowany przepis to: {match.title}")
# print(f"Jego makro: {match.macro}")
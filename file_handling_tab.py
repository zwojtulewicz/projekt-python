import os
import csv
import streamlit as st

from aniagotuje_scraping import *


def load_recipes_from_file(filename="recipes.csv") -> list:
    """
    Loads recipe list from the CSV file. If the file doesn't exist, returns an empty list.

    Args:
        filename: name of the file with recipes, by default it should be 'recipes.csv' (pre-made recipe list)

    Returns:
        list:  list of all the recipes that the file contains
    """
    recipes = []

    # Checks if the path to a file exists, if not - then returns an empty list
    if not os.path.exists(filename):
        return recipes

    try:
        with open(filename, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                # Checks if a line in the file is not empty
                if row:
                    # Gets the first value in the row and adds it to the list
                    recipes.append(row[0].strip())
    except Exception as e:
        print(f"Nieoczekiwany błąd podczas wczytywania pliku: {e}")

    return recipes


def add_recipe_to_file(recipe_url_name: str, filename='recipes.csv') -> str | None:
    """
    Adds recipe to the CSV file. If the file doesn't exist, returns an empty list.

    Args:
        recipe_url_name: name of the recipe taken from aniagotuje url, that user tries to add to the file
        filename: name of the file with recipes, by default it should be 'recipes.csv' (pre-made recipe list)

    Returns:
        None: function returns a None value, if the recipe already is in the file, or prints out a success
                message or an error message
    """
    recipe_url_name = recipe_url_name.strip().lower()

    # Checks if the user's recipe already exists in the csv file
    if recipe_url_name in load_recipes_from_file(filename):
        print(f"Wpis '{recipe_url_name}' już istnieje w pliku.")
        return "Przepis już istnieje w bazie"

    try:
        # If create_soup() raises an error, recipe won't be added to the csv file
        soup = create_soup(recipe_url_name)

        # Appends recipe name to the csv file
        with open(filename, 'a', encoding='utf-8', newline='') as f:
            csv.writer(f).writerow([recipe_url_name])

        return "SUCCESS"

    # Handles the errors raised by create_soup()
    except requests.exceptions.HTTPError:
        raise Exception("Błąd: Strona dla Twojego przepisu nie istnieje.")
    except requests.exceptions.ConnectionError:
        raise Exception("Błąd: Problem z połączeniem internetowym.")
    except Exception as e:
        raise Exception(f"Nieoczekiwany błąd: {e}")


def remove_recipe_from_file(recipe_url_name: str, filename='recipes.csv') -> None:
    """
    Removes recipe from the CSV file. If the file doesn't exist, returns an empty list.

    Args:
        recipe_url_name: name of the recipe taken from aniagotuje url, that user tries to remove from the file
        filename: name of the file with recipes, by default it should be 'recipes.csv' (pre-made recipe list)

    Returns:
        None: function doesn't return a value, but it prints out a success message or an error message
    """
    recipe_url_name = recipe_url_name.strip().lower()
    recipes = load_recipes_from_file(filename)

    if recipe_url_name in recipes:
        soup = create_soup(recipe_url_name)
        title = get_recipe_title(soup)

        # Removes the user's recipe from the recipe list
        recipes.remove(recipe_url_name)
        # Clears the file and writes down modificated recipe list (there's no an easier way to do this)
        with open(filename, "w", encoding="utf-8", newline='') as f:
            writer = csv.writer(f)
            for recipe in recipes:
                writer.writerow([recipe])

        print(f"Usunięto {title}")
    else:
        print(f"Nie znaleziono {recipe_url_name}")

def add_recipe_st_version(new_recipe_name, file):
    if new_recipe_name:
        try:
            # Próbujemy dodać przepis
            result = add_recipe_to_file(new_recipe_name, file)

            if result == "SUCCESS":
                st.success(f"Pomyślnie dodano przepis!")
                st.rerun()  # Odświeżamy listę tylko przy sukcesie
            else:
                # To obsłuży przypadek, gdy przepis już istnieje
                st.warning(result)

        except Exception as e:
            # Tutaj Streamlit wyświetli błąd ze strony AniaGotuje na czerwono
            st.error(str(e))
    else:
        st.error("Proszę wpisać nazwę przepisu!")
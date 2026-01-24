from aniagotuje_scraping import *
from file_handling_tab import load_recipes_from_file


def create_cookbook(filename: str = "recipes.csv") -> list:
    """
    Fetches and initializes recipe objects based on slugs stored in a file.

    Args:
        filename (str): The path to the file containing recipe slugs. Defaults to "recipes.csv".

    Returns:
        list: A list of successfully initialized recipe objects. Returns an empty
        list if the file is empty or no recipes could be retrieved.

    Raises:
        FileNotFoundError: If the specified filename does not exist (handled by  load_recipes_from_file).
    """
    recipe_slugs = load_recipes_from_file(filename)

    all_recipes = []

    if not recipe_slugs:
        return all_recipes

    for slug in recipe_slugs:
        try:
            recipe_obj = get_recipe(slug)
            all_recipes.append(recipe_obj)
        except Exception as e:
            print(f"Pominięto '{slug}': błąd pobierania ({e})")
            continue

    return all_recipes


def find_best_match(cookbook, user, goals, exclude: list = None, multiplier=3.0) -> object | None:
    """
    Finds the recipe that best matches (least squares method) the user's nutritional goals using a weighted score.

    Args:
        cookbook (list): List of recipe objects to search through.
        user (object): User object containing diet_type and other profile data.
        goals (dict): Dictionary of target nutritional values (e.g., {'calories': 500}).
        exclude (list, optional): List of recipe objects to skip. Defaults to None.
        multiplier (float, optional): Factor to scale 100g macro values to portion size.
            Defaults to 3.0 (300g).

    Returns:
        object | None: The recipe object with the lowest error score, or None if no
            match is found.
    """
    best_recipe = None
    min_score = float('inf')
    exclude = exclude or []

    # Maps internal goal keys to the specific keys used in recipe macro dictionaries
    mapping = {
        'calories': 'Kalorie (kcal)',
        'protein': 'Białko (g)',
        'fat': 'Tłuszcze (g)',
        'carbs': 'Węglowodany (g)',
        'sugar': 'Cukry (g)'
    }

    # Defines importance weights: higher values make deviations more "punishing"
    weights = {
        'Kalorie (kcal)': 0.1,
        'Węglowodany (g)': 1.0,
        'Białko (g)': 2.0,  # Protein is prioritized
        'Tłuszcze (g)': 1.0
    }

    # Normalizes user diet types to lowercase for robust comparison
    user_diets = [d.lower() for d in (user.diet_type if isinstance(user.diet_type, list) else [user.diet_type])]

    for recipe in cookbook:
        # Skips recipes already added to the daily plan or temporarily rejected
        if recipe in exclude:
            continue

        # Filters by diet: skips if recipe tags don't match user preferences (unless standard)
        if 'standardowa' not in user_diets:
            recipe_tags = [d.lower() for d in getattr(recipe, 'diet', [])]
            if not any(diet in recipe_tags for diet in user_diets):
                continue

        score = 0
        found_any_macro = False

        for goal_key, goal_val in goals.items():
            # Matches goal key to recipe key (direct match or via mapping)
            recipe_key = goal_key if goal_key in recipe.macro else mapping.get(goal_key)

            if recipe_key and recipe_key in recipe.macro:
                found_any_macro = True
                # Scales the 100g value to the actual portion size
                actual_val = float(recipe.macro.get(recipe_key, 0)) * multiplier

                w = weights.get(recipe_key, 1.0)

                # Uses squared difference to penalize larger deviations non-linearly
                diff = float(goal_val) - actual_val
                score += (diff ** 2) * w

        # Updates best match if the current recipe has a lower error score
        if found_any_macro and score < min_score:
            min_score = score
            best_recipe = recipe

    return best_recipe
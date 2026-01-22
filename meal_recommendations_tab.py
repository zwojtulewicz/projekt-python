from aniagotuje_scraping import *
from bmr_tdee_tab import calculate_tdee
from file_handling_tab import load_recipes_from_file
from macros_tab import macros


def create_cookbook(filename: str = "recipes.csv") -> list:
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


def find_best_match(cookbook, user, exclude: list = None, multiplier = 3.0) -> recipe | None:
    best_recipe = None
    min_score = float('inf')
    exclude = exclude or []

    weights = {
        'calories': 0.1,
        'carbs': 1.0,
        'protein': 1.5,  # proteins are more important to us than other macros
        'fat': 1.0
    }

    for recipe in cookbook:
        if recipe in exclude:
            continue

        if isinstance(user.diet_type, list):
            user_diets = [d.lower() for d in user.diet_type]
        else:
            user_diets = [user.diet_type.lower()]

        for recipe in cookbook:
            if recipe in exclude:
                continue

            if 'standardowa' not in user_diets:
                recipe_tags = [d.lower() for d in recipe.diet]

                # Sprawdzamy, czy którakolwiek z diet użytkownika jest w tagach przepisu
                # any(...) zwróci True, jeśli znajdzie chociaż jedno dopasowanie
                if not any(diet in recipe_tags for diet in user_diets):
                    continue

        score = 0

        goals = {"calories": calculate_tdee(user), **macros(user, calculate_tdee(user))}

        for key, goal_val in goals.items():
            if key in recipe.macro:
                val_per_100g = float(recipe.macro.get(key, 0))

                # changing the weight, because you dont eat every meal in 100g portion lmao
                actual_val = val_per_100g * multiplier
                w = weights.get(key, 1.0)

                diff = float(goal_val) - actual_val
                score += (diff ** 2) * w

        if score < min_score:
            min_score = score
            best_recipe = recipe

    return best_recipe

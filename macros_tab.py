# definiuje proporcje makroskładników w zależności od celu
def macros(user, tdee_value):
    if user.target == "lose":
        p_ratio, f_ratio, c_ratio = 0.30, 0.25, 0.45
    elif user.target == "gain":
        p_ratio, f_ratio, c_ratio = 0.20, 0.20, 0.60
    else:
        p_ratio, f_ratio, c_ratio = 0.20, 0.30, 0.50

    # kalkulacja zapotrzebowania na konkretną gramaturę makroskładników
    proteins = (tdee_value * p_ratio) / 4
    fats = (tdee_value * f_ratio) / 9
    carbs = (tdee_value * c_ratio) / 4
    return {
        "Białko (g)": round(proteins),
        "Tłuszcze (g)": round(fats),
        "Węglowodany (g)": round(carbs)
    }

    # funkcja zwraca zalecenia odnośnie mikroskładników w zależności od wybranego celu


def minerals(user):
    if user.target == "lose":
        return "Monitoruj poziom magnezu, witamin z grupy B, żelaza i jodu ze względu na deficyt kaloryczny."
    elif user.target == "gain":
        return "Monitoruj cynk, wapń, witaminę D, potas i sód."
    else:
        return "Dla zdrowej diety monitoruj magnez, potas, witaminy B i D oraz kwasy OMEGA-3."


# funkcja rekomenduje konkretne produkty szczególnie bogate w dane makroskładniki

def recommendations(user):
    protein_list = ["kurczak", "indyk", "chuda wołowina", "ryby", "jajka", "twaróg", "jogurt grecki",
                    "soczewica", "quinoa", "fasola", "ciecierzyca", "tofu"]
    fat_list = ["oliwa", "orzechy (migdały, włoskie)", "awokado", "nasiona chia", "pestki dyni", "ryby morskie"]
    carb_list = ["kasze", "brązowy ryż", "owies", "chleb pełnoziarnisty", "makaron pełnoziarnisty", "ziemniaki",
                 "bataty", "owoce", "warzywa"]

    # restrykcje żywieniowe - w zależności od wyboru użytkownika usuwa nietolerowane produkty z listy rekomendacji

    if "wegańska" in user.diet_type:
        forbidden = ["kurczak", "indyk", "chuda wołowina", "ryby", "jajka", "twaróg", "jogurt grecki",
                     "ryby morskie"]
        protein_list = [p for p in protein_list if p not in forbidden]
        fat_list = [p for p in fat_list if p not in forbidden]
    elif "wegetariańska" in user.diet_type:
        forbidden = ["kurczak", "indyk", "chuda wołowina", "ryby", "ryby morskie"]
        protein_list = [p for p in protein_list if p not in forbidden]
        fat_list = [p for p in fat_list if p not in forbidden]
    if "bezglutenowa" in user.diet_type:
        gluten = ["owies", "chleb pełnoziarnisty", "makaron pełnoziarnisty"]
        carb_list = [p for p in carb_list if p not in gluten]
        carb_list.extend(["chleb bezglutenowy", "makaron kukurydziany/ryżowy", "płatki jaglane"])

    return {"Białka": ", ".join(protein_list), "Tłuszcze": ", ".join(fat_list),
            "Węglowodany": ", ".join(carb_list)}

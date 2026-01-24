from input_handling import *
from input_tab import *
from bmi_tab import *
from bmr_tdee_tab import *
from macros_tab import *
from file_handling_tab import *
from meal_recommendations_tab import *

@st.cache_data
def load_cookbook_cached(filename):
    return create_cookbook(filename)

if __name__ == "__main__":
    st.title("🌱 Asystent Zdrowego Żywienia")  # tytuł aplikacji
    st.write("Witaj w kompleksowym systemie wsparcia dietetycznego.")  # podtytuł/pierwszy komunikat dla użytkownika

    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'filename' not in st.session_state:
        st.session_state.filename = "recipes.csv"

    # Zdefiniowanie wspólnych zakładek dla wszystkich funkcjonalności
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Wczytanie danych", "Kalkulator BMI",
                                                  "Kalkulator BMR/TDEE", "Planer Dietetyczny",
                                                  "Obsługa pliku", "Rekomendacja posiłków"])

    with tab1:
        st.header("Wczytanie danych")  # ustawia nagłówek
        col_z1, col_z2 = st.columns(2)  # dzieli ekran na kolumny

        # zawartość 1 kolumny (lista rozwijana z płcią, pole numeryczne do wieku, wzrostu i wagi)
        with col_z1:
            gender_val, age_z, height_z, weight_z = st_input_col1()

        # zawartość 2 kolumny (słownik z opcjami aktywności i ich wartościami ze wzoru matematycznego oraz wybór celu)
        with col_z2:
            activity_val, target_val, lifestyle = st_input_col2()

        diet_type = st.multiselect("Typ diety", ["bezglutenowa", "wegetariańska",
                                                 "wegańska", "standardowa"], key="z_restr")  # lista wyboru typów diet

        if st.button("Zatwierdź wprowadzone dane", type="primary", key="btn_zuzia"):  # przycisk uruchamiający kod
            try:
                # tworzenie obiektu klasy User
                st.session_state.user = User(
                    gender=gender_val,
                    age=int(age_z),
                    weight=weight_z,
                    height=int(height_z),
                    activity=activity_val,
                    diet_type=diet_type,
                    lifestyle=lifestyle,
                    target=target_val
                )  # przekazanie danych do klasy, sprawdzenie czy nie ma errorów

            except ValueError as e:
                st.error(f"Błąd danych: {e}")

    with tab2:
        st.header("Kalkulator BMI")

        if st.session_state.user is not None:
            user = st.session_state.user

            if st.button("Oblicz moje BMI"):  # uwtorzenie przycisku do wywołania dalszej części kodu
                bmi = calculate_bmi(user)

                st.metric(label="Twoje BMI wynosi", value=f"{bmi:.2f}")
                interpret_bmi(bmi)
        else:
            # Ten komunikat pojawi się tylko, jeśli użytkownik nie zatwierdził danych w tab1
            st.info("Najpierw uzupełnij i zatwierdź dane w zakładce 'Wczytanie danych'")

    with tab3:
        st.header("Kalkulator BMR/TDEE")

        if st.session_state.user is not None:
            user = st.session_state.user

            if st.button("Oblicz BMR i TDEE"):
                bmr_val = calculate_bmr_simple(user)
                tdee_val = calculate_tdee(user)

                st.divider()
                col_res1, col_res2 = st.columns(2)
                col_res1.metric("Podstawowa przemiana materii:", f"{bmr_val:.2f} kcal")
                col_res2.metric("Całkowite dzienne zapotrzebowanie kaloryczne:", f"{tdee_val:.2f} kcal")
        else:
            # Ten komunikat pojawi się tylko, jeśli użytkownik nie zatwierdził danych w tab1
            st.info("Najpierw uzupełnij i zatwierdź dane w zakładce 'Wczytanie danych'")

    with tab4:
        st.header("Planer Dietetyczny")

        if st.session_state.user is not None:
            user = st.session_state.user

            if st.button("Planer Dietetyczny"):
                tdee_val = calculate_tdee(user)  # wywołuje funkcję kalkulatora tdee z klasy User

                st.markdown("---")  # linia oddzielająca formularz od wyników
                st.success(f"🥑 Twoje zapotrzebowanie (TDEE): **{int(tdee_val)} kcal**")  # wyświetla wynik

                st.write("Twoje dzienne zapotrzebowanie na mikroskładniki:")
                macros_res = macros(user, tdee_val)  # uruchamia metodę macros z klasy
                c1, c2, c3 = st.columns(3)  # dzieli ekran na 3 kolumny, gdzie wyświetlają się wyniki dla makro
                c1.metric("Białko", f"{macros_res['Białko (g)']} g")
                c2.metric("Tłuszcze", f"{macros_res['Tłuszcze (g)']} g")
                c3.metric("Węglowodany", f"{macros_res['Węglowodany (g)']} g")

                st.info(f"💡 Porada: {minerals(user)}")  # wyświetla poradę odnośnie mikroelementów

                with st.expander("Zobacz polecane produkty"):  # tworzy rozwijaną listę rekomendacji
                    recs_res = recommendations(user)  # pobiera listę rekomendowanych produktów z klasy
                    for k, v in recs_res.items():  # pętla przechodząca przez słownik z rekomendacjami
                        st.write(f"**{k}:** {v}")  # wypisuje zmienne w tekście (** - pogrubienie)
        else:
            # Ten komunikat pojawi się tylko, jeśli użytkownik nie zatwierdził danych w tab1
            st.info("Najpierw uzupełnij i zatwierdź dane w zakładce 'Wczytanie danych'")

    with tab5:
        st.header("Obsługa pliku")

        # Handles the file name input through a Streamlit form
        with st.form("file_settings"):
            temp_filename = st.text_input(
                "Podaj nazwę pliku csv z przepisami:",
                value=st.session_state.get('filename', ''),
                help="Wpisz nazwę i naciśnij Enter lub przycisk poniżej"
            )
            submit_file = st.form_submit_button("Zatwierdź plik")

        if submit_file:
            # Updates the session state with the provided filename
            st.session_state.filename = temp_filename

        # Manages the logic for loading the cookbook if the filename is valid
        if 'filename' in st.session_state and st.session_state.filename:
            current_file = st.session_state.filename

            # Checks if the cookbook needs to be reloaded from the disk
            if 'cookbook' not in st.session_state or st.session_state.get('last_loaded_file') != current_file:
                with st.spinner(f"Ładowanie przepisów z pliku {current_file}..."):
                    # Populates the cookbook object and updates the tracking variable
                    st.session_state.cookbook = create_cookbook(current_file)
                    st.session_state.last_loaded_file = current_file

            cookbook_data = st.session_state.cookbook
        else:
            st.warning("Proszę zatwierdzić nazwę pliku, aby kontynuować.")

        st.subheader("Dodaj nowy przepis")
        recipe_to_add = st.text_input("Wpisz nazwę przepisu (z URL):", key="add_input")

        if st.button("Zatwierdź dodawanie"):
            # Triggers the scraping and adding process for a new recipe
            add_recipe_st_version(recipe_to_add, current_file)

        st.subheader("Usuń przepis")
        recipe_slugs = load_recipes_from_file(current_file)

        if recipe_slugs:
            slug_to_remove = st.selectbox("Wybierz przepis do skasowania:", options=recipe_slugs)

            if st.button("Potwierdź usunięcie"):
                # Deletes the specified recipe and reloads the application state
                remove_recipe_from_file(slug_to_remove, current_file)
                st.success(f"Usunięto: {slug_to_remove}")
                st.rerun()
        else:
            st.info("Brak przepisów w bazie do usunięcia.")

        st.subheader("Twoja lista przepisów")
        all_slugs = load_recipes_from_file(current_file)

        if all_slugs:
            for slug in all_slugs:
                st.write(f"• {slug}")
        else:
            st.write("Lista jest obecnie pusta.")

    with tab6:
        st.header("Interaktywny Kreator Dnia")

        if st.session_state.user is not None:
            current_user = st.session_state.user

            # Verifies if daily plan variables exist in session state, otherwise initializes them
            if 'daily_plan' not in st.session_state:
                st.session_state.daily_plan = []
                st.session_state.temp_exclude = []
                st.session_state.remaining_goals = None
                st.session_state.meals_to_go = 0

            # Renders the initial configuration form for the daily plan
            if st.session_state.meals_to_go == 0:
                num_meals = st.number_input("Na ile posiłków podzielić dzień?", 2, 10, 3)
                if st.button("Zacznij planowanie dnia"):
                    tdee_value = calculate_tdee(current_user)
                    macro_requirements = macros(current_user, tdee_value)

                    # Establishes the starting nutritional budget based on user data
                    st.session_state.remaining_goals = {
                        'calories': tdee_value,
                        'carbs': macro_requirements.get("Węglowodany (g)", 0),
                        'protein': macro_requirements.get("Białko (g)", 0),
                        'fat': macro_requirements.get("Tłuszcze (g)", 0),
                        'sugar': macro_requirements.get("Cukry (g)", 50)
                    }
                    st.session_state.meals_to_go = num_meals
                    st.session_state.daily_plan = []
                    st.rerun()

            # Handles the active meal selection process
            if st.session_state.meals_to_go > 0:
                st.write(f"Pozostało posiłków do zaplanowania: {st.session_state.meals_to_go}")

                # Calculates requirements for the current specific meal slot
                meal_target = {
                    k: v / st.session_state.meals_to_go
                    for k, v in st.session_state.remaining_goals.items()
                }

                # Merges confirmed recipes and temporary skips for the exclusion filter
                exclusion_list = st.session_state.daily_plan + st.session_state.get('temp_exclude', [])

                # Invokes the matching algorithm to suggest the best recipe
                suggested_recipe = find_best_match(
                    st.session_state.cookbook,
                    current_user,
                    goals=meal_target,
                    exclude=exclusion_list
                )

                if suggested_recipe:
                    st.subheader(f"Propozycja posiłku nr {len(st.session_state.daily_plan) + 1}")

                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.markdown(f"### {suggested_recipe.title}")
                        st.write(f"Czas: {suggested_recipe.cooking_time} min")
                        st.write("Składniki:", ", ".join(suggested_recipe.ingredients))
                    with col2:
                        st.write("**Makra (w 100g):**")
                        st.json(suggested_recipe.macro)

                    btn_col1, btn_col2, btn_col3 = st.columns(3)

                    if btn_col1.button("Akceptuję", type="primary", use_container_width=True):
                        # Adds the chosen recipe to the daily plan and updates balance
                        st.session_state.daily_plan.append(suggested_recipe)

                        portion_multiplier = 3.0
                        mapping_dict = {
                            'calories': 'Kalorie (kcal)',
                            'carbs': 'Węglowodany (g)',
                            'protein': 'Białko (g)',
                            'fat': 'Tłuszcze (g)',
                            'sugar': 'Cukry (g)'
                        }

                        for internal_key, recipe_key in mapping_dict.items():
                            macro_value = float(suggested_recipe.macro.get(recipe_key, 0)) * portion_multiplier
                            # Subtracts the consumed nutrients from the remaining daily allowance
                            st.session_state.remaining_goals[internal_key] -= macro_value

                        st.session_state.temp_exclude = []
                        st.session_state.meals_to_go -= 1
                        st.rerun()

                    if btn_col2.button("Zaproponuj inny", use_container_width=True):
                        # Temporarily hides the current recipe from further suggestions
                        st.session_state.temp_exclude.append(suggested_recipe)
                        st.rerun()

                    if btn_col3.button("Resetuj plan", use_container_width=True):
                        # Clears all progress and returns to the initial state
                        st.session_state.meals_to_go = 0
                        st.session_state.daily_plan = []
                        st.session_state.temp_exclude = []
                        st.rerun()

            # Displays the final summary once all meals are planned
            if st.session_state.meals_to_go == 0 and len(st.session_state.daily_plan) > 0:
                st.success("Twój plan na dziś jest gotowy!")
                for idx, meal in enumerate(st.session_state.daily_plan, 1):
                    st.write(f"{idx}. {meal.title}")

                if st.button("Zaplanuj nowy dzień"):
                    st.session_state.daily_plan = []
                    st.rerun()

        else:
            st.info("Najpierw uzupełnij i zatwierdź dane w zakładce 'Wczytanie danych'")
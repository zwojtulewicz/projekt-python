from input_handling import *
from input_tab import *
from bmi_tab import *
from bmr_tdee_tab import *
from macros_tab import *
from file_handling_tab import *
from meal_recommendations_tab import *

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

        st.text_input(
            "Nazwa pliku z przepisami:",
            key="filename",  # Streamlit automatycznie synchronizuje to pole z st.session_state.filename
            help="Zmiana nazwy tutaj wpłynie na wszystkie operacje poniżej"
        )

        file = st.session_state.filename

        st.subheader("Dodaj nowy przepis")
        new_recipe_name = st.text_input("Wpisz nazwę przepisu (z URL):", key="add_input")

        if st.button("Zatwierdź dodawanie"):
            add_recipe_st_version(new_recipe_name, file)

        st.subheader("Usuń przepis")
        current_recipes = load_recipes_from_file(file)

        if current_recipes:
            recipe_to_remove = st.selectbox("Wybierz przepis do skasowania:", options=current_recipes)

            if st.button("Potwierdź usunięcie"):
                remove_recipe_from_file(recipe_to_remove, file)
                st.success(f"Usunięto: {recipe_to_remove}")
                st.rerun()
        else:
            st.info("Brak przepisów w bazie do usunięcia.")

        st.subheader("Twoja lista przepisów")
        recipes = load_recipes_from_file(file)

        if recipes:
            for r in recipes:
                st.write(f"• {r}")
        else:
            st.write("Lista jest obecnie pusta.")

    with tab6:
        st.header("🥗 Interaktywny Kreator Dnia")

        if st.session_state.user is not None:
            user = st.session_state.user
            cookbook = create_cookbook(file)

            # 1. Inicjalizacja sesji dla rekomendacji
            if 'daily_plan' not in st.session_state:
                st.session_state.daily_plan = []
                st.session_state.remaining_goals = None
                st.session_state.meals_to_go = 0

            # Formularz startowy
            if st.session_state.meals_to_go == 0:
                num_meals = st.number_input("Na ile posiłków podzielić dzień?", 2, 10, 3)
                if st.button("Zacznij planowanie dnia"):
                    tdee = calculate_tdee(user)
                    m_goals = macros(user, tdee)


                    # Ustawiamy cele początkowe używając POLSKICH kluczy z Twojej funkcji
                    st.session_state.remaining_goals = {
                        'calories': tdee,
                        'carbs': m_goals.get("Węglowodany (g)", 0),
                        'protein': m_goals.get("Białko (g)", 0),
                        'fat': m_goals.get("Tłuszcze (g)", 0),
                        'sugar': m_goals.get("Cukry (g)", 50)  # Jeśli macros nie liczy cukru, zostawiamy 50g
                    }
                    st.session_state.meals_to_go = num_meals
                    st.session_state.daily_plan = []
                    st.rerun()

            # 2. Proces rekomendacji
            if st.session_state.meals_to_go > 0:
                st.write(f"Pozostało posiłków do zaplanowania: **{st.session_state.meals_to_go}**")

                # Obliczamy cel dla TEGO konkretnego posiłku
                current_meal_target = {
                    k: v / st.session_state.meals_to_go
                    for k, v in st.session_state.remaining_goals.items()
                }

                # Szukamy przepisu
                # (Pamiętaj, aby cookbook był dostępny w zasięgu)
                rec = find_best_match(
                    cookbook,
                    user,
                    exclude=st.session_state.daily_plan
                )

                if rec:
                    st.subheader(f"Propozycja posiłku nr {len(st.session_state.daily_plan) + 1}")
                    st.info(f"Szukaliśmy posiłku o parametrach: {current_meal_target['calories']:.0f} kcal")

                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.markdown(f"### {rec.title}")
                        st.write(f"⏱ Czas: {rec.cooking_time} min")
                        st.write("**Składniki:**", ", ".join(rec.ingredients))
                    with col2:
                        st.write("**Makra (w 100g):**")
                        st.json(rec.macro)

                    # PRZYCISKI AKCJI
                    c1, c2 = st.columns(2)
                    if c1.button("✅ Akceptuję, podaj następny", type="primary"):
                        # Aktualizujemy stan
                        st.session_state.daily_plan.append(rec)
                        # Odejmujemy (zakładając porcję np. 300g jak wcześniej ustaliliśmy)
                        multiplier = 3.0
                        for key, macro_name in {'calories': 'Kalorie (kcal)', 'carbs': 'Węglowodany (g)',
                                                'protein': 'Białko (g)', 'fat': 'Tłuszcze (g)',
                                                'sugar': 'Cukry (g)'}.items():
                            val = float(rec.macro.get(macro_name, 0)) * multiplier
                            st.session_state.remaining_goals[key] -= val

                        st.session_state.meals_to_go -= 1
                        st.rerun()

                    if c2.button("🔄 Losuj inny"):
                        st.toast("Szukam innej opcji...")  # W tej wersji Greedy zawsze znajdzie to samo,
                        # chyba że dodasz element losowości

                if st.button("❌ Resetuj plan"):
                    st.session_state.meals_to_go = 0
                    st.rerun()

            # 3. Podsumowanie końcowe
            if st.session_state.meals_to_go == 0 and len(st.session_state.daily_plan) > 0:
                st.success("🎉 Twój plan na dziś jest gotowy!")
                for i, m in enumerate(st.session_state.daily_plan, 1):
                    st.write(f"{i}. {m.title}")

                if st.button("Zaplanuj nowy dzień"):
                    st.session_state.daily_plan = []
                    st.rerun()

        else:
            st.info("Najpierw uzupełnij i zatwierdź dane w zakładce 'Wczytanie danych'")
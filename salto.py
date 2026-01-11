import streamlit as st
import pandas as pd
import requests
import zipfile
import io

# ==========================================
# CZĘŚĆ LOGICZNA (KLASY I FUNKCJE)
# ==========================================

# Klasa User (Logika Julki/Ogólna)
class User:
    def __init__(self, gender, age, weight, height, activity, restrictions, target):
        self._gender = gender
        self._age = age
        self._weight = weight
        self._height = height
        self.activity = activity
        self.restrictions = [r.casefold() for r in restrictions]
        self._target = target

    @property
    def gender(self):
        return self._gender

    @property
    def age(self):
        return self._age

    @property
    def weight(self):
        return self._weight

    @property
    def height(self):
        return self._height

    @property
    def target(self):
        return self._target

    def bmr(self):
        # Wzór Mifflina-St Jeora
        if self.gender == "kobieta":
            return (10 * self.weight) + (6.25 * self.height) - (5 * self.age) - 161
        else:
            return (10 * self.weight) + (6.25 * self.height) - (5 * self.age) + 5

    def tdee(self):
        tdee_val = self.bmr() * self.activity   
        if self.target == "schudnąć":
            return round(tdee_val - 500)
        elif self.target == "przytyć":
            return round(tdee_val + 500)
        else: # utrzymać wagę
            return round(tdee_val)
        
    def macros(self):
        cal = self.tdee()
        if self.target == "schudnąć":
            p_ratio, f_ratio, c_ratio = 0.30, 0.25, 0.45
        elif self.target == "przytyć":
            p_ratio, f_ratio, c_ratio = 0.20, 0.20, 0.60
        else:
            p_ratio, f_ratio, c_ratio = 0.20, 0.30, 0.50
        
        proteins = (cal * p_ratio) / 4
        fats = (cal * f_ratio) / 9
        carbs = (cal * c_ratio) / 4
        
        return {
            "Białko (g)": round(proteins),
            "Tłuszcze (g)": round(fats),
            "Węglowodany (g)": round(carbs)
        }

    def minerals(self):
        if self.target == "schudnąć":
            return "Monitoruj poziom magnezu, witamin z grupy B, żelaza i jodu ze względu na deficyt kaloryczny."
        elif self.target == "przytyć":
            return "Monitoruj poziom cynku, wapnia, witaminy D, potasu i sodu."
        else:
            return "Dla zbilansowanej diety monitoruj magnez, potas, witaminy B i D oraz kwasy OMEGA-3."

    def recs(self):
        return {
            "Białko": "chude mięso (kurczak, indyk), ryby, jajka, twaróg, jogurt grecki, soczewica, tofu",
            "Tłuszcze": "oliwa z oliwek, orzechy, awokado, nasiona chia, ryby morskie",
            "Węglowodany": "kasza gryczana/jaglana, ryż brązowy, płatki owsiane, pieczywo pełnoziarniste, owoce, warzywa"
        }

# Funkcja Ani - Pobieranie danych GIOS
def download_gios_archive(year, gios_id, filename):
    gios_archive_url = "https://powietrze.gios.gov.pl/pjp/archives/downloadFile/"
    url = f"{gios_archive_url}{gios_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            with z.open(filename) as f:
                # Header=0 oznacza, że pierwszy wiersz to nagłówki
                df = pd.read_excel(f, header=0) 
        return df
    except Exception as e:
        st.error(f"Wystąpił błąd podczas pobierania danych: {e}")
        return None

# ==========================================
# INTERFEJS STREAMLIT
# ==========================================

# Konfiguracja strony - nazwa projektu SALTO PROJEKT GEMINI
st.set_page_config(page_title="SALTO PROJEKT GEMINI", page_icon="🚀", layout="wide")

# Główny tytuł i podtytuł
st.title("🚀 SALTO PROJEKT GEMINI")
st.write("Witaj w zintegrowanym systemie wspomagania decyzji żywieniowych i środowiskowych.")

# Definicja zakładek
tab1, tab2, tab3, tab4 = st.tabs(["Kalkulator BMI", "Środowisko (Ania)", "Kalkulator Kalorii (Julka)", "Lodówka (Zuzia)"])

# ----------------------------------------------------
# ZAKŁADKA 1: Kalkulator BMI
# ----------------------------------------------------
with tab1:
    st.header("Kalkulator BMI")
    col1, col2 = st.columns(2)
    
    with col1:
        waga = st.number_input("Podaj wagę (kg)", min_value=0.0, step=0.1, key="bmi_waga")
    with col2:
        wzrost = st.number_input("Podaj wzrost (m)", min_value=0.0, step=0.01, format="%.2f", key="bmi_wzrost")

    if st.button("Oblicz moje BMI"):
        if waga > 0 and wzrost > 0:
            bmi = waga / (wzrost ** 2)
            st.metric(label="Twoje BMI wynosi", value=f"{bmi:.2f}")
            
            interpretacja = ""
            color = ""
            
            if bmi < 16.0:
                interpretacja = "wygłodzenie"
                color = "error"
            elif bmi < 17.0:
                interpretacja = "wychudzenie"
                color = "warning" 
            elif bmi < 18.5:
                interpretacja = "niedowaga"
                color = "warning" 
            elif bmi < 25.0:
                interpretacja = "waga prawidłowa"
                color = "success"
            elif bmi < 30.0:
                interpretacja = "nadwaga"
                color = "warning"
            elif bmi < 35.0:
                interpretacja = "otyłość I stopnia"
                color = "error"
            elif bmi < 40.0:
                interpretacja = "otyłość II stopnia"
                color = "error"
            else:
                interpretacja = "otyłość III stopnia"
                color = "error"
            
            if color == "success":
                st.success(f"Interpretacja: {interpretacja}")
            elif color == "warning":
                st.warning(f"Interpretacja: {interpretacja}")
            else:
                st.error(f"Interpretacja: {interpretacja}")
        else:
            st.error("Proszę uzupełnić wagę i wzrost wartościami większymi od zera.")

# ----------------------------------------------------
# ZAKŁADKA 2: Ania (Jakość powietrza)
# ----------------------------------------------------
with tab2:
    st.header("Analiza Jakości Powietrza (PM2.5)")
    st.info("Zdrowe życie to nie tylko jedzenie, to też środowisko. Moduł pobiera historyczne dane o zanieczyszczeniu.")
    
    # ID plików GIOS (przykładowe lata)
    gios_url_ids = {2014: '302', 2019: '322'} 
    gios_pm25_file = {2014: '2014_PM2.5_1g.xlsx', 2019: '2019_PM25_1g.xlsx'}
    
    selected_year = st.selectbox("Wybierz rok danych do pobrania", options=[2014, 2019])
    
    if st.button("Pobierz dane GIOS"):
        with st.spinner("Pobieranie i przetwarzanie danych..."):
            df_air = download_gios_archive(selected_year, gios_url_ids[selected_year], gios_pm25_file[selected_year])
            
        if df_air is not None:
            st.success(f"Pobrano dane za rok {selected_year}")
            st.dataframe(df_air.head(10)) # Wyświetl pierwsze 10 wierszy
            st.caption("Wyświetlono 10 pierwszych wierszy pobranego pliku.")

# ----------------------------------------------------
# ZAKŁADKA 3: Julka (Kalkulator CPM/Makro)
# ----------------------------------------------------
with tab3:
    st.header("Zapotrzebowanie Kaloryczne i Makroskładniki")
    
    # Formularz danych użytkownika
    col_j1, col_j2 = st.columns(2)
    with col_j1:
        gender_input = st.selectbox("Płeć", ["kobieta", "mężczyzna"])
        age_input = st.number_input("Wiek", min_value=1, max_value=120, value=25)
        weight_input = st.number_input("Waga (kg)", min_value=30.0, max_value=300.0, value=70.0)
    
    with col_j2:
        height_input = st.number_input("Wzrost (cm)", min_value=100, max_value=250, value=170)
        # Mapowanie opisu aktywności na wskaźnik PAL
        activity_map = {
            "Brak aktywności (siedzący tryb życia)": 1.2,
            "Lekka aktywność (ćwiczenia 1-3 razy w tyg.)": 1.375,
            "Średnia aktywność (ćwiczenia 3-5 razy w tyg.)": 1.55,
            "Duża aktywność (ćwiczenia 6-7 razy w tyg.)": 1.725,
            "Bardzo duża aktywność (praca fizyczna + treningi)": 1.9
        }
        activity_desc = st.selectbox("Poziom aktywności", list(activity_map.keys()))
        target_input = st.selectbox("Cel diety", ["schudnąć", "utrzymać wagę", "przytyć"])

    if st.button("Oblicz plan dietetyczny"):
        # Logika "Bezpieczeństwa"
        bmi_check = weight_input / ((height_input/100) ** 2)
        unsafe_goal = False
        
        if bmi_check < 18.5 and target_input == "schudnąć":
            st.error("⚠️ UWAGA: Twoje BMI wskazuje na niedowagę. Odchudzanie może być niebezpieczne dla zdrowia!")
            unsafe_goal = True
        elif bmi_check > 30.0 and target_input == "przytyć":
            st.warning("⚠️ UWAGA: Twoje BMI wskazuje na otyłość. Zwiększanie masy ciała powinno odbywać się pod kontrolą lekarza.")
        
        # Tworzenie obiektu User
        pal_value = activity_map[activity_desc]
        user = User(gender_input, age_input, weight_input, height_input, pal_value, [], target_input)
        
        st.divider()
        
        # Wyniki
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("PPM (BMR)", f"{int(user.bmr())} kcal", help="Podstawowa Przemiana Materii")
        with c2:
            st.metric("CPM (TDEE)", f"{int(user.bmr() * user.activity)} kcal", help="Całkowita Przemiana Materii")
        with c3:
            st.metric("Cel Kaloryczny", f"{user.tdee()} kcal", delta=f"{user.tdee() - int(user.bmr() * user.activity)} kcal różnicy")

        st.subheader("🍽️ Twój rozkład Makroskładników")
        macros = user.macros()
        df_macros = pd.DataFrame.from_dict(macros, orient='index', columns=['Ilość'])
        st.bar_chart(df_macros)
        
        st.subheader("💊 Witaminy i Minerały")
        st.info(user.minerals())

        st.subheader("🛒 Co jeść?")
        recs = user.recs()
        with st.expander("Kliknij, aby zobaczyć polecane źródła"):
            st.write(f"**Białko:** {recs['Białko']}")
            st.write(f"**Tłuszcze:** {recs['Tłuszcze']}")
            st.write(f"**Węglowodany:** {recs['Węglowodany']}")

# ----------------------------------------------------
# ZAKŁADKA 4: Zuzia (Lodówka / Przepisy)
# ----------------------------------------------------
with tab4:
    st.header("Co zjem z tego co mam w lodówce?")
    st.write("Zaznacz produkty, które masz w domu, a system zaproponuje proste danie.")
    
    # Baza prostych przepisów
    recipes_db = [
        {"name": "Jajecznica z pomidorami", "ingredients": ["jajka", "pomidor", "cebula"], "type": "śniadanie"},
        {"name": "Owsianka z owocami", "ingredients": ["płatki owsiane", "mleko", "jabłko"], "type": "śniadanie"},
        {"name": "Kurczak z ryżem i warzywami", "ingredients": ["kurczak", "ryż", "papryka"], "type": "obiad"},
        {"name": "Makaron z sosem pomidorowym", "ingredients": ["makaron", "pomidor", "czosnek"], "type": "obiad"},
        {"name": "Sałatka grecka", "ingredients": ["pomidor", "ogórek", "ser feta", "oliwa"], "type": "kolacja"},
        {"name": "Kanapki z serem i szynką", "ingredients": ["chleb", "ser żółty", "szynka", "masło"], "type": "kolacja/śniadanie"},
    ]
    
    # Lista wszystkich unikalnych składników
    all_ingredients = sorted(list(set([item for sublist in [r['ingredients'] for r in recipes_db] for item in sublist])))
    
    # Multiselect dla użytkownika
    user_fridge = st.multiselect("Co masz w lodówce/szafce?", all_ingredients)
    
    if st.button("Znajdź przepis"):
        found_any = False
        if not user_fridge:
            st.warning("Najpierw zaznacz jakieś składniki!")
        else:
            st.subheader("Propozycje dań:")
            for recipe in recipes_db:
                recipe_ingredients = set(recipe['ingredients'])
                user_ingredients = set(user_fridge)
                
                missing = recipe_ingredients - user_ingredients
                
                # Warunek wyświetlenia: masz wszystko ALBO brakuje max 1 składnika
                if len(missing) == 0:
                    st.success(f"**{recipe['name']}** ({recipe['type']}) - Masz wszystkie składniki! ✅")
                    found_any = True
                elif len(missing) == 1:
                    st.info(f"**{recipe['name']}** ({recipe['type']}) - Brakuje Ci tylko: {list(missing)[0]}. Może dasz radę bez tego? 🤔")
                    found_any = True
            
            if not found_any:
                st.error("Niestety, z tych składników nie umiem ułożyć pełnego dania z mojej bazy. Spróbuj dokupić jajka lub pomidory - pasują do wszystkiego!")

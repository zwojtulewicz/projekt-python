import streamlit as st

def calculate_bmi(user):
    # wzór do obliczenia BMI
    return user.weight / ((user.height / 100) ** 2)

def interpret_bmi(bmi):
    if bmi < 16.0:  # sprawdza, czy BMI jest mniejsze od 16 i przypisuje temu odpowiednią interpretację
        interpretacja = "wygłodzenie"
        color = "error"  # ustawia flagę koloru na "error", co w języku streamlit oznacza czerowny
    elif bmi < 17.0:  # jeżeli powyższy warunek jest niespełniony sprawdza, czy BMI jest większe lub równe 16, ale mniejsze o od 17 i przypisuje temu odpowiednią interpretację
        interpretacja = "wychudzenie"
        color = "warning"  # ustawia flagę koloru na "warning", co w języku streamlit oznacza pomarańczowy
    elif bmi < 18.5:  # jeżeli powyższy warunek jest niespełniony sprawdza, czy BMI jest większe lub równe 17, ale mniejsze o od 18.5 i przypisuje temu odpowiednią interpretację
        interpretacja = "niedowaga"
        color = "warning"  # ustawia flagę koloru na "warning", co w języku streamlit oznacza pomarańczowy
    elif bmi < 25.0:  # jeżeli powyższy warunek jest niespełniony sprawdza, czy BMI jest większe lub równe 18.5, ale mniejsze o od 25 i przypisuje temu odpowiednią interpretację
        interpretacja = "waga prawidłowa"
        color = "success"  # ustawia flagę koloru na "success", co w języku streamlit oznacza zielony
    elif bmi < 30.0:  # jeżeli powyższy warunek jest niespełniony sprawdza, czy BMI jest większe lub równe 25, ale mniejsze o od 30 i przypisuje temu odpowiednią interpretację
        interpretacja = "nadwaga"
        color = "warning"  # ustawia flagę koloru na "warning", co w języku streamlit oznacza pomarańczowy
    elif bmi < 35.0:  # jeżeli powyższy warunek jest niespełniony sprawdza, czy BMI jest większe lub równe 30, ale mniejsze o od 35 i przypisuje temu odpowiednią interpretację
        interpretacja = "otyłość I stopnia"
        color = "error"  # ustawia flagę koloru na "error", co w języku streamlit oznacza czerwony
    elif bmi < 40.0:  # jeżeli powyższy warunek jest niespełniony sprawdza, czy BMI jest większe lub równe 35, ale mniejsze o od 40 i przypisuje temu odpowiednią interpretację
        interpretacja = "otyłość II stopnia"
        color = "error"  # ustawia flagę koloru na "error", co w języku streamlit oznacza czerowny
    else:  # jeżeli powyższy warunek jest niespełniony else zajmuje się wszystkimi przypadkami gdzie BMI jest większe lub równe 40
        interpretacja = "otyłość III stopnia"
        color = "error"  # ustawia flagę koloru na "error", co w języku streamlit oznacza czerowny

    if color == "success":  # wyświetla zielony pasek "sukcesu" z tekstem interpretacji
        st.success(f"Interpretacja: {interpretacja}")
    elif color == "warning":  # wyświetla pomarańczowy pasek "ostrzeżenia" z tekstem interpretacji
        st.warning(f"Interpretacja: {interpretacja}")
    else:  # wyświetla czerwony "błędu" z tekstem interpretacji
        st.error(f"Interpretacja: {interpretacja}")
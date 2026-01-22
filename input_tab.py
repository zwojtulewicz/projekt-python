import streamlit as st

def st_input_col1():
    gender_display = st.selectbox("Płeć", ["Mężczyzna", "Kobieta"], key="z_plec")
    gender_val = "m" if gender_display == "Mężczyzna" else "f"  # odnosi się do wartości określonych w klasie

    age_z = st.number_input("Wiek", min_value=1, max_value=120, value=25, key="z_wiek")  # domyślna wartość: 25

    height_z = st.number_input("Wzrost (cm)", min_value=100, max_value=250, value=170,
                               key="z_wzrost")  # domyślna wartość: 170
    weight_z = st.number_input("Waga (kg)", min_value=30.0, max_value=300.0, value=65.0,
                               key="z_waga")  # domyślna wartość: 65

    return gender_val, age_z, height_z, weight_z

def st_input_col2():
    activity_options = {
        "Brak ćwiczeń": 1.2,
        "Lekka (1-3 dni)": 1.375,
        "Umiarkowana (3-5 dni)": 1.55,
        "Duża (6-7 dni)": 1.725,
        "Bardzo duża (sport zawodowy)": 2.4
    }
    act_key = st.selectbox("Aktywność", list(activity_options.keys()), key="z_akt")  # wyświetla klucze z listy
    activity_val = activity_options[act_key]  # wyciąga wartość liczbową z kodu podporządkowaną pod klucz

    target_options = {"Schudnąć": "lose", "Utrzymać wagę": "maintain",
                      "Przytyć": "gain"}  # słownik podporządkowany pod klasę
    tar_key = st.selectbox("Cel", list(target_options.keys()), key="z_cel")  # lista z wyborem celu
    target_val = target_options[tar_key]  # wyciąga wartość z kodu podporządkowaną pod klucz

    lifestyle = st.selectbox("Tryb pracy", ["Biurowa", "Fizyczna", "Mieszana"],
                             key="z_praca")  # lista wyboru trybu pracy

    return activity_val, target_val, lifestyle
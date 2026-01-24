# Asystent Zdrowego Żywienia

Kompleksowa aplikacja webowa stworzona w języku **Python** przy użyciu biblioteki **Streamlit**.  
Projekt pełni rolę osobistego asystenta dietetycznego, oferując narzędzia do analizy stanu zdrowia (BMI), obliczania zapotrzebowania kalorycznego (BMR/TDEE) oraz inteligentnego planowania posiłków.

---

## Główne funkcjonalności

Aplikacja podzielona jest na 5 interaktywnych modułów:

### Kalkulator BMI
- Obliczanie wskaźnika masy ciała na podstawie wagi i wzrostu  
- Interpretacja wyniku (od niedowagi po różne stopnie otyłości)  
- Czytelna prezentacja wyników z kodowaniem kolorystycznym  

### Kalkulator BMR i TDEE
- Obliczanie Podstawowej Przemiany Materii (BMR)  
- Szacowanie Całkowitego Dziennego Zapotrzebowania Kalorycznego (TDEE)  
- Uwzględnienie poziomu aktywności fizycznej użytkownika  

### Planer Dietetyczny
- Generowanie podziału makroskładników (białko, tłuszcze, węglowodany)  
- Dopasowanie do celu użytkownika (redukcja, utrzymanie, masa)  
- Rekomendacje źródeł makroelementów  
- Filtrowanie diet (wegańska, wegetariańska, bezglutenowa)  
- Podstawowe porady dotyczące mikroelementów i suplementacji  

### Baza Przepisów (Web Scraping)
- Automatyczne pobieranie przepisów z serwisu **aniagotuje.pl**  
- Parsowanie danych:
  - tytuł przepisu  
  - makroskładniki  
  - czas przygotowania  
  - lista składników  
  - liczba porcji  
- Zarządzanie lokalną bazą danych w pliku `recipes.csv`
  - dodawanie  
  - usuwanie przepisów  

### Interaktywny Kreator Dnia
- Inteligentny algorytm rekomendacji posiłków  
- Dobieranie przepisów do dziennego celu kalorycznego i makroskładnikowego  

---

## Struktura plików
- `main.py`: Główny plik uruchomieniowy aplikacji, łączy wszystkie moduły i zarządza nawigacją między zakładkami
- `aniagotuje_scraping.py`: Moduł odpowiedzialny za web scraping, zawiera klasę recipe oraz funkcje pobierające i parsujące dane ze strony **aniagotuje.pl**
- `file_handling_tab.py`: Obsługa pliku CSV (wczytywanie, dodawanie i usuwanie przepisów z bazy)
- `meal_recommendations_tab.py`: Logika "książki kucharskiej" i algorytm dobierania najlepszego przepisu do zadanych celów makroskładnikowych
- `input_handling.py`: Definicja klasy User wraz z walidacją danych wejściowych (gettery, settery)
- `input_tab.py`: Komponenty interfejsu służące do wprowadzania danych użytkownika
- `bmi_tab.py`: Logika i wyświetlanie kalkulatora BMI
- `bmr_tdee_tab.py`: Funkcje obliczeniowe dla zapotrzebowania kalorycznego
- `macros_tab.py`: Obliczenia podziału makroskładników i generowanie list polecanych produktów
- `recipes.csv`: Plik tekstowy pełniący rolę bazy danych z nazwami przepisów

---

## Wymagania i instalacja

### Wymagania
- Python **3.8+**
- pip

### Instalacja

```bash
# Sklonuj repozytorium
git clone https://github.com/zwojtulewicz/projekt-python.git
cd projekt-python

# Utwórz i aktywuj środowisko wirtualne
python3 -m venv venv
source venv/bin/activate  # macOS / Linux
# venv\Scripts\activate   # Windows

# Zainstaluj wymagane pakiety
pip install streamlit requests beautifulsoup4

# Uruchom aplikację
streamlit run main.py


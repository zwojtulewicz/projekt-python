# Asystent Zdrowego Żywienia

Kompleksowa aplikacja webowa stworzona w języku **Python** przy użyciu biblioteki **Streamlit**.  
Projekt pełni rolę osobistego asystenta dietetycznego, oferując narzędzia do analizy stanu zdrowia (BMI), obliczania zapotrzebowania kalorycznego (BMR/TDEE) oraz inteligentnego planowania posiłków.

---

## Główne funkcjonalności

Aplikacja podzielona jest na kilka interaktywnych modułów:

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
- Możliwość planowania całego dnia:
  - 3, 4 lub 5 posiłków  

---

## Wymagania i instalacja

### Wymagania
- Python **3.8+**
- pip

### Instalacja

Sklonuj repozytorium:
```bash
git clone <adres-twojego-repozytorium>
cd <nazwa-folderu>

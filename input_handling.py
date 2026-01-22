class User:
    # przypisania, które wywołują settery, czyli metody walidacji
    def __init__(self, gender, age, weight, height, activity, diet_type, lifestyle, target):
        self.gender = gender  # ustawienie płci
        self.age = age  # ustawienie wieku
        self.weight = weight  # ustawienie wagi
        self.height = height  # ustawienie wzrostu
        self.activity = activity  # ustawienie poziomu aktywności
        self.diet_type = [r.casefold() for r in diet_type]  # tworzy listę restrykcji
        self.lifestyle = lifestyle  # ustawienie trybu życia
        self.target = target  # ustawienie targetu

    @property
    def gender(self):
        return self._gender  # getter zwraca wartość zmiennej

    @gender.setter
    def gender(self, g):  # setter sprawdza czy spełnione są konkretne warunki (płeć kobieta lub mężczyzna)
        valid_gender = ["f", "m"]
        if not isinstance(g,
                          str) or g.casefold() not in valid_gender:  # jeżeli płeć nie jest stringiem lub jedną z valid genders - error
            raise ValueError("Nieprawidłowa płeć")
        self._gender = g.casefold()  # jeżeli spełnione są warunki - zapis do zmiennej

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self,
            a):  # setter sprawdza czy spełnione są konkretne warunki (wiek wyższy lub równy 0 i jednocześnie mniejszy od 120)
        if not isinstance(a,
                          int) or a <= 0 or a > 120:  # jeżeli nie spełnia warunków lub nie jest liczbą całkowitą - error
            raise ValueError("Nieprawidłowy wiek")
        self._age = a

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self,
               w):  # setter sprawdza czy spełnione są konkretne warunki (waga większa lub równa 0 i jednocześnie mniejsza od 600)
        if w <= 0 or w > 600:  # jeżeli nie spełnia warunków - error
            raise ValueError("Nieprawidłowa waga")
        self._weight = w

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self,
               h):  # setter sprawdza czy spełnione są konkretne warunki (wzrost większy lub równy 50 i jednocześnie mniejszy od 300)
        if h <= 50 or h > 300:  # jeżeli nie spełnia warunków - error
            raise ValueError("Nieprawidłowy wzrost")
        self._height = h

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, t):
        valid_target = ["lose", "gain",
                        "maintain"]  # setter sprawdza czy spełnione są konkretne warunki (czy cel znajduje się w liście)
        if not isinstance(t,
                          str) or t.casefold() not in valid_target:  # jeżeli cel nie jest stringiem i nie należy do listy - error
            raise ValueError("Nieprawidłowy cel")
        self._target = t.casefold()

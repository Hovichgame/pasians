# **Dokumentacja Projektu: Pasjans Konsolowy**
Niniejszy dokument opisuje sposób uruchomienia oraz instrukcje użytkowania gry Pasjans w wersji konsolowej, a także przedstawia strukturę kodu źródłowego.
## **Sposób Uruchomienia Projektu**
Aby uruchomić grę Pasjans, wykonaj następujące kroki:

1. **Upewnij się, że masz zainstalowany Python.** Projekt jest napisany w języku Python. Jeśli nie masz Pythona, możesz go pobrać ze strony [python.org](https://www.python.org/ "null").
1. **Pobierz plik 13-15 python\_aliaksei\_akulau.py.**
1. **Otwórz terminal lub wiersz poleceń.**
1. **Przejdź do katalogu, w którym zapisałeś plik.** Możesz to zrobić za pomocą komendy cd <nazwa\_katalogu>.
1. **Uruchom grę** wpisując w terminalu:

   python "13-15 python\_aliaksei\_akulau.py"
## **Instrukcje Rozgrywki dla Użytkownika**
Gra "Pasjans" to klasyczna wersja Pasjansa "Kosynka", uruchamiana w konsoli. Poniżej znajdziesz dostępne komendy i ogólne zasady gry.
### **Cel Gry**
Celem gry jest przeniesienie wszystkich kart na cztery fundamenty, budując je od Asa do Króla dla każdego koloru.
### **Sterowanie (Dostępne Komendy)**
Wszystkie komendy wpisuje się w konsoli po wyświetleniu bieżącego stanu gry.

- **dobierz**
  - **Opis:** Dobiera jedną kartę z talii do talonu. Jeśli talia się skończy, zostaje zresetowana.
  - **Przykład:** dobierz
- **przenies kol <z\_nr> <na\_nr> <ile\_kart>**
  - **Opis:** Przenosi określoną liczbę kart z jednej kolumny na drugą.
    - <z\_nr>: Numer kolumny źródłowej.
    - <na\_nr>: Numer kolumny docelowej.
    - <ile\_kart>: Liczba kart do przeniesienia (od góry stosu).
  - **Przykład:** przenies kol 3 5 2 (przenosi 2 karty z kolumny 3 do kolumny 5)
- **przenies talon <kolumna\_nr>**
  - **Opis:** Przenosi kartę z talonu na wybraną kolumnę.
    - <kolumna\_nr>: Numer kolumny docelowej.
  - **Przykład:** przenies talon 2
- **przenies fund <kolumna\_nr> <fundament\_nr>**
  - **Opis:** Przenosi kartę z kolumny na fundament.
    - <kolumna\_nr>: Numer kolumny źródłowej.
    - <fundament\_nr>: Numer fundamentu docelowego.
  - **Przykład:** przenies fund 1 3
- **przenies talon fund**
  - **Opis:** Przenosi kartę z talonu na fundament, jeśli pasuje do któregoś z fundamentów.
  - **Przykład:** przenies talon fund
- **auto**
  - **Opis:** Automatycznie przenosi możliwe karty na fundamenty.
  - **Przykład:** auto
- **undo**
  - **Opis:** Cofnij ostatni ruch.
  - **Przykład:** undo
- **restart**
  - **Opis:** Rozpoczyna nową grę z nowym układem kart.
  - **Przykład:** restart
- **stan**
  - **Opis:** Pokazuje bieżący stan gry. Ta komenda jest zwykle wykonywana automatycznie po każdym ruchu, ale można jej użyć do odświeżenia widoku.
  - **Przykład:** stan
- **wyjdz**
  - **Opis:** Kończy grę.
  - **Przykład:** wyjdz
### **Dodatkowe Informacje**
- Talia zawiera 52 karty.
- Karty są oznaczone np. A♥, 10♠, K♦ itd.
- Zakryte karty są oznaczone jako XX.
- Fundamenty rosną od Asa do Króla dla każdego koloru.
- System obsługuje cofanie ruchów (undo).
- Gra automatycznie odkrywa kartę, jeśli zostanie sama w kolumnie.
## **Opis Poszczególnych Klas, Modułów i Metod/Funkcji**
Poniżej znajduje się opis kluczowych elementów kodu źródłowego pliku 13-15 python\_aliaksei\_akulau.py.
### **Stałe Globalne**
- RANKS: Lista stringów reprezentujących rangi kart (od 'A' do 'K').
- SUITS: Lista stringów reprezentujących kolory kart ('♠', '♥', '♦', '♣').
- RED: Zbiór stringów reprezentujących czerwone kolory ('♥', '♦').
- BLACK: Zbiór stringów reprezentujących czarne kolory ('♠', '♣').
### **Funkcje**
- pokaz\_dokumentacje():
  - **Opis:** Wyświetla w konsoli szczegółową dokumentację gry, w tym opis ogólny, dostępne komendy i dodatkowe informacje o rozgrywce.
- create\_deck():
  - **Opis:** Tworzy pełną talię 52 kart, łącząc wszystkie rangi z wszystkimi kolorami.
  - **Zwraca:** list - lista stringów reprezentujących karty (np. "A♠", "2♥").
### **Klasa Solitaire**
Główna klasa zarządzająca logiką gry Pasjans.
#### **Atrybuty Instancji**
- foundations: Lista list, gdzie każda wewnętrzna lista reprezentuje jeden z czterech fundamentów. Karty na fundamentach są posortowane rosnąco według rangi i koloru.
- tableau: Lista list, gdzie każda wewnętrzna lista reprezentuje jedną z siedmiu kolumn na stole. Karty mogą być zakryte (XX) lub odkryte.
- talon: Lista stringów reprezentujących karty w talii (stosie dobierania).
- talon\_index: Liczba całkowita wskazująca indeks bieżącej karty w talon, która jest widoczna lub gotowa do przeniesienia.
- history: Lista zawierająca kopie stanu gry (krotki (foundations, tableau, talon, talon\_index)) przed każdym ruchem, co umożliwia cofanie ruchów.
#### **Metody**
- \_\_init\_\_(self):
  - **Opis:** Konstruktor klasy. Inicjuje nową grę poprzez wywołanie metody restart().
- restart(self):
  - **Opis:** Resetuje stan gry do początkowego. Tworzy nową, potasowaną talię, rozkłada karty na fundamenty i kolumny, oraz inicjuje talon i historię ruchów.
- save(self):
  - **Opis:** Zapisuje bieżący stan gry (fundamenty, kolumny, talon, indeks talonu) do historii (self.history). Używa copy.deepcopy aby zapewnić, że zapisywane są niezależne kopie.
- undo(self):
  - **Opis:** Cofnięcie ostatniego ruchu. Przywraca stan gry z ostatniego zapisanego punktu w historii, a następnie usuwa ten punkt z historii.
- draw(self):
  - **Opis:** Dobiera kartę z talonu. Zwiększa talon\_index o 1, aby wskazać następną kartę. Jeśli talon się skończy, talon\_index jest resetowany do 0. Stan gry jest zapisywany przed ruchem.
- print\_state(self):
  - **Opis:** Wyświetla w konsoli aktualny stan gry, w tym zawartość fundamentów, talonu oraz wszystkich kolumn.
- can\_stack(self, upper, lower):
  - **Opis:** Sprawdza, czy karta upper może być położona na kartę lower zgodnie z zasadami pasjansa (przeciwne kolory i ranga o jeden niższa). Nie pozwala na układanie na zakrytych kartach (XX).
  - **Parametry:**
    - upper (str): Karta, którą chcemy położyć.
    - lower (str): Karta, na którą chcemy położyć.
  - **Zwraca:** bool - True jeśli można ułożyć, False w przeciwnym razie.
- move\_tableau(self, z, na, ile):
  - **Opis:** Przenosi ile kart z kolumny o numerze z do kolumny o numerze na. Sprawdza poprawność ruchu (np. czy można przenosić zakryte karty, czy karta jest Królem na pustą kolumnę, czy karty pasują do siebie). Aktualizuje stan gry i odkrywa zakryte karty, jeśli staną się jedynymi w kolumnie.
- move\_talon\_to\_tableau(self, k):
  - **Opis:** Przenosi aktualnie widoczną kartę z talonu do kolumny o numerze k. Sprawdza poprawność ruchu i aktualizuje stan gry.
- move\_column\_to\_foundation(self, kol, fund):
  - **Opis:** Przenosi wierzchnią kartę z kolumny o numerze kol na odpowiedni fundament. Wykorzystuje wewnętrzną metodę \_move\_card\_to\_foundation.
- move\_talon\_to\_foundation(self):
  - **Opis:** Próbuje przenieść aktualnie widoczną kartę z talonu na którykolwiek z fundamentów, jeśli jest to zgodne z zasadami.
- \_move\_card\_to\_foundation(self, card, col\_idx=None, force\_fund\_idx=None):
  - **Opis:** Prywatna metoda pomocnicza do przenoszenia karty na fundament. Sprawdza, czy karta może być dodana do fundamentu (czy jest Asem na pustym fundamencie lub ma rangę o jeden wyższą niż wierzchnia karta fundamentu i ten sam kolor).
  - **Parametry:**
    - card (str): Karta do przeniesienia.
    - col\_idx (int lub None): Indeks kolumny, z której przenoszona jest karta. Jeśli None, karta pochodzi z talonu.
    - force\_fund\_idx (int lub None): Wymuszony indeks fundamentu, na który ma być przeniesiona karta. Jeśli None, fundament jest wybierany na podstawie koloru karty.
  - **Zwraca:** bool - True jeśli ruch się powiódł, False w przeciwnym razie.
- auto\_foundation(self):
  - **Opis:** Automatycznie przenosi wszystkie możliwe karty z kolumn i talonu na fundamenty, dopóki są możliwe ruchy.
- check\_game\_over(self):
  - **Opis:** Sprawdza, czy gra została zakończona (zwycięstwo lub przegrana).
    - **Zwycięstwo:** Wszystkie fundamenty są pełne (13 kart każdy).
    - **Przegrana:** Brak możliwych ruchów na stole (nie można przenieść kart między kolumnami ani z talonu) i talon jest pusty.
  - **Zwraca:** bool - True jeśli gra się zakończyła, False w przeciwnym razie.
- play(self):
  - **Opis:** Główna pętla gry. Wyświetla stan gry, przyjmuje komendy od użytkownika, przetwarza je i sprawdza stan gry po każdym ruchu. Obsługuje również błędy wejścia.

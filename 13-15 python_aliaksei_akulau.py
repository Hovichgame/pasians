import random
import copy
import sys

RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
SUITS = ['♠', '♥', '♦', '♣']
RED = {'♥', '♦'}
BLACK = {'♠', '♣'}


def pokaz_dokumentacje():
    print("""
📘 Dokumentacja gry konsolowej: Pasjans

📌 Opis ogólny:
Ta gra to klasyczna wersja pasjansa "Kosynka", działająca w konsoli. 
Gra zawiera podstawowe funkcje oraz dodatkowe jak automatyczne przenoszenie, cofanie ruchów i restart gry.

✅ Dostępne komendy:

dobierz
  - Dobiera jedną kartę z talii do talonu.
  - Jeśli talia się skończy, zostaje zresetowana.
  - Przykład: dobierz

przenies kol <z_nr> <na_nr> <ile_kart>
  - Przenosi karty z jednej kolumny do drugiej.
  - Przykład: przenies kol 3 5 2

przenies talon <kolumna_nr>
  - Przenosi kartę z talonu na kolumnę.
  - Przykład: przenies talon 2

przenies fund <kolumna_nr> <fundament_nr>
  - Przenosi kartę z kolumny na fundament.
  - Przykład: przenies fund 1 3

przenies talon fund
  - Przenosi kartę z talonu na fundament, jeśli pasuje.
  - Przykład: przenies talon fund

auto
  - Automatycznie przenosi możliwe karty na fundamenty.
  - Przykład: auto

undo
  - Cofnij ostatni ruch.
  - Przykład: undo

restart
  - Rozpoczyna nową grę z nowym układem kart.
  - Przykład: restart

stan
  - Pokazuje bieżący stan gry.
  - Przykład: stan

wyjdz
  - Kończy grę.
  - Przykład: wyjdz

ℹ️ Dodatkowe informacje:
- Talia zawiera 52 karty.
- Karty są oznaczone np. A♥, 10♠, K♦ itd.
- Zakryte karty są oznaczone jako XX.
- Fundamenty rosną od Asa do Króla dla każdego koloru.
- System obsługuje cofanie ruchów (undo).
- Gra automatycznie odkrywa kartę, jeśli zostanie sama w kolumnie.

Miłej gry!
""")



def create_deck():
    return [r + s for s in SUITS for r in RANKS]

class Solitaire:
    def __init__(self):
        self.restart()
    
    def restart(self):
        deck = create_deck()
        random.shuffle(deck)
        self.foundations = [[] for _ in range(4)]
        self.tableau = []
        for i in range(7):
            hidden = ['XX'] * i
            visible = [deck.pop()]
            self.tableau.append(hidden + visible)
        self.talon = deck
        self.talon_index = 0
        self.history = []

    def save(self):
        self.history.append(copy.deepcopy((self.foundations, self.tableau, self.talon, self.talon_index)))

    def undo(self):
        if self.history:
            self.foundations, self.tableau, self.talon, self.talon_index = self.history.pop()

    def draw(self):
        self.save()
        if self.talon_index < len(self.talon):
            self.talon_index += 1
        else:
            self.talon_index = 0

    def print_state(self):
        print("\n--- Stan gry ---")
        print("Fundamenty:")
        for i, f in enumerate(self.foundations, 1):
            print(f" {i}: {f[-1] if f else '(puste)'}", end=" | ")
        print(f"\n\nTalon: {self.talon[self.talon_index - 1] if self.talon_index > 0 else '(pusty)'}\n")
        print("Kolumny:")
        for i, col in enumerate(self.tableau, 1):
            print(f"{i}. {' '.join(col)}")
        print("-----------------")

    def can_stack(self, upper, lower):
        if lower == 'XX': return False
        r1, s1 = upper[:-1], upper[-1]
        r2, s2 = lower[:-1], lower[-1]
        return ((s1 in RED and s2 in BLACK) or (s1 in BLACK and s2 in RED)) and RANKS.index(r1) + 1 == RANKS.index(r2)

    def move_tableau(self, z, na, ile):
        z -= 1
        na -= 1
        src = self.tableau[z]
        dst = self.tableau[na]
        if ile <= 0 or ile > len(src):
            print("Nieprawidłowa liczba kart.")
            return
        moving = src[-ile:]
        if 'XX' in moving:
            print("Nie można przenosić zakrytych kart.")
            return
        if not dst:
            if moving[0][:-1] != 'K':
                print("Tylko króla można położyć na pustą kolumnę.")
                return
        elif not self.can_stack(moving[0], dst[-1]):
            print("Nie można położyć tej karty tutaj.")
            return
        self.save()
        self.tableau[na].extend(moving)
        del self.tableau[z][-ile:]
        if self.tableau[z] and self.tableau[z][-1] == 'XX':
            self.tableau[z][-1] = self.talon.pop() if self.talon else 'A♠'

    def move_talon_to_tableau(self, k):
        if self.talon_index == 0:
            print("Brak kart w talonie.")
            return
        card = self.talon[self.talon_index - 1]
        dst = self.tableau[k - 1]
        if not dst:
            if card[:-1] != 'K':
                print("Tylko króla można położyć.")
                return
        elif not self.can_stack(card, dst[-1]):
            print("Nie można położyć tej karty.")
            return
        self.save()
        dst.append(card)
        del self.talon[self.talon_index - 1]
        self.talon_index -= 1

    def move_column_to_foundation(self, kol, fund):
        card = self.tableau[kol - 1][-1]
        self._move_card_to_foundation(card, kol - 1)

    def move_talon_to_foundation(self):
        if self.talon_index == 0:
            print("Brak kart w talonie.")
            return
        card = self.talon[self.talon_index - 1]
        for i in range(4):
            if self._move_card_to_foundation(card, None, i):
                self.save()
                del self.talon[self.talon_index - 1]
                self.talon_index -= 1
                return
        print("Nie można przenieść do fundamentu.")

    def _move_card_to_foundation(self, card, col_idx=None, force_fund_idx=None):
        r, s = card[:-1], card[-1]
        f_idx = force_fund_idx if force_fund_idx is not None else SUITS.index(s)
        fund = self.foundations[f_idx]
        if (not fund and r == 'A') or (fund and RANKS.index(r) == RANKS.index(fund[-1][:-1]) + 1):
            if col_idx is not None:
                self.save()
                self.foundations[f_idx].append(self.tableau[col_idx].pop())
                if self.tableau[col_idx] and self.tableau[col_idx][-1] == 'XX':
                    self.tableau[col_idx][-1] = self.talon.pop() if self.talon else 'A♠'
            else:
                self.foundations[f_idx].append(card)
            return True
        return False
    
    def auto_foundation(self):
        moved = True
        while moved:
            moved = False
            for i in range(7):
                col = self.tableau[i]
                if col and col[-1] != 'XX':
                    if self._move_card_to_foundation(col[-1], i):
                        moved = True
                        break
            if self.talon_index > 0:
                card = self.talon[self.talon_index - 1]
                for f in range(4):
                    if self._move_card_to_foundation(card, None, f):
                        self.save()
                        del self.talon[self.talon_index - 1]
                        self.talon_index -= 1
                        moved = True
                        break


    def check_game_over(self):
        if all(len(f) == 13 for f in self.foundations):
            print("\n🎉 Gratulacje! Wygrałeś grę!")
            exit()

        mozliwy_ruch = False
        if self.talon_index == 0 and not self.talon:
            
            for i, kolumna in enumerate(self.tableau):
                if not kolumna:
                    continue
                karta = kolumna[-1]
                for j, kolumna2 in enumerate(self.tableau):
                    if i == j:
                        continue
                    if kolumna2:
                        cel = kolumna2[-1]
                        if self.can_stack(karta, cel):
                            mozliwy_ruch = True
                            break
                    elif karta[:-1] == 'K':
                        mozliwy_ruch = True
                        break
                if mozliwy_ruch:
                    break

        if not mozliwy_ruch:
            print("\n❌ Brak możliwych ruchów. Przegrałeś.")
            exit()
    
    def play(self):
        while True:
            self.print_state()
            cmd = input("Podaj komendę: ").strip().lower()
            try:
                if cmd == "wyjdz":
                    break
                elif cmd == "dobierz":
                    self.draw()
                elif cmd == "undo":
                    self.undo()
                elif cmd == "restart":
                    self.restart()
                elif cmd == "auto":
                    self.auto_foundation()
                elif cmd.startswith("przenies kol"):
                    _, _, z, na, ile = cmd.split()
                    self.move_tableau(int(z), int(na), int(ile))
                elif cmd.startswith("przenies talon"):
                    _, _, k = cmd.split()
                    self.move_talon_to_tableau(int(k))
                elif cmd.startswith("przenies fund"):
                    _, _, z, f = cmd.split()
                    self.move_column_to_foundation(int(z), int(f))
                elif cmd == "przenies talon fund":
                    self.move_talon_to_foundation()
                else:
                    print("Nieznana komenda.")
                
                if self.check_game_over():
                    break
            except Exception as e:
                print(f"Błąd: {e}")

pokaz_dokumentacje()

if __name__ == "__main__":
    Solitaire().play() 

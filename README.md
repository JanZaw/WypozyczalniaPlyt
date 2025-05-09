# Wypożyczalnia Płyt Muzycznych – Opis i Wstępna Dokumentacja

## 1. Czym jest projekt

Projekt to prosty system do wypożyczania płyt muzycznych. 

Pozwala użytkownikowi:

- przeglądać dostępne płyty,
- rejestrować się i logować,
- wypożyczać i zwracać płyty,
- filtrować płyty po wykonawcy,
- przeglądać historię swoich wypożyczeń.

Administrator może:

- dodawać/usuwać płyty,
- zarządzać użytkownikami i wypożyczeniami.

## 2. Zakres realizacji

**Do Zrobione:**

- logowanie i rejestracja (JWT),
- katalog płyt,
- wypożyczanie i zwracanie płyt,
- historia wypożyczeń,
- API REST (JSON).


## 3. API – Jak korzystać

1. Użytkownik loguje się (`POST /api/login`), dostaje token.
2. Używa tokena do pobrania listy płyt (`GET /api/discs`).
3. Filtruje po id wykonawcy (`GET /apo/discs/:artist_id`)
3. Wypożycza płytę (`POST /api/rentals`).
4. Zwraca płytę (`PUT /api/rentals/:id/return`).
5. Może sprawdzić historię (`GET /api/rentals/history`).

## 4. Endpointy

### Autoryzacja

- `POST /api/register` – rejestracja
- `POST /api/login` – logowanie

**Przykład:**
```json
{ "email": "test@test.pl", "password": "haslo123" }
```

---

### Płyty

- `GET /api/discs` – lista płyt
- `GET /api/discs/:artist_id` - lista płyt danego wykonawcy
- `POST /api/discs` – dodanie płyty (admin)
- `PUT /api/discs/:id` – edycja (admin)
- `DELETE /api/discs/:id` – usunięcie (admin)

**Przykład:**
```json
{
  "artist": "Queen",
  "title": "A Night at the Opera",
  "genre": "rock",
  "year": 1975
}
```

---

### Wypożyczenia

- `POST /api/rentals` – wypożyczenie płyty
```json
{ "disc_id": 5 }
```

- `PUT /api/rentals/:id/return` – zwrot płyty
- `GET /api/rentals/history` – historia wypożyczeń
```json
[
  {
    "disc": "Nirvana – Nevermind",
    "rented_at": "2025-05-01",
    "returned_at": "2025-05-07"
  }
]
```

## 5. Baza danych (prosto)

- `users`: id, username ,email, password, role  
- `discs`: id, name, artist_id, genre, year avaible 
- `artist`: id, name, surname
- `rentals`: id, user_id, disc_id, rented_at, returned_at 

## PROJEKT MOŻE MIEĆ ZMIENIONE ZAŁOŻENIA PODCZAS ROBIENIA
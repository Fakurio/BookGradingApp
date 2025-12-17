# Book Grading App

System do oceniania książek. Umożliwia podstawowe operacje CRUD na książkach oraz dodawanie recenzji.  
W czasie rzeczywistym wyświetlane są statystyki dotyczące liczby książek i recenzji znajdujących się w systemie.

---

## Uruchomienie

1.  **Sklonuj repozytorium:**
    ```bash
    https://github.com/Fakurio/BookGradingApp.git
    cd BookGradingApp
    ```

2.  **Uruchom aplikację w kontenerach:**
    ```bash
    docker-compose up -d
    ```
3.  **Dostęp do aplikacji:** 
   Aplikacja jest dostępna pod adresem
    http://localhost:8080

---

## Technologie

**Backend:**
* **FastAPI**
* **SQLAlchemy**
* **MySQL**
* **Pytest**

**Frontend:**
* **React**
* **Typescript**

---

## Testowanie
  Testy jednostkowe można uruchomić za pomocą komendy

  ```bash
    cd backend && python3 -m pytest
  ```
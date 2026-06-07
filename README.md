# 📚 BookNook
A comfy personal book tracker with statistics and more

---

## Features
- Login and sign up
    - At the start of the application you can choose between "Log in" and "Create Account" 
    - Inserting a "username" and "password" in "Create Account" signs you in immediately
    - You can logout by pressing the "Logout" in the header
- Add, delete and edit books
    - You can add new book under the "+ Add Book" button seen in the header
    - You can delete a book by clicking on a book you have added and clicking the "Delete Book" button
    - You can edit a book by click on a book and clicking the "Edit Book" button and changing the information
- Regex supported search bar that searches book titles and authors
    - In the search bar in the index you can use regex expressions to search through added books
- Reading dashboard with statistics
    - In index you can click the link "Click to see your favorite books" and see statistics regarding read books

---

## 🚀 How to run

### 1. Clone repository

```sh
git clone https://github.com/bellpy/book-nook.git
cd book-nook
```

### 2. Create virtual environment
```sh
python3 -m venv .venv
. .venv/bin/activate
```
### 3. Install dependencies
```sh
pip install -r requirements.txt
```
### 4. Create database in postgres
Start PostgreSQL shell:
```sh
psql postgres
```
Inside psql run
```sh
CREATE DATABASE booknook;
```
You can verify it with ```\l``` and quit with ```\q```

### 5. Set enironments variables
```sh
export FLASK_APP=booknook
export FLASK_ENV=development
```
In the file `__init__.py` replace `user` and `your_password` with your own PostgreSQL credentials
```sh
export DATABASE_URL="postgresql://user:your_password@localhost:5432/booknook"
```

### 6. Initialize database
```sh
flask init-db
```

### 7. Running the application
```sh
flask run
```
---
## Testing
## 1. Initialize test database
```sh
CREATE DATABASE booknook_test;
```
## 2. Run tests
```sh
pytest
```

---

### To-do
- [X] Delete books
- [X] Regex search
- [X] Test setup
- [X] Edit books 
- [X] Add book statistics (Materialized view (top-rated books))
- [X] Login into app

Extra:
- [ ] Cover images
- [ ] Number of pages read
- [ ] Use ISBN API
- [ ] Track deletions (trigger function)
- [ ] Auto timestamp (trigger function)
- [ ] Docker?
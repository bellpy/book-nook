# 📚 BookNook
A comfy personal book tracker with statistics and more

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
CREATE DATABASE booknook;
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
export DATABASE_URL="postgresql://user:your_password@localhost:5432/booknook"
```

```sh
export DATABASE_URL="postgresql://user:your_password@localhost:5432/booknook"
```
Replace user and your_password with your actual PostgreSQL credentials.

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
- [ ] Edit books 
- [ ] Use ISBN API
- [ ] Add book statistics (Materialized view (top-rated books))
- [ ] Login into app
- [ ] Track deletions (trigger function)
- [ ] Auto timestamp (trigger function)
- [ ] Docker?
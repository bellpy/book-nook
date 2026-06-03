def test_homepage(client):
    response = client.get("/")
    assert response.status_code == 200

def test_create_book(client):
    response = client.post("/create", data={
        "title": "Dune",
        "author": "Frank Herbert",
        "review": "Great book",
        "rating": "5"
    }, follow_redirects=True)

    assert response.status_code == 200

def test_book_detail(client):
    response = client.get("/book/1")
    assert response.status_code in [200, 404]

def test_delete_book(client):
    response = client.post("/delete/1", follow_redirects=True)
    assert response.status_code == 200
def test_homepage(client):
    assert client.get("/").status_code == 200


def test_create_book(client):
    response = client.post("/create",
        data={
            "title": "Dune",
            "author": "Frank Herbert",
            "genres": "Sci-Fi",
            "review": "Great book",
            "rating": "5",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200


def test_dashboard(client):
    assert client.get("/dashboard").status_code == 200


def test_book_detail(client):
    client.post("/create",
        data={
            "title": "Dune",
            "author": "Frank Herbert",
            "genres": "Sci-Fi",
            "review": "Great book",
            "rating": "5",
        }
    )

    assert client.get("/book/1").status_code == 200


def test_delete_book(client):
    client.post("/create",
        data={
            "title": "Dune",
            "author": "Frank Herbert",
            "genres": "Sci-Fi",
            "review": "Great book",
            "rating": "5",
        }
    )

    response = client.post(
        "/delete/1",
        follow_redirects=True
    )

    assert response.status_code == 200
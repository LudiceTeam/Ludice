# Routers

## Done send request to API

### Bet.py
```python
def send_user_to_api(username, author, id_game, bet_id, ):
    url = "http://0.0.0.0:8000/register"
    data = {
        "username": username,
        "id_game": id_game,
        "author": author,
        "title": title,
        "bet": bet
    }
```

### Create_party.py
```python
def send_user_to_api(username, id, title, is_open=True):
    url = "http://0.0.0.0:8000/register"
    data = {
        "username": username,
        "id": id,
        "title": title,
        "is_open": is_open
    }
```

### delete_party.py
``` python
def send_user_to_api(username, id, title, is_open=True):
    url = "http://0.0.0.0:8000/register"
    data = {
        "username": username,
        "id": id,
    }
```

### joun_game.py
```python
def join_party(id_game, username, author):
    url = "http://0.0.0.0:8000/join"
    data = {
        "id_game": id_game,
        "username": username,
        "author": author
    }
```
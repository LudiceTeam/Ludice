import requests as r

#uvicorn main:app --reload
def register():
    url = "http://127.0.0.1:8000/register"
    data = {
        "username":"me",
        "psw":"123"
    }
    resp = r.post(url,json = data)
register()



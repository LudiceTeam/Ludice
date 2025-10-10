import json
import uuid
def generate():
    with open("drotic.json","r") as file:
        data = json.load(file)
    data.append({
        "bet":0,
        "players":[],
        "id":str(uuid.uuid4()),
        "cache":[]
    })   
    with open("drotic.json","w") as file:
        json.dump(data,file)
for i in range(10):
    generate()
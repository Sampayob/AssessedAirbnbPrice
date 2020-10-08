from fastapi import FastAPI
from joblib import load
from pydantic import  BaseModel, Field
import uvicorn
import os
from model import train, predict

#initiate API
app = FastAPI(title='MadridxAirbnb host price predictor',
              description = '''This project aims to **deploy a machine learning model in a RestAPI using FastAPI**.
              \n- It is a tool for future or actual Madrid Airbnb host to easy get their room/house priced.
              \n- **The data comes from Murray Cox project Inside Airbnb** and was goten the 13th of September, 2020.
              \n- For the moment **I am working to integrate the Streamlit (UI) and the FlastAPI server together** in Heroku
              (right now I can only display one of them on the cloud) although **they work together in local**.
              \n This are the **input requiremnts for GET and POST methods**:
              \n - **Neighbourhood group** (Centro, Latina...)
              \n - **Neighbourhood inside the previous one** (Retiro, Puerta del Angel...)
              \n - **Room type** (Private room, Entire home/apt or Hotel room)
              \n - **Minimum number of nights** (1,2,3,10...)
              \n - [Airbnb Madrid data-Interactive map](http://insideairbnb.com/madrid/)
               ''',

              version="1.0.0")

tags_metadata = [
    {
        "name": "home",
        "description": "Welcome page",
    },
    {
        "name": "predict_get",
        "description": "get a predicted price. Need Neighbourhood group, neighbourhood, room type and minimum_nights info",
        "externalDocs": {
            "description": "Airbnb Madrid data-Interactive map:",
            "url": "http://insideairbnb.com/madrid/"},
    },
    {
        "name": "predict_post",
        "description": "post a predicted price. Need Neighbourhood group, neighbourhood, room type and minimum_nights info",
        "externalDocs": {
            "description": "Airbnb Madrid data-Interactive map:",
            "url": "http://insideairbnb.com/madrid/"},
    },
]


# class for predictions post params
class Prediction(BaseModel):
    param1: str
    param2: str
    param3: str
    param4: int

# home page
@app.get('/', tags=["home"])
def home():
    return {"Greetings": 'Welcome to the MadridxAirbnb API for room/house predicted prices for Airbnb host in Madrid',
            "Next step": "Please go to '/docs' for accessing documentation and use GET and POST methods"}

# GET
@app.get('/predict/' , tags=["predict_get"])
async def get_prediction(neighbourhood_group, neighbourhood, room_type, minimum_nights):
    train()
    predicted_price = predict(neighbourhood_group, neighbourhood, room_type, minimum_nights)
    return {'Neighbourhood': neighbourhood_group,
            'Neighbourhood group': neighbourhood,
            'Room type': room_type,
            'Minimum nights': minimum_nights,
            'Predicted price': predicted_price}

# POST
@app.post('/predict/', tags=["predict_post"])
async def get_prediction(params: Prediction):
    train()
    predicted_price = predict(params.param1, params.param2, params.param3, params.param4)
    return {'Neighbourhood': params.param1,
            'Neighbourhood group': params.param2,
            'Room type': params.param3,
            'Minimum nights': params.param4,
            'Predicted price': predicted_price}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    uvicorn.run(app, host='0.0.0.0', port=port)

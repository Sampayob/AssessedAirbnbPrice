from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from joblib import load
from pydantic import  BaseModel
import uvicorn
import os

from model import train, predict

#initiate API
app = FastAPI(title='MadridxAirbnb assessed price predictor',
              description = '''This project aims to combine a web app and an API using Streamlit and FastAPI.
              The data comes from Murray Cox project Inside Airbnb and was goten the 13th of September, 2020.
                            ''',
              version="1.0.0")

class Prediction(BaseModel):
    param1: str
    param2: str
    param3: str
    param4: int

#Jinja2 template
#templates = Jinja2Templates(directory="templates")

@app.post('/predict')
async def get_prediction(params: Prediction):

    train()
    predicted_price = predict(params.param1, params.param2, params.param3, params.param4)
    return predicted_price


#if __name__ == '__main__':
#	uvicorn.run(app, host="127.0.0.1", port=8000)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    uvicorn.run(app, host='0.0.0.0', port=port)

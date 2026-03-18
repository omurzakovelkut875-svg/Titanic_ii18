from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import joblib

scaler = joblib.load('scaler (3).pkl')
model = joblib.load('model (1).pkl')

titanic_app = FastAPI()

class TitanicSchema(BaseModel):
    Pclass: int
    Sex: str
    Age: float
    Fare: float
    FamilySize: int
    Embarked: str


@titanic_app.post('/predict')
async def predict_titanic(titanic: TitanicSchema):
    data = titanic.dict()

    sex = 1 if data.pop('Sex') == 'female' else 0
    embarked = data.pop('Embarked')

    embarked_Q = 1 if embarked == 'Q' else 0
    embarked_S = 1 if embarked == 'S' else 0

    features = [
        data['Pclass'],
        sex,
        data['Age'],
        data['Fare'],
        data['FamilySize'],
        embarked_S
    ]

    scaled = scaler.transform([features])
    pred = model.predict(scaled)[0]

    result = 'Survived' if pred == 1 else 'Not Survived'

    return {"Answer": result}

if __name__ == "__main__":
    uvicorn.run(titanic_app, host="127.0.0.1", port=8001)


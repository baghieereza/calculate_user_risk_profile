from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class UserData(BaseModel):
    age: int
    dependents: int
    income: int
    marital_status: str
    risk_questions: list[int]
    house: Optional[dict] = None
    vehicle: Optional[dict] = None

@app.post("/calculate-risk-profile")
async def calculate_risk(user_data: UserData):

    #getting value
    age = user_data.age
    dependents = user_data.dependents
    income = user_data.income
    marital_status = user_data.marital_status
    risk_questions = user_data.risk_questions

    house = user_data.house or {}
    ownership_status = house.get('ownership_status', None)

    vehicle = user_data.vehicle or {}
    vehicle_year = vehicle.get('year', None)
    
    #checking base score
    base_score = sum(risk_questions)

    life_score = int(base_score)
    disability_score = int(base_score)
    home_score = int(base_score)
    auto_score = int(base_score)

    #calculate the risk
    if not income:
        disability_score = auto_score = home_score = 0
    if age > 60:
        disability_score = life_score = 0
    if age < 30:
        life_score -= 2
        disability_score -= 2
        home_score -= 2
        auto_score -= 2
    elif 30 <= age < 40:
        life_score -= 1
        disability_score -= 1
        home_score -= 1
        auto_score -= 1
    if income > 200000:
        life_score -= 1
        disability_score -= 1
        home_score -= 1
        auto_score -= 1
    if ownership_status == "mortgaged":
        home_score += 1
        disability_score += 1
    if dependents > 0:
        life_score += 1
        disability_score += 1
    if marital_status == "married":
        life_score += 1
        disability_score -= 1
    if vehicle_year and vehicle_year >= (2023 - 5):
        auto_score += 1

    def get_risk_type(score):
        if score <= 0:
            return "economic"
        elif score <= 2:
            return "regular"
        else:
            return "responsible"

    return {
        "auto": Get_risk_type(auto_score),
        "disability": Get_risk_type(disability_score),
        "home": Get_risk_type(home_score),
        "life": Get_risk_type(life_score)
    }
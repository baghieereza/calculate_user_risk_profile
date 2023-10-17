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
async def calculate_user_risk_profile(user_data: UserData):
    def map_to_profile(score):
        if score <= 0:
            return "economic"
        elif score <= 2:
            return "regular"
        else:
            return "responsible"

    # Extract user attributes
    age = user_data.age
    dependents = user_data.dependents
    income = user_data.income
    marital_status = user_data.marital_status
    risk_questions = user_data.risk_questions

    house = user_data.house or {}
    ownership_status = house.get('ownership_status', None)

    vehicle = user_data.vehicle or {}
    vehicle_year = vehicle.get('year', None)

    # Calculate base risk score
    base_score = sum(risk_questions)

    # Initialize risk scores for each line of insurance
    life_score = base_score
    disability_score = base_score
    home_score = base_score
    auto_score = base_score

    # Apply rules to calculate risk scores
    if not income:
        disability_score = auto_score = home_score = "ineligible"
    if age > 60:
        disability_score = life_score = "ineligible"
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

    return {
        "auto": map_to_profile(auto_score),
        "disability": map_to_profile(disability_score),
        "home": map_to_profile(home_score),
        "life": map_to_profile(life_score)
    }

from fastapi import FastAPI , Path , HTTPException , Query
import json
from fastapi.responses import JSONResponse
from pydantic import BaseModel ,Field  , computed_field
from typing import Annotated , Literal , Optional

class Patient(BaseModel):
    id: Annotated[str, Field(...,description="ID of the Patient in Database", example="P001")]
    name: Annotated[str, Field(...,description="Name of the Patient", example="John Doe")]
    age: Annotated[int, Field(...,gt=0,lt=120, description="Age of the Patient")]
    height: Annotated[float, Field(..., gt=0 , description="Height of the Patient in meters")]
    weight: Annotated[float, Field(...,gt=0, description="Weight of the Patient in kilograms")]
    gender: Annotated[Literal['Male', 'Female','Other'], Field(..., description="Gender of the Patient")]
    city: Annotated[str, Field(..., description="City of the Patient", example="New York")]
    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)

    @computed_field
    @property
    def bmi_category(self) -> str:
        bmi_value = self.bmi
        if bmi_value < 18.5:
            return "Underweight"
        elif 18.5 <= bmi_value < 24.9:
            return "Normal weight"
        elif 25 <= bmi_value < 29.9:
            return "Overweight"
        else:
            return "Obesity"

class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(None,description="Name of the Patient", example="John Doe")]
    age: Annotated[Optional[int], Field(None,gt=0,lt=120, description="Age of the Patient")]
    height: Annotated[Optional[float], Field(None, gt=0 , description="Height of the Patient in meters")]
    weight: Annotated[Optional[float], Field(None,gt=0, description="Weight of the Patient in kilograms")]
    gender: Annotated[Optional[Literal['Male', 'Female','Other']], Field(None, description="Gender of the Patient")]
    city: Annotated[Optional[str], Field(None, description="City of the Patient", example="New York")]

def load_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data
app=FastAPI()

def save_data(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file)

@app.get("/")
def hello():
    return {"message": "Patients Management System API"}

@app.get("/about")
def about():
    return {"message": "A fully functional API for managing patients data."}

@app.get("/view")
def view():
    data = load_json_file('patients.json')
    return data

@app.get("/view/{patient_id}")
def view_patient(patient_id: str = Path(..., description="ID of the Patient in Database", example="P001" )):
    data = load_json_file('patients.json')
    for patient_id in data:
            return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found")

@app.get("/sort")
def sort(sort_by: str = Query("height", description="Sort Patients by height , weight or bmi", example ="Height") , order : str =Query('asc',description="Sort in asc or desc order")):
     valid_Fields = ['height', 'weight', 'bmi']
     if sort_by.lower() not in valid_Fields:
         raise HTTPException(status_code=400, detail=f"Invalid sort field. Valid fields are: {', '.join(valid_Fields)}")

     if order not in ['asc', 'desc']:
         raise HTTPException(status_code=400, detail="Invalid order. Valid orders are: asc, desc")

     data = load_json_file('patients.json')
     sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by.lower(), 0), reverse=(order == 'desc'))

     return sorted_data

@app.post("/create")
def create_patient(patient: Patient):
    data = load_json_file('patients.json')

    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient with this ID already exists.")
    
    data[patient.id] = patient.model_dump(exclude={'id'})
    save_data(data, 'D:\ML Projects\FastAPI_Learning\patients.json')
    return JSONResponse(content={"message": "Patient created successfully."}, status_code=201)

@app.put("/update/{patient_id}")
def update_patient(patient_id: str, patient_update: PatientUpdate):
    data = load_json_file('patients.json')

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found.")

    existing_patient_data = data[patient_id]
    updated_data = patient_update.model_dump(exclude_unset=True)

    # Update the existing patient data with the new values
    for key, value in updated_data.items():
        existing_patient_data[key] = value
    existing_patient_data['id'] = patient_id
    patient_obj = Patient(**existing_patient_data)
    existing_patient_data = patient_obj.model_dump(exclude={'id'})
    data[patient_id] = existing_patient_data
    save_data(data, 'D:\\ML Projects\\FastAPI_Learning\\patients.json')
    return JSONResponse(content={"message": "Patient updated successfully."}, status_code=200)
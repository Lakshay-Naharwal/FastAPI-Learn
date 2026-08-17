from fastapi import FastAPI , Path
import json

def load_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data
app=FastAPI()


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
    return {"message": "Patient not found."}
from fastapi import FastAPI , Path , HTTPException , Query
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
    raise HTTPException(status_code=404, detail="Patient not found")

@app.get("/sort")
def sort(sort_by: str = Query(..., description="Sort Patients by Hight , Weight or BMI", example ="Height") , order : str =Query('asc',description="Sort in asc or desc order")):
     valid_Fields = ['Height', 'Weight', 'BMI']
     if sort_by not in valid_Fields:
         raise HTTPException(status_code=400, detail=f"Invalid sort field. Valid fields are: {', '.join(valid_Fields)}")

     if order not in ['asc', 'desc']:
         raise HTTPException(status_code=400, detail="Invalid order. Valid orders are: asc, desc")

     data = load_json_file('patients.json')
     sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=(order == 'desc'))

     return sorted_data
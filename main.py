from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from datetime import date
import os
import uvicorn
from fastapi.encoders import jsonable_encoder

from dotenv import load_dotenv


load_dotenv()

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Missing required environment variables")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)



class Student(BaseModel):
    id: int | None = None
    first_name: str
    last_name: str
    DOB: date
    grade: int
    created_at: date | None = None


class Teacher(BaseModel):
    id: int | None = None
    first_name: str
    last_name: str
    specialty: str = Field(..., alias="speaciality")
    DOB: date
    created_at: date | None = None

    class Config:
        allow_population_by_field_name = True

@app.post("/students/", response_model=Student)
def create_student(student: Student):
    # Use jsonable_encoder to convert date objects to strings
    student_data = jsonable_encoder(student, exclude_unset=True)
    response = supabase.table("records_student").insert(student_data).execute()
    if not response.data:
        raise HTTPException(status_code=400, detail="Failed to create student")
    return response.data[0]

@app.get("/students/", response_model=list[Student])
def get_students():
    response = supabase.table("records_student").select("*").execute()
    return response.data

@app.get("/students/{student_id}", response_model=Student)
def get_student(student_id: int):
    response = supabase.table("records_student").select("*").eq("id", student_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Student not found")
    return response.data[0]

@app.put("/students/{student_id}", response_model=Student)
def update_student(student_id: int, student: Student):

    student_data = jsonable_encoder(student, exclude_unset=True)
    response = supabase.table("records_student").update(student_data).eq("id", student_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Student not found or update failed")
    return response.data[0]

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    response = supabase.table("records_student").delete().eq("id", student_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Student not found or deletion failed")
    return {"deleted": True}


# Teacher CRUD operations


@app.post("/teachers/", response_model=Teacher)
def create_teacher(teacher: Teacher):
    teacher_data = jsonable_encoder(teacher, exclude_unset=True)
    response = supabase.table("records_teacher").insert(teacher_data).execute()
    if not response.data:
        raise HTTPException(status_code=400, detail="Failed to create teacher")
    return response.data[0]

@app.get("/teachers/", response_model=list[Teacher])
def get_teachers():
    response = supabase.table("records_teacher").select("*").execute()
    return response.data

@app.get("/teachers/{teacher_id}", response_model=Teacher)
def get_teacher(teacher_id: int):
    response = supabase.table("records_teacher").select("*").eq("id", teacher_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return response.data[0]

@app.put("/teachers/{teacher_id}", response_model=Teacher)
def update_teacher(teacher_id: int, teacher: Teacher):
    teacher_data = jsonable_encoder(teacher, exclude_unset=True)
    response = supabase.table("records_teacher").update(teacher_data).eq("id", teacher_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Teacher not found or update failed")
    return response.data[0]

@app.delete("/teachers/{teacher_id}")
def delete_teacher(teacher_id: int):
    response = supabase.table("records_teacher").delete().eq("id", teacher_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Teacher not found or deletion failed")
    return {"deleted": True}



result = supabase.table("records_teacher").select("*").execute()
print(result)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)








































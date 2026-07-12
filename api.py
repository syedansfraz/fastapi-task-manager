from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal, TaskModel, init_db

app = FastAPI()
init_db()

class TaskCreate(BaseModel):
    title: str
    deadline: str

class TaskUpdate(BaseModel):
    done: bool

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(TaskModel).all()
    return {"total": len(tasks), "tasks": tasks}

@app.post("/tasks")
def add_task(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = TaskModel(
        title=task.title,
        deadline=task.deadline,
        done=False
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {"message": "Task added", "task": new_task}

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_data: TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.done = task_data.done
    db.commit()
    db.refresh(task)
    return {"message": f"Task {task_id} updated", "task": task}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": f"Task {task_id} deleted"}
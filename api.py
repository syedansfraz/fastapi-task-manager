from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal, TaskModel, UserModel, init_db,get_db
from auth import hash_password, verify_password, create_access_token,get_current_user

app = FastAPI()
init_db()

class TaskCreate(BaseModel):
    title: str
    deadline: str

class TaskUpdate(BaseModel):
    done: bool

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(UserModel).filter(UserModel.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already registered")

    new_user = UserModel(
        username=user.username,
        hashed_password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully", "user_id": new_user.id}


@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token({"sub": db_user.username})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/tasks")
def get_tasks(db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    tasks = db.query(TaskModel).filter(TaskModel.user_id == current_user.id).all()
    return {"total": len(tasks), "tasks": tasks}

@app.post("/tasks")
def add_task(task: TaskCreate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    new_task = TaskModel(
        title=task.title,
        deadline=task.deadline,
        done=False,
        user_id=current_user.id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {"message": "Task added", "task": new_task}

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_data: TaskUpdate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    task = db.query(TaskModel).filter(TaskModel.id == task_id, TaskModel.user_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.done = task_data.done
    db.commit()
    db.refresh(task)
    return {"message": f"Task {task_id} updated", "task": task}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    task = db.query(TaskModel).filter(TaskModel.id == task_id, TaskModel.user_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": f"Task {task_id} deleted"}
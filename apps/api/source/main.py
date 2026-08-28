from fastapi import FastAPI,Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from apps.api.services.models import User, Todos
from apps.api.source.dependecies import get_db
from apps.api.pydantic_schemas.schemas import UserBase, TodoBase
from sqlalchemy import or_
from sqlalchemy.orm import Session
from apps.api.pydantic_schemas.response_schemas import UserResponse, TodoResponse
from apps.api.services.auth import pwd_context, create_access_token, verify_access_token
from apps.api.services.background_tasks import add_background_mail, remove_background_mail, add_daily_background_mail, add_weekly_background_mail, add_monthly_background_mail
from fastapi.middleware.cors import CORSMiddleware

 
app = FastAPI(description="A simple TODO application with user authentication and task management.")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://frontend-mytodo.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 

@app.get("/")
def home():
    return {"message": "Welcome to the TODO application"}



@app.post("/create_user", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserBase, db: Session = Depends(get_db)):
    print(user.password)
    print(len(user.password))
    print(len(user.password.encode("utf-8")))

    existing_user = db.query(User).filter(or_(User.username == user.username, User.user_email == user.user_email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already exists.")

    new_user = User(username=user.username, password= pwd_context.hash(user.password), user_email=user.user_email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid username or password.")

    access_token = create_access_token(data={"sub": user.username})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }



@app.post("/create_todo_once", status_code=status.HTTP_201_CREATED, response_model=TodoResponse)
def create_todo(todo: TodoBase, db: Session = Depends(get_db), current_user: str = Depends(verify_access_token)):
    user = db.query(User).filter(User.username == current_user).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    new_todo = Todos(title=todo.title, username=current_user, time=todo.time, is_completed=todo.is_completed)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    add_background_mail(to_email=user.user_email, subject=f"Reminder: {todo.title}", description=f"Your task '{todo.title}' is scheduled for {todo.time}.", send_time=todo.time, id=new_todo.id)
    return new_todo



@app.post("/create_todo_daily", status_code=status.HTTP_201_CREATED, response_model=TodoResponse)
def create_todo(todo: TodoBase, db: Session = Depends(get_db), current_user: str = Depends(verify_access_token)):
    user = db.query(User).filter(User.username == current_user).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    new_todo = Todos(title=todo.title, username=current_user, time=todo.time, is_completed=todo.is_completed)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    add_daily_background_mail(to_email=user.user_email, subject=f"Reminder: {todo.title}", description=f"Your task '{todo.title}' is scheduled for {todo.time}.", send_time=todo.time, id=new_todo.id)
    return new_todo


@app.post("/create_todo_weekly", status_code=status.HTTP_201_CREATED, response_model=TodoResponse)
def create_todo(todo: TodoBase, db: Session = Depends(get_db), current_user: str = Depends(verify_access_token)):
    user = db.query(User).filter(User.username == current_user).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    new_todo = Todos(title=todo.title, username=current_user, time=todo.time, is_completed=todo.is_completed)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    add_weekly_background_mail(to_email=user.user_email, subject=f"Reminder: {todo.title}", description=f"Your task '{todo.title}' is scheduled for {todo.time}.", send_time=todo.time, id=new_todo.id)
    return new_todo


@app.post("/create_todo_monthly", status_code=status.HTTP_201_CREATED, response_model=TodoResponse)
def create_todo(todo: TodoBase, db: Session = Depends(get_db), current_user: str = Depends(verify_access_token)):
    user = db.query(User).filter(User.username == current_user).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    new_todo = Todos(title=todo.title, username=current_user, time=todo.time, is_completed=todo.is_completed)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    add_monthly_background_mail(to_email=user.user_email, subject=f"Reminder: {todo.title}", description=f"Your task '{todo.title}' is scheduled for {todo.time}.", send_time=todo.time, id=new_todo.id)
    return new_todo


@app.get("/get_todos/{page_no}", status_code=status.HTTP_200_OK, response_model=list[TodoResponse])
def get_todos(page_no: int, page_size:int = 10, current_user: str = Depends(verify_access_token), db: Session = Depends(get_db)):
    skip = (page_no - 1 ) * page_size
    todos = db.query(Todos).filter(Todos.username == current_user).offset(skip).limit(page_size).all()
    if not todos:
        raise HTTPException(status_code=404, detail="No todos found for this user.")
    return todos


@app.get("/search_todo/{todo_name}", status_code=status.HTTP_200_OK, response_model=list[TodoResponse])
def search_todo(todo_name: str, current_user: str = Depends(verify_access_token), db: Session = Depends(get_db)):
    todos = db.query(Todos).filter(Todos.title.ilike(f"%{todo_name}%"), Todos.username == current_user).all()
    return todos


@app.put("/update_todo_status/{todo_id}", status_code= status.HTTP_201_CREATED)
def update_todo_status(todo_id: int, is_completed: bool, db: Session = Depends(get_db), current_user: str = Depends(verify_access_token)):
    todo = db.query(Todos).filter(Todos.id == todo_id, Todos.username == current_user).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found.")
    
    todo.is_completed = is_completed
    db.commit()
    return {"message": "Todo status updated successfully."}



@app.put("/update_todo/{todo_id}", status_code= status.HTTP_201_CREATED)
def update_todo(todo: TodoBase, todo_id: int, db: Session = Depends(get_db), current_user: str = Depends(verify_access_token)):
    existing_todo = db.query(Todos).filter(Todos.id == todo_id, Todos.username == current_user).first()
    if not existing_todo:
        raise HTTPException(status_code=404, detail="Todo not found.")

    remove_background_mail(id=todo_id)
    existing_todo.title = todo.title
    existing_todo.time = todo.time
    existing_todo.is_completed = todo.is_completed
    db.commit()
    user_mail = db.query(User).filter(User.username == current_user).first().user_email
    add_background_mail(to_email=user_mail, subject=f"Reminder: {todo.title}", description=f"Your task '{todo.title}' is scheduled for {todo.time}.", send_time=todo.time, id=todo_id)

    return {"message": "Todo updated successfully."}



@app.delete("/delete_todo/{todo_id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int, db: Session = Depends(get_db), current_user: str = Depends(verify_access_token)):
    todo = db.query(Todos).filter(Todos.id == todo_id, Todos.username == current_user).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found.")

    remove_background_mail(id=todo_id)
    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted successfully."}


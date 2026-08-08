from fastapi import FastAPI,Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models import User, Todos
from dependecies import get_db
from schemas import UserBase, TodoBase
from sqlalchemy.orm import Session
from response_schemas import UserResponse, TodoResponse
from auth import pwd_context, create_access_token, verify_access_token
from background_tasks import add_background_mail

 


app = FastAPI(description="A simple TODO application with user authentication and task management.")
 

@app.get("/")
def home():
    return {"message": "Welcome to the TODO application!"}


@app.post("/create_user", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserBase, db: Session = Depends(get_db)):
    print(user.password)
    print(len(user.password))
    print(len(user.password.encode("utf-8")))

    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists.")
    
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



@app.post("/create_todo", status_code=status.HTTP_201_CREATED, response_model=TodoResponse)
def create_todo(todo: TodoBase, db: Session = Depends(get_db), current_user: str = Depends(verify_access_token)):
    user = db.query(User).filter(User.username == current_user).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    new_todo = Todos(title=todo.title, username=current_user, time=todo.time, is_completed=todo.is_completed)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    add_background_mail(to_email=user.user_email, subject=f"Reminder: {todo.title}", description=f"Your task '{todo.title}' is scheduled for {todo.time}.", send_time=todo.time)
    return new_todo




@app.get("/get_todos", status_code=status.HTTP_200_OK, response_model=list[TodoResponse])
def get_todos(current_user: str = Depends(verify_access_token), db: Session = Depends(get_db)):
    todos = db.query(Todos).filter(Todos.username == current_user).all()
    if not todos:
        raise HTTPException(status_code=404, detail="No todos found for this user.")
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

    existing_todo.title = todo.title
    existing_todo.time = todo.time
    existing_todo.is_completed = todo.is_completed
    db.commit()
    return {"message": "Todo updated successfully."}


@app.delete("/delete_todo/{todo_id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int, db: Session = Depends(get_db), current_user: str = Depends(verify_access_token)):
    todo = db.query(Todos).filter(Todos.id == todo_id, Todos.username == current_user).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found.")
    
    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted successfully."}


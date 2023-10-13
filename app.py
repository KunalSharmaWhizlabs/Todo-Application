from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine, Column, BOOLEAN, Integer, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

Base = declarative_base()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'

class Todo(Base):
    __tablename__ ="todo"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    title = Column("title", VARCHAR(100))
    complete = Column("completed", BOOLEAN)

db = create_engine("sqlite:///mydb.db", echo=True)
Base.metadata.create_all(bind=db)
Session = sessionmaker(bind=db)
session = Session()

@app.route("/")
def home():
    # statement = select(Todo.id, Todo.title, Todo.complete)
    todo_list = session.query(Todo).all()
    return render_template("base.html", todo_list=todo_list)


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    session.add(new_todo)
    session.commit()
    return redirect(url_for("home"))


@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = session.query(Todo).filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    session.commit()
    return redirect(url_for("home"))


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = session.query(Todo).filter_by(id=todo_id).first()
    session.delete(todo)
    session.commit()
    return redirect(url_for("home"))

if __name__ == "__main__":
    # db.create_all()
    app.run(debug=True)

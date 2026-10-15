# Imports
from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


# My App
app = Flask(__name__)
Scss(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


# Data Class = Row of Data
class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self) -> str:
        return f"Task {self.id}"


# Home page
@app.route("/", methods=["GET", "POST"])
def index():
    # Add a Task
    if request.method == "POST":
        task_content = request.form["content"]
        new_task = MyTask(content=task_content, complete=0)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except:
            return "There was an issue adding your task"

    tasks = MyTask.query.order_by(MyTask.date).all()
    return render_template("index.html", tasks=tasks)


# Delete an Item
@app.route("/delete/<int:id>", methods=["GET", "POST"])
def delete(id: int):
    task_to_delete = MyTask.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return "There was a problem deleting that task"


# Update an Item
@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id: int):
    task_to_update = MyTask.query.get_or_404(id)

    if request.method == "POST":
        task_to_update.content = request.form["content"]

        try:
            db.session.commit()
            return redirect("/")
        except:
            return "There was a problem updating the task"

    return render_template('edit.html', task_to_update=task_to_update)


if __name__ in "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
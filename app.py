import sqlite3
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy  
from datetime import datetime 
app = Flask(__name__)
# Intializing SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todopy.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class todo(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(300),nullable=False)
    description = db.Column(db.String(500),nullable=False)
    date_created = db.Column(db.DateTime,default=datetime.now())

    def __repr__(self) ->str:
        return f"{self.id} - {self.title}"
@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "POST":
        title = request.form["task-title"]
        desc = request.form['task-desc']
        Todo = todo(title=title,description=desc)
        db.session.add(Todo)
        db.session.commit()
    context_list = todo.query.all()
    return render_template("index.html",context_list = context_list)
@app.route("/delete/<int:id>")
def delete(id):
    Todo = todo.query.filter_by(id=id).first()
    db.session.delete(Todo)
    db.session.commit()
    return redirect("/")
@app.route("/update/<int:id>",methods=["GET","POST"])
def update(id):
    if request.method == "POST":
        title = request.form['task-title']
        desc = request.form['task-desc']
        Todo = todo.query.filter_by(id=id).first()
        Todo.title = title
        Todo.description = desc
        print(Todo.title)
        print(Todo.description)
        db.session.add(Todo)
        db.session.commit()
        return redirect("/") 
       
    context_list = todo.query.filter_by(id=id).first()
    return render_template("update.html",context_list = context_list)

if __name__ == "__main__":
    app.run(debug=True)
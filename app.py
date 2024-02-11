from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_DATABASE_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model) :
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50), nullable = False)
    desc = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str :
        return f"{self.sno} -  {self.title}"
    

# Add this line to create the app context
app.app_context().push()


@app.route('/', methods = ["GET","POST"])
def welcome() :
    if request.method == "POST":
        todo_title = request.form['title']
        todo_desc = request.form['desc']
        todo = Todo(title= todo_title,desc = todo_desc)
        db.session.add(todo)
        db.session.commit()
    all_todo = Todo.query.all()
    return render_template('index.html',todo_data = all_todo)

@app.route('/update/<int:sno>',methods = ["GET","POST"])
def update(sno) :
    if request.method == "POST" :
        title = request.form['title']
        desc = request.form['desc']
        update_todo = Todo.query.filter_by(sno=sno).first()
        update_todo.title = title
        update_todo.desc = desc
        db.session.add(update_todo)
        db.session.commit()
        return redirect('/')

    update_todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo_data = update_todo)

@app.route('/delete/<int:sno>')
def delete(sno) :
    del_todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(del_todo)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__' :
    app.run(debug=True)
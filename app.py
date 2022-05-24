from flask import Flask, redirect, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:wube@localhost:5432/todo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

db.create_all()
class Todo(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return f"""<Todos>
                id:{self.id} 
                content:{self.content},
                completed: {self.completed} 
                date created: {self.date_created}"""

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "there was an error creating the task"    
    else:
        tasks = Todo.query.order_by('date_created').all()
        return render_template("index.html", tasks=tasks)




if __name__ == '__main__':
    app.run(debug=True)
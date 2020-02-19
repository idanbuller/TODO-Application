from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
# from blueprint_for_tasks import tasks_bp
from datetime import datetime
import math

app = Flask(__name__)


# Configs
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://user:password@localhost/todo-py'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Init SQLAlchemy
db = SQLAlchemy(app)


# Models
class Task(db.Model):
    __tablename__ = 'tasks'
    idTask = db.Column('idTask', db.Integer, primary_key=True)
    task = db.Column('task', db.String)
    status = db.Column('status', db.String, default='uncomplete')
    creation_date = db.Column('creation_date', db.DateTime, default=datetime.utcnow())

    def __init__(self, task):
        self.task = task


# Routes
allTasks = []


# Home page
@app.route('/')
def index():
    all_tasks = Task.query.all()
    return render_template('index.html', t=all_tasks)


# Create a new task
@app.route('/task', methods=['POST'])
def tasks():
    new_task = Task(request.form['task'])
    db.session.add(new_task)
    db.session.commit()
    return redirect('/', 302)


# Read a specific task
@app.route('/task/<id>', methods=['GET'])
def getTask(id):
    return id


# Update a task
@app.route('/updatetask/<taskID>', methods=['GET'])
def updateTask(taskID):
    the_task = Task.query.filter_by(idTask=taskID).first()

    return render_template('update.html', task=the_task)


@app.route('/do_updatetask', methods=['POST'])
def do_updatetask():
    update_task = Task.query.filter_by(idTask=request.form['taskID']).first()
    update_task.task = request.form['task']
    db.session.commit()

    return redirect('/', 302)


# Delete a task
@app.route('/deletetask/<taskID>', methods=['GET'])
def deleteTask(taskID):
    delete_task = Task.query.filter_by(idTask=taskID).first()
    db.session.delete(delete_task)
    db.session.commit()
    return redirect('/', 302)


@app.route('/complete/<taskID>')
def complete(taskID):
    complete_task = Task.query.filter_by(idTask=taskID).first()
    complete_task.status = 'complete'
    db.session.commit()
    return redirect('/', 302)


@app.route('/uncomplete/<taskID>')
def uncomplete(taskID):
    uncomplete_task = Task.query.filter_by(idTask=taskID).first()
    uncomplete_task.status = 'uncomplete'
    db.session.commit()
    return redirect('/', 302)


# Models 2
class Task_list(db.Model):
    __tablename__ = 'task_list'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String)
    status = db.Column('status', db.String, default='uncomplete')
    creation_date = db.Column('creation_date', db.DateTime, default=datetime.utcnow())
    idTask = db.Column('idTask', db.Integer)

def __init__(self, task):
    self.id = task

#Home Page
@app.route('/list_home_page/<idTask>', methods=['GET'])
def list_home_page(idTask):
    specific_id = Task_list.query.filter_by(idTask=idTask)
    return render_template('task_list_index.html', list=specific_id)


# add a new task
@app.route('/add/<idTask>', methods=['POST'])
def add(idTask):
    task_id = Task_list.query.get(idTask)
    new_task = Task_list(request.form['name'])
    db.session.add(new_task, task_id)
    db.session.commit()
    return "Row inserted"


# Read a specific task
@app.route('/gettask/<idTask>', methods=['GET'])
def get_task(idTask):
    return idTask


# Update a task
@app.route('/update/<id>', methods=['GET'])
def update(id):
    the_task = Task_list.query.filter_by(id=id).first()
    return render_template('update_list.html', name=the_task)


@app.route('/do_update', methods=['POST'])
def do_update():
    update_task = Task_list.query.filter_by(id=request.form['id']).first()
    update_task.task = request.form['task']
    db.session.commit()
    return redirect('/list_home_page', 302)


# Delete a task
@app.route('/delete/<id>', methods=['GET'])
def delete(id):
    delete_task = Task_list.query.filter_by(id=id).first()
    db.session.delete(delete_task)
    db.session.commit()
    return redirect('/list_home_page', 302)


@app.route('/completed/<id>')
def completed(id):
    complete_task = Task_list.query.filter_by(id=id).first()
    complete_task.status = 'complete'
    db.session.commit()
    return render_template('task_list_index.html')


@app.route('/uncompleted/<id>')
def uncompleted(id):
    uncomplete_task = Task_list.query.filter_by(id=id).first()
    uncomplete_task.status = 'uncomplete'
    db.session.commit()
    return render_template('task_list_index.html')


if __name__ == '__main__':
    app.run(debug=True)

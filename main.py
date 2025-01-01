from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    exp_value = db.Column(db.Integer, nullable=False)
    date_logged = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def index():
    total_exp = sum(task.exp_value for task in Task.query.all())
    tasks = Task.query.order_by(Task.date_logged.asc()).all()  
    # Fetch all tasks in descending order
    return render_template('index.html', total_exp=total_exp, tasks=tasks)

@app.route('/log', methods=['GET', 'POST'])
def log_task():
    if request.method == 'POST':
        task_name = request.form['task_name']
        exp_value = int(request.form['exp_value'])
        new_task = Task(name=task_name, exp_value=exp_value)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('log_task.html')

## this below didn't work
# if __name__ == '__main__':
#     db.create_all()  # Set up the database if not already created
#     app.run(host='0.0.0.0', port=81)  # Required for Replit

if __name__ == '__main__':
    with app.app_context():  # Create an application context
        db.create_all()  # Set up the database if not already created
    app.run(host='0.0.0.0', port=81)  # Required for Replit
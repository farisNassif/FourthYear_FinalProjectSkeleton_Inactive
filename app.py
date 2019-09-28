import pymongo
from pymongo import MongoClient
from flask import Flask, render_template, url_for, request, redirect, Blueprint
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# MongoString generated on my https://cloud.mongodb.com account
cluster = MongoClient("mongodb+srv://faris:loughrea@skeletonforproject-a2j6y.mongodb.net/test?retryWrites=true&w=majority")

app = Flask(__name__)

# Where the database is located
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
db2 = cluster["testdb"]
collection = db2["testcollection"]

# Schema for SQLite
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # Return a string everytime make a new element
    def __repr__(self):
        return '<Task %r>' % self.id

# Index route so when I browse to the url it doesn't 404
@app.route('/', methods=['Post', 'GET'])
def index():
    # Whenever someone wants to add some input 
    if request.method == 'POST':
        # Preparing data to be inserted into SQLite
        task_content = request.form['content']
        # Assigning everything in the Schema for SQLite to new_task. id and date_created don't require input so 'content' only needs passing.
        new_task = Todo(content=task_content)
        # Preparing data to be inserted into mongo
        postForCollection = {"content":request.form['content'],"date":datetime.now()}
        try:        
            # Posting data stored above to mongo
            collection.insert_one(postForCollection)
            # Data below is stored in SQL
            db.session.add(new_task)
            db.session.commit()
            # Once above commits are made return back to index page
            return redirect('/')
        # Error Handling
        except: 
            # If for some reason data couldn't be commit throw an error message
            return 'Issue adding input'
    else:
        # Looks at database contents in order they were created and show all of them
        tasks = Todo.query.order_by(Todo.date_created).all()
        # Base Page
        return render_template('index.html', tasks=tasks)

# Delete route, delete by id
@app.route('/delete/<int:id>')
def delete(id):
    # Attempt to get task by id or 404 if it doesn't exist
    task_to_delete = Todo.query.get_or_404(id)
    try: 
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Deleting didnt work :( '

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    # Attempt to get task by id or 404 if it doesn't exist
    task = Todo.query.get_or_404(id)
    
    if request.method == 'POST':
        # Setting above tasks content to the content in the update input field
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Updating didnt work :('
    else:
        return render_template('update.html', task=task)

if __name__ == "__main__":
    # If theres any errors they'll pop up on the page
    app.run(debug=True)
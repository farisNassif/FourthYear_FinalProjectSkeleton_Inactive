import pymongo
from pymongo import MongoClient
from flask import Flask, render_template, url_for, request, redirect, Blueprint
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from bson.objectid import ObjectId

# MongoString generated on my https://cloud.mongodb.com account
cluster = MongoClient("mongodb+srv://faris:loughrea@skeletonforproject-a2j6y.mongodb.net/test?retryWrites=true&w=majority")

app = Flask(__name__)

db2 = cluster["testdb"]
collection = db2["testcollection"]

# Index route so when I browse to the url it doesn't 404
@app.route('/', methods=['Post', 'GET'])
def index():
    # Whenever someone wants to submit
    if request.method == 'POST':
        # Preparing data to be inserted into mongo
        postForCollection = {"content":request.form['content'],"date_created":datetime.now().replace(microsecond=0)}
        try:        
            # Posting data stored above to mongo
            collection.insert_one(postForCollection)
            # Once above commits are made return back to index page
            return redirect('/')
        # Error Handling
        except: 
            # If for some reason data couldn't be commit throw an error message
            return 'Issue adding input'
    else:
        # Retrieving Mongo data and putting it in a list
        mongoData = list(collection.find().sort('date_created', pymongo.ASCENDING))
        # Base Page
        return render_template('index.html', tasks=mongoData)

# Delete route, remove from MongoDB by id
@app.route('/delete/<string:_id>')
def delete(_id):
    try: 
        collection.delete_one( {'_id': ObjectId(_id) } ) 
        return redirect('/')
    except:
        return 'Deleting didnt work :( '

@app.route('/update/<string:_id>', methods=['GET', 'POST'])
def update(_id):
    # Finding the record the user wants to update and storing the object in recordToEdit
    recordToEdit = collection.find_one( {'_id': ObjectId(_id) } )
    if request.method == 'POST':
        # userUpdate is whatever the person enters on the input page
        userUpdate = request.form['content']
        try:
            # Update by id, insert newly input data
            collection.update_one({ "_id": ObjectId(_id) }, { "$set": { "content": userUpdate } } )
            return redirect('/')
        except:
            return 'Updating didnt work :('
    else:
        return render_template('update.html', task=recordToEdit)

if __name__ == "__main__":
    # If theres any errors they'll pop up on the page
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

client = MongoClient()
db = client.CharityTracker
donations = db.donations

app = Flask(__name__)

@app.route('/')
def charity_index(): 
    return render_template("charity_index.html", donations=donations.find())

@app.route('/donations/new')
def donation_new():
    return render_template('donations_new.html')

@app.route('/donations', methods=['POST'])
def donation_submit():
    donation = {
        'name': request.form.get('charity-name'),
        'amount': request.form.get('amount'),
        'date': request.form.get('date'),
      }
    donations.insert_one(donation)
    return redirect(url_for('charity_index'))

if __name__ == '__main__':
    app.run(debug=True)
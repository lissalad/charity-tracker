from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
import certifi

host = os.environ.get("DB_URL")
client = MongoClient(host=host, tlsCAFile=certifi.where())
db = client.CharityTracker
donations = db.donations
charities = db.charities

app = Flask(__name__)

# ----------- PAGES ----------------------------------------- #
@app.route('/')
def charity_index():
    donates=list(donations.find())
    for i in range(len(donates)):
      donates[i]['amount'] = float(donates[i]['amount'])
    donates.sort(key=lambda x: x['date'], reverse=False)
    return render_template("charity_index.html", donations=donates)

@app.route('/charities')
def charities_show():
    chair = charities.find()
    return render_template("charities_show.html", charities=chair)

@app.route('/charities/new')
def charities_new():
    return render_template("charity_new.html")

@app.route('/donations')
def donations_show():
    donates=list(donations.find())
    for i in range(len(donates)):
      donates[i]['amount'] = float(donates[i]['amount'])
    donates.sort(key=lambda x: x['date'], reverse=False)
    return render_template("donations_show.html", donations=donates)

@app.route('/donations/new')
def donation_new():
    chair = list(charities.find())
    return render_template('donations_new.html', charities=chair)

@app.route('/charities', methods=['POST'])
def charity_create():
  charity = {
    'name': request.form.get('name'),
    'website': request.form.get('website'),
    'description': request.form.get('description'),
    'total': 0
    }
  charities.insert_one(charity)
  return redirect(url_for('charities_show'))

@app.route('/donations', methods=['POST'])
def donation_create():
    name = request.form.get('charity-name')
    charity = charities.find_one({'name': name})
    donation = {
        'charity_id': charity['_id'],
        'name': request.form.get('charity-name'),
        'website': charity['website'],
        'amount': float(request.form.get('amount')),
        'date': request.form.get('date'),
      }
    donations.insert_one(donation)
    total = donation['amount'] + charity['total']
    charities.update_one({'_id': donation['charity_id']}, {'$set':{'total':total}})
    print(charity['total'])
    return redirect(url_for('donations_show'))

@app.route('/donations/<donation_id>/remove', methods=['POST'])
def donation_del(donation_id):
    donations.delete_one({'_id': ObjectId(donation_id)})
    return redirect(url_for('donations_show'))

@app.route('/charities/<charity_id>/remove', methods=['POST'])
def charity_del(charity_id):
    charities.delete_one({'_id': ObjectId(charity_id)})
    return redirect(url_for('charities_show'))







if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, request, render_template
from pymongo import MongoClient
from datetime import datetime
import os
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

# Retrieve environment variables
mongo_uri = os.environ.get('MONGO_URI')
mongo_port = int(os.environ.get('MONGO_PORT'))  # Convert to int
mongo_user = os.environ.get('MONGO_USER')
mongo_pass = os.environ.get('MONGO_PASS')

# MongoDB connection
client = MongoClient(
    host=mongo_uri,
    port=mongo_port,
    username=mongo_user,
    password=mongo_pass,
    authSource="admin"
)
db = client['users']  # Use 'users' database

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        timestamp = datetime.now()
        # Inserting data into MongoDB
        db.users.insert_one({'name': name, 'timestamp': timestamp})
        return 'Name "{}" added to the database with timestamp: {}'.format(name, timestamp)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=False) 

from datetime import datetime
import os
import ssl
from flask import Flask
from flask.globals import request
from flask.templating import render_template
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()


def create_app():
    app = Flask(__name__)
    client = MongoClient(os.environ.get('MONGODB_URI'), ssl_cert_reqs=ssl.CERT_NONE)
    app.db = client.microblog


    @app.route("/", methods=["GET", 'POST'])
    def home():
        for e in app.db.entries.find({}):
            print(e)

        if request.method == 'POST':
            entry_content = request.form.get('content')
            formatted_date = datetime.today().strftime('%Y-%m-%d')
            app.db.entries.insert({"content": entry_content, "date": formatted_date})

        entries_with_dates = [
            (
                entry["content"],
                entry["date"],
                datetime.strptime(entry["date"], '%Y-%m-%d').strftime("%b, %d")
            )
            for entry in app.db.entries.find()
        ]

        return render_template("home.html", entries=entries_with_dates)

    return app
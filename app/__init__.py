from flask import Flask

app = Flask(__name__)
app.secret_key = 'supersecretkey'

from app import routes
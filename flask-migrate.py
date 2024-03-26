from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ugamvnpf:1MpfujWOdVdmpKYxBx8Bpxh7yt5BPmLh@raja.db.elephantsql.com/ugamvnpf'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

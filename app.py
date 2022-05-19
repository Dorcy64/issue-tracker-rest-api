from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'eoiicneu9rbu973284hb20bdu2803h2b8ub937b4397b379b3789'

# connect the project to a database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bugs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


if __name__ == "__main__":
    from controllers import api
    app.register_blueprint(api)
    app.run(host='0.0.0.0', port=5000, debug=True)

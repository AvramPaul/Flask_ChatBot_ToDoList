from flask import Flask
from flask_scss import Scss

from models import db
from routes.chat import chat_bp
from routes.home import home_bp
from routes.tasks import tasks_bp


app = Flask(__name__)
Scss(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(home_bp)
app.register_blueprint(tasks_bp)
app.register_blueprint(chat_bp)


if __name__ in "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
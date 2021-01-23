from flask import Flask
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand

from utils import sql_utils

host = sql_utils.getHost()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = sql_utils.getDBURLFromHost(host)

db = SQLAlchemy(app)
db.init_app(app)

migrate = Migrate(app, db)
migrate.init_app(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()

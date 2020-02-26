# In questo file sono state inserite le configurazioni dell'app, del db
# e la registrazione del namespace dell'api.
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restplus import Api
import traceback

app = Flask(__name__)

# Dopo aver creato un'istanza della classe Flask
# creo un wrapper dell'ORM SQLALchemy.
# Definisco poi una variabile d'ambiente che contiene, per ora, l'url relativo
# del db sqlite. Questo deve essere cambiato, in seguito, col db postgress.

db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../../site.db'

# Per poter attuare delle modifiche aldb in corso d'opera,
# istanzio anche la classe Migrate

migrate = Migrate(app, db)

# I comandi per creare il db utilizzando flask-migrate sono:
# flask db init, flask db migrate e flask db upgrade.
# Questi però non sono sufficenti se non si aggiunge il comando:
# db.create_all()

db.create_all()

# Per formattare la nostra app sulle sembianze di una RESTFUL API abbiamo 
# necessità della classe wrapper Api.
 
api = Api(app, version='1.0', title='Sample Questionari_Insert API',
    description='API')

# In quanto è buona prassi dividere l'app in moduli (in questo caso secondo il
# modello MVC), è necessario importare il namespace e registrarlo.

from app.controllers import users

api.add_namespace(users)

#P.S: si succerisce di continuare la lettura dei commenti sul file models.py
# In questi modelli sono definite le classi che rispecchiano 
# la struttura del db.
# Benchè questo microservizio non effettua modifiche alle tabelle
# relative ai quiz. Essendo il db relazionale. E necessario
# costruire tutte le tabelle assieme.
# La tabella che effettivamente verrà sfruttata è quella User.
# Tale tabella ha infatti annesso anche un metodo.
# Il metodo asDict, ci servirà infatti per restituire un formato
# idoneo nelle nostre api.
# I notri modelli ereditano dalla classe Model, presente in SQLAlchemy.
# Sono pertanto conformi, ad essere tradotti in tabelle 
# di un db relazionale.

from app import db

# Il modello User è una normale tabella che contine le credenziali dell'utente.
# E relazionata uno a molti con la tabella Questionario.
# In modo da consentire ad un utente di creare più quiz.
# Inoltre, questa classe, contiene un campo status.
# Tale campo è stato inserito qualora un utente volesse essere eliminato.
# Essendo un'app di quiz, sarebbe opportuno, che in caso un utente voglia
# eliminare il suo account, i quiz che ha creato, possano restare a disposizione.
# Il campo status verrà quindi cambiato in 'deleted', in ogni utente
# eliminato, ma i suoi quiz potranno ancora essere disponibili.
# La query degli user potrà poi essere effettuata solo  sugli utenti attivi.

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=True, unique=True)
    password = db.Column(db.String, nullable=True, default='https://shmector.com/_ph/4/184260380.png')
    status = db.Column(db.String, nullable=False, default='active')
    questionari = db.relationship('Questionario', backref='author', lazy=True)

    def asDict(self):
        return { 'id' : self.id,
                 'name' : self.name,
                 'email' : self.email,
                 'password' : self.password
                }

# Le tabelle relative ai questionari sono 3.
# Questionario:
#   contiene esclusivamente il titolo del questionario ed l'id dell'user
#   che ha creato il questionario. E inoltre relazionata 1 a molti con la tabella
#   Domanda. In questo modo ogniquestionario può avere più domande.
# Domanda: 
#   contiene il testo della domandae l'id del questionario a cui è associata.
#   E relazionata uno a molti con la tabella risposta. In questo modo è 
#   possibile assegnare più di una risposta ad ogni domanda e quindi creare un
#   quiz a risposta multipla.
# Risposta:
#   contiene il testo della risposta e l'indicazione della sua validità o meno.
#   Qualora la risposta sia corretta il campo esatta dovra essere True.
#   Mentre sarà False in caso contrario.
#   Dovrà infine contenere l'id della domandaa cui è associata. 


class Questionario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titolo = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),  nullable=False)
    domande = db.relationship('Domanda', backref='questionario', lazy=True)

class Domanda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    domanda = db.Column(db.String, nullable=False)
    questionario_id = db.Column(db.Integer, db.ForeignKey('questionario.id'),  nullable=False)
    risposte = db.relationship('Risposta', backref='domanda', lazy=True)

class Risposta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    risposta = db.Column(db.String, nullable=False)
    esatta = db.Column(db.Boolean, nullable=False)
    domanda_id = db.Column(db.Integer, db.ForeignKey('domanda.id'),  nullable=False)


# P.S. proseguire la lettura dei commenti e delcodice nel file controllers.py
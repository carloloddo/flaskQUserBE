# In questo file sono definiti gli endpoint dell' API.

from flask import jsonify, request
from app import db, app, api
from flask_restplus import Resource, fields, reqparse
import traceback
from app.models import User

# Defizizione del namespace.
# Ogni endpoint associato al namespace user,
# avrà come url iniziale: nome_dominio + /api/v1.0/users

users = api.namespace('api/v1.0/users',description='CRUD operation for users')

# L'userModel non è necessario ma è utile. Questo infatti 
# consente di richiedere al client che farà la chiamata api, post o put, di
# inviare un json dell'esatto formato definito qui sotto.
# In caso il json non rispetti questo formato la chiamata verrà bloccata.

userModel = users.model('userModel', {
    'name' : fields.String(required=True, validate=True),
    'password' : fields.String(required=True, validate=True),
    'email' : fields.String(required=True, validate=True)
    }
)

# I parser servono a richiedere dei parametri nella forma:
# es ../users?active=true 
# In questo caso serve a richiedere se si vogliono utenti con stato 'active'.

parserStatus = reqparse.RequestParser()
parserStatus.add_argument('active',type=bool)

# Questo primo endpoint non richiede id. 
# E quindi generale e può essere chiamato in pagine che non necessitano il login.
# Sono associate ad esso due chiamate http.
# GET:
#   Restituisce la lista utenti attivi se l'argomento richiesto è true
#   altrimenti restituisce tutti gli utenti.
# POST:
#   Registra un utente nel db e restituisce i dati dell'utente postato
#   grazie alla funzione asDict definita nella classe User e alla funzione
#   di Flask jsonify.

@users.route('')
class General_users_requests(Resource):
    @users.expect(parserStatus)
    def get(self):
        '''get all users'''
        status = request.args.get('active')
        status = str(status)
        print(status)
        if status == 'true':
            users = User.query.filter_by(status='active')
            response={}
            response['data']=[]
            for user in users:
                response['data'].append(user.asDict())
            return jsonify(response)
        users = User.query.all()
        response={}
        response['data']=[]
        for user in users:
            response['data'].append(user.asDict())
        return jsonify(response)

    @users.expect(userModel, validate=True)
    def post(self):
        '''create a new user'''
        #create a new record in the DB
        data = request.get_json()
        name_request = data.get("name")
        email_request = data.get("email")
        password_request = data.get('password')
        u = User(name=name_request, email=email_request, password=password_request)
        db.session.add(u)
        db.session.commit()
        return jsonify(u.asDict())

# In questo endpoint è richiesto l'id nell'url.
# Nella forma: es. ../api/v1.0/users/1
# Vi sono associate 3 chiamate html:
# GET: restituisce i dati del singolo utente,
#   con id uguale a quello richiesto nell'url,
#   se presente.
# PUT: modifica i dati dell'utente.
# DELETE: cambia lo stato dell'utente in 'deleted'

@users.route('/<int:user_id>')
class Single_user_requests(Resource):
    def get(self, user_id):
        '''get a single user'''
        user =  User.query.get(user_id)
        if not user:
            return 'U-ser not found', 404
        return jsonify(user.asDict())

    @users.expect(userModel, validate=True)
    def put(self,user_id):
        '''update a user'''
        try:
            data = request.get_json()
            name_request = data.get("name")
            email_request = data.get("email")
            password_request = data.get("password")
            u = User.query.filter_by(id = user_id).first()
            if(u is None):
                return 'user not in DB', 404
            u.name = data['name'] if data['name'] else u.name
            u.password = data['password'] if data['password'] else u.password
            u.email =  data['email'] if data['email'] else u.email
            db.session.commit()
            return jsonify(u.asDict())
        except:
            app.logger.error(traceback.format_exc())
            return 'Error server side', 500

    def delete(self, user_id):
        '''deletes a user '''
        try:
            u = User.query.filter_by(id = user_id).first()
            if (u is None):
                return 'User not found', 404
            u.status = 'deleted'
            db.session.commit()
            return  'User status change to deleted!', 204
        except:
            app.logger.error(traceback.format_exc())
            return 'Error server side', 500

# In questo endpoint è richiesto l'email e la password dell'utente.
# Questo può essere utile per un login.
# GET: 
#   restituisce i dati dell'utente qualora la mail sia presente
#   nel db e la password relativa a questa coincida con
#   quella inserita nell'url.
# N.B. mandare password nell'url è possibile solo se queste siano
#    state prima criptate.
#    Qui per ora non è stato implementato nessun controllo di 
#    questo tipo.

@users.route('/<string:email>/<string:password>')
class GET_User(Resource):
    def get(self,email,password):
        '''get user matching his email and his password'''
        user = User.query.filter_by(email=email).first()
        if not user:
           return 'User Not Found', 404
        elif user.password != password:
           return 'Wrong Password', 400
        return jsonify(user.asDict())
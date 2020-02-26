# Questo è un microservizio API, sviluppato in Flask, che fornisce le
# basiche funzioni di recupero e registrazione utente (CRUD).
# Tale servizio si occupa, inoltre, della creazione del db.
# La struttura di quest'app è del tipo MVC.
# Nel pacchetto app si trovano i models e i controllers.
# La parte view è gestita dal servizio esterno swagger.
# Questo è possibile grazie all'utilizzo di flask-restplus.
# La configurazione dell'app è stata inserita all'interno del file  __init__.py
# presente nella cartella app.
# Essendo questo il file che deve essere mandato in run,
# importiamo dal package app, l'istanza app di Flask.
# Quindi lanciamo l'app.
# In quanto i microservizi sono due ( Users e Quizs ) e li stiamo sviluppando
# assieme, è opportuno cambiare il numero di porta ad uno di essi.
# In questo modo, entrambi potranno essere avviati in locale.

from app import app

if __name__ == '__main__':
    app.run(debug=True,port=8000)

# P.S:proseguire la lettura dei commenti sul file __init__.py
# MediAnalyserPOC

### New server setup

1. install requirements with pip

'pip3 install -r requirements.txt'

2. install en_core_web_sm

'python3 -m spacy download en_core_web_sm'

3. update pg_hba file:

in database type

'show hba_file;'

open file, and edit line

'local all all peers'
\*other lines may also have to be changed

set to

'local all all trust'

4. install cronjobs

5. install nginx server

6. grant permissions:

'sudo chown jean:jean /var/run/'

7. install guincorn server

### Concept of the app

1. Get Articles (once, weekly, daily, ...)

    a. scraping & parsing

    b. API access

    c. save to DB!!!

2. Recognise keywords and main topic

    a. TF-IDF

    b. ???

3. Group with other of the same topic

    a. Main topic matching

    b. Hierarchy (decision tree?)

4. Find divergences

    a. diff on keyword set

    b. difference of opinion

    c. difference of data sources

    d. difference in

5. Represent articles and divergences

### À explorer

agressivité
orientation politique

ploting
clustering, analyse multifactorielle sémantique points communs
recommendation articles qui couvrent tout le sujet (2-3 de divers opinions)

story instagram (titre, nom journal, phrase clé) pour différents articles, story suivant -> thème intéressant
titre, citation venant de l'article

Revue de presse
Avoir les opinions

Huffington post vs France Inter
différents opinions sur un même sujet politique intérnationnal

Plongeon sur un topic
Références historiques (quelques semaines)

Composition personnelle de revue de presse

People? Meme catégories que dans les journeaux: sport,
Devanture de kioscke de journal avec toutes les unes

## Usefull tutorials

### SQLAlchemy

https://hackersandslackers.com/python-database-management-sqlalchemy/

https://hackersandslackers.com/sqlalchemy-data-models/

https://hackersandslackers.com/database-queries-sqlalchemy-orm/

### NLP

https://spacy.io/usage/spacy-101

in particular

https://spacy.io/usage/spacy-101#annotations-pos-deps

### Word2Vec with Gensim

https://www.kaggle.com/pierremegret/gensim-word2vec-tutorial

### TF-IDF Vectorisation

https://towardsdatascience.com/tf-idf-explained-and-python-sklearn-implementation-b020c5e83275

### Mail service

https://realpython.com/python-send-email/

https://blog.mailtrap.io/send-emails-with-gmail-api/

https://developers.google.com/gmail/api/guides/push

### Google Cloud Engine

https://cloud.google.com/sql/docs/mysql/connect-app-engine-standard

https://cloud.google.com/secret-manager/docs/overview

### Flask app with gUnicorn and nginx

https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04

https://www.datadoghq.com/blog/nginx-502-bad-gateway-errors-gunicorn/

https://certbot.eff.org/lets-encrypt/debianbuster-nginx

https://flask.palletsprojects.com/en/1.1.x/quickstart/

### Possible News Sources

https://about.proquest.com/products-services/news-newspapers/Global-Breaking-Newswires.html

https://about.proquest.com/products-services/news-newspapers/ProQuest-Recent-Newspapers.html

https://about.proquest.com/products-services/news-newspapers/Newspaperscom-Library-Edition.html

https://about.proquest.com/products-services/news-newspapers/?selectFilter-search=Public&selectFilterTwo-search=News+and+Issues

### Network

https://linuxconfig.org/how-to-configure-static-ip-address-on-ubuntu-18-04-bionic-beaver-linux

https://netplan.io/examples/

https://www.ubuntu18.com/ubuntu-change-ssh-port/

http://www.artdecoded.net/blog/how-to-change-the-ssh-port-in-mac-os-x/

### Data Visualisation

https://medium.com/@rovai/from-data-to-graph-a-web-jorney-with-flask-and-sqlite-6c2ec9c0ad0

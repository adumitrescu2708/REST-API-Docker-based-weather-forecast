
"""
    Dumitrescu Alexandra 343 C1 - SPRC - December 2023
"""

import datetime
from flask_sqlalchemy import SQLAlchemy

# create a database
db = SQLAlchemy()

# Tari table
class Tari(db.Model):
    __tablename__ = "Tari"
    
    # id is the primary key
    id          = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    # name should be unique
    nume_tara   = db.Column('nume_tara', db.String, unique=True)
    latitudine  = db.Column('latitudine', db.FLOAT)
    longitudine = db.Column('longitudine', db.FLOAT)
    
    def __init__(self, nume_tara, latitudine, longitudine):
        self.nume_tara      = nume_tara
        self.latitudine     = latitudine
        self.longitudine    = longitudine
        
# Orase table        
class Orase(db.Model):
    __tablename__ = "Orase"
    
    # id is primary key
    id          = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    # id_tara is foreign key with Tari table
    id_tara     = db.Column('id_tara', db.Integer, db.ForeignKey('Tari.id', ondelete='CASCADE'))
    nume_oras   = db.Column('nume_oras', db.String)
    latitudine  = db.Column('latitudine', db.FLOAT)
    longitudine = db.Column('longitudine', db.FLOAT)
    
    __table_args__  = (db.UniqueConstraint("id_tara", "nume_oras"), )
    
    def __init__(self, id_tara, nume_oras, latitudine, longitudine):
        self.id_tara = id_tara
        self.nume_oras = nume_oras
        self.latitudine = latitudine
        self.longitudine = longitudine
    
# Temperaturi table    
class Temperaturi(db.Model):
    __tablename__ = "Temperaturi"
    
    # id is primary key
    id          = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    valoare     = db.Column('valoare', db.FLOAT)
    timestamp   = db.Column('timestamp', db.DateTime, default=datetime.datetime.utcnow)
    # id_oras is foreign key with Orase table
    id_oras     = db.Column('id_oras', db.Integer, db.ForeignKey('Orase.id', ondelete='CASCADE'))
    
    __table_args__  = (db.UniqueConstraint("id_oras", "timestamp"), )
    
    def __init__(self, valoare, id_oras):
        self.valoare = valoare
        self.id_oras = id_oras
import sqlite3
import hashlib
from flask import Flask, session

class auth:
    def __init__(self, app):
        self.app = app
        self.app.secret_key = "secret_123"

    def SignUp(self,username, password):
        self.connection = sqlite3.connect("car_prediction.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute(f'''INSERT INTO Users(username, passwordHash) 
                        VALUES ("{username}","{hashlib.sha256(password.encode()).hexdigest()}")''')
        self.connection.commit()
        self.connection.close()

    def Login(self, username, password):
        self.connection = sqlite3.connect("car_prediction.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute(f'''SELECT passwordHash FROM Users WHERE username = "{username}"''')
        actual_password_Hash = self.cursor.fetchone()
        self.connection.close()
        if not actual_password_Hash: return False # return false for empty list
        session["username"] = username
        session['logged_in'] = True
        return hashlib.sha256(password.encode()).hexdigest() == actual_password_Hash[0]
    
    def Is_already_logged_in(self):
        return session.get('logged_in'), session.get('username')
    
    def Logout(self):
        session.clear()
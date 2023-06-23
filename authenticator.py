import sqlite3
import hashlib
from flask import session
import requests

class auth:
    def __init__(self, app):
        self.app = app
        self.app.secret_key = "secret_123"

    def SignUp(self,username, password):
        self.connection = sqlite3.connect("car_prediction.db")
        self.cursor = self.connection.cursor()
        try:
            self.cursor.execute(f'''INSERT INTO Users(username, passwordHash) 
                            VALUES ("{username}","{hashlib.sha256(password.encode()).hexdigest()}")''')
            self.connection.commit()
            self.connection.close()
            return True
        except sqlite3.IntegrityError:
            return False

    def Login(self, username, password):
        self.connection = sqlite3.connect("car_prediction.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute(f'''SELECT passwordHash FROM Users WHERE username = "{username}"''')
        actual_password_Hash = self.cursor.fetchone()
        self.connection.close()
        if not actual_password_Hash: return False # return false for empty list
        return hashlib.sha256(password.encode()).hexdigest() == actual_password_Hash[0]
    
    def Is_already_logged_in(self):
        return {"logged_in" : session.get('logged_in'), "username" : session.get('username')}
    
    def create_session(self, username):
        session["username"] = username
        session['logged_in'] = True
    
    def Logout(self):
        session.clear()

    def sent_discord_verification_message(self,discord_webhook_url, verification_code):
        data = {
            'content': f'Verification code for LeCun Car Prediction Login is: {verification_code}'
        }

        response = requests.post(discord_webhook_url, json=data)
        if response.status_code == 204: return True
        return False
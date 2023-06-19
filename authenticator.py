import sqlite3
import hashlib

class auth:
    def __init__(self):
        self.connection = sqlite3.connect("car_prediction.db")
        self.cursor = self.connection.cursor()

    def SignUp(self,username, password):
        self.cursor.execute(f'''INSERT INTO Users(username, passwordHash) 
                        VALUES ("{username}","{hashlib.sha256(password.encode()).hexdigest()}")''')
        self.connection.commit()
        self.connection.close()

    def Login(self, username, password):
        self.cursor.execute(f'''SELECT passwordHash FROM Users WHERE username = "{username}"''')
        actual_password_Hash = self.cursor.fetchone()
        self.connection.close()
        if not actual_password_Hash: return False # return false for empty list
        return hashlib.sha256(password.encode()).hexdigest() == actual_password_Hash[0]
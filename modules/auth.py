from flask_login import UserMixin

users = {
    "admin": {"password": "admin123", "role": "admin"},
    "user": {"password": "user123", "role": "user"},
    "guest": {"password": "guest123", "role": "guest"}
}

class User(UserMixin):
    def __init__(self, username):
        self.id = username
        self.password = users[username]["password"]
        self.role = users[username]["role"]

def get_user(username):
    if username in users:
        return User(username)
    return None

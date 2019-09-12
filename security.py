users = {
    "id": 1,
    "username": "admin",
    "password": "password"
}

usersame_mapping = {"admin": {
    "id": 1,
    "username": "admin",
    "password": "password"
    }
}

userid_mapping = {"1": {
    "id": 1,
    "username": "admin",
    "password": "password"
    }
}
 

def authenticate(username, password):
    user = userid_mapping.get(username, None)
    if user and user.password == password:
        return user


def identity(payload):
    user_id = payload["identity"]
    return userid_mapping.get(user_id, None)

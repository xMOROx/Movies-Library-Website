import pyrebase

firebaseConfig = {
    # PASTE YOUR FIREBASE CONFIG HERE
}
firebase = pyrebase.initialize_app(firebaseConfig)

config = {
    "authe": firebase.auth(),
    "database": firebase.database(),
}


def get_config():
    return config

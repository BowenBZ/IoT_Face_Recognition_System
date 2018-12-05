import pyrebase


class MyDataBase:
    def __init__(self):
        self._config = {
            "apiKey": "AIzaSyCvrQZV4I_IvYmpyBJIKhP5gTNwCTmfB78",
            "authDomain": "assignment2-database.firebaseapp.com",
            "databaseURL": "https://assignment2-database.firebaseio.com",
            "storageBucket": "assignment2-database.appspot.com",
        }

        # Initialize firebase
        self._firebase = pyrebase.initialize_app(self._config)

        #authenticate a user
        self._auth = self._firebase.auth()
        self._user = self._auth.sign_in_with_email_and_password("a6887791@126.com", "ilovepython")

        # Generate the firebase
        self._db = self._firebase.database()

    def send_data(self, subdir, data):
        self._db.child(subdir).update(data, self._user['idToken'])

    def read_data(self):
        print("Log on")
        data = self._db.get().val()
        print(data["image"])
        print("Read Finish")

# Read data
# data = db.get().val()
# print(data["say"])

# Write data
# new_data = {"say2": "hello friends hh"}
# db.child('test').update(new_data, user['idToken'])

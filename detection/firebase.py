
import pyrebase
firebaseConfig = {
#     "apiKey": "AIzaSyCYGEHXFsbiFSWTFa6nYUVoM13fwVT_8_Q",
#     "authDomain": "cervi-test-models.firebaseapp.com",
#     "projectId": "cervi-test-models",
#     "storageBucket": "cervi-test-models.appspot.com",
#     "messagingSenderId": "1063586652238",
#     "appId": "1:1063586652238:web:78d1d347c956e5fb04631f",
#     "databaseURL": "https://cervi-test-models.firebaseio.com/",
#     "measurementId": "G-251VGDM6Y8"
    
      "apiKey": "AIzaSyDeLyZpqnhaklpKw2uT5Tvw_f_f-7TAQ6E",
      "authDomain": "cervi-test-project.firebaseapp.com",
      "projectId": "cervi-test-project",
      "storageBucket": "cervi-test-project.appspot.com",
      "messagingSenderId": "242934371681",
      "appId": "1:242934371681:web:dd8054d2cf533a18a6a120",
      "databaseURL": "https://cervi-test-project-default-rtdb.firebaseio.com/",
      "measurementId": "G-52ESV45G4N"
}

firebase = pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()

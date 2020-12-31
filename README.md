#Election Portal

###package installation

```
pip3 install requirements.txt
```

###setting up project
First start postgres server and replace postgres creds with your creds of postgres
```
python3 manage.py makemigrations
python3 manage.py migrate
```
create images folder in root directory of project with name `images` and one folder inside `images` folder with name `voter` 

###import database from csv files
```
python3 manage.py runscript data_upload
```
###running server
```
python3 manage.py runserver
```

###routes
```
"/election_portal" will be used for asking login with outlook
"/election_portal/verification" is being used for getting location, image of user and captcha verification
"/election_portal/vote" will be used for voting
```

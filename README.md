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
"/" will be used for asking login with outlook
"/verification" is being used for getting location, image of user and captcha verification
"/voter/" will be used to show voter details
"/voter/vote" will be used for voting
```
# might also need to run django bootstrap to get up and running
virtualenv venv
source venv/bin/activate
pip install django
pip install requests
python manage.py runserver #runs the debug variant of the server


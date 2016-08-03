# Use virtualenv
virtualenv venv
# Activate virtualenv
source venv/bin/activate
# Install django and requests
pip install django==1.4
pip install requests
# To run
python manage.py runserver #runs the debug variant of the server

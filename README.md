# Restaurant-Revenue-Prediction 
### How to install

To run this project, you'll need Python 3.10.9, postgresql and pip (to install packages).
Use the following commands: 
```
git clone https://github.com/elizavetalipen/Restaurant-Revenue-Prediction.git
cd testtask
```
You can also create and activate a virtual environment (optional).
Then run this command to install the project dependencies
```
pip install -r requirements.txt
```
You'll need to create an .env file and write your database data and Django secret key.
To generate the key, use >>python command to open the interpreter
```
from django.core.management.utils import get_random_secret_key
get_random_secret_key()
```
Now copy this key to your .env file:
```
SECRET_KEY=your_key
DB_NAME=your_dbname
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=your_host(or localhost)
DB_PORT=your_port(default 5432)
```
Apply migrations and start server
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Dev env setup
*********************************************
1. Install requirements.txt. Use venv or pipenv(preference)
2. Activate the virtual environment
3. Run migration
   > python manage.py makemigrations
   > python manage.py migrate
4. Create super user a/c(admin)
5. Runserver
   > python manage.py runserver
6. Create/Load dummy data
   Directly on the database table or using endpoints.
   > python manage.py runserver
7. Explore the various endpoints as listed

***********************************************
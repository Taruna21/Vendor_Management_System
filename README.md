Dev environment setup
*********************************************
1. Install dependencies. Use venv or pipenv(preference)
2. Activate the virtual environment
3. Run migration
   > python manage.py makemigrations <br>
   > python manage.py migrate
4. Create super user a/c(admin)
5. Runserver
   > python manage.py runserver
6. Create/Load dummy data
   Directly on the database table or using endpoints.
   > python manage.py runserver
7. Import 'endpoints.har' in the project directory into the client
i.e. Postman or Insomnia etal
8. Explore the various endpoints as listed.

***********************************************
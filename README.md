A demo project for [wesharesolar.com](http://wesharesolar.com)

The project uses **Python 3.5.1** and **Django 1.9.2**

![Excursions app](http://i.imgur.com/sCr5wrV.png "Excursions app")

### Setup:

1. Clone the repo
2. Manually create local Posgresql database and dbuser (see `settings.py`)
3. Run `./manage.py migrate`
  * A superuser will be created, see `settings.py` for login credentials
  * Do not forget to change them once logged in to `http://localhost:8000/admin`
4. Visit `http://localhost:8000/`
5. Profit

### Tests:

run `./manage.py test`

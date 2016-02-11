A demo project for [wesharesolar.com](http://wesharesolar.com)

The project uses **Python 3.5.1** and **Django 1.9.2**

![Excursions app](http://i.imgur.com/sCr5wrV.png "Excursions app")

### Setup:

1. Clone the repo
2. Manually create virtual environment using `pyenv` or `virtualenv`, the project uses **Python 3.5.1**
3. Run `pip install -r requirements.txt`
4. Manually create local Posgresql database and dbuser (see `settings.py`), set proper db login credentials there
5. Run `./manage.py migrate`
  * A superuser will be created, see `settings.py` for login credentials
  * Do not forget to change them once logged in to `http://localhost:8000/admin`
6. Run `./manage.py update_database` to update local database with data from csv files stored in Dropbox cloud
7. There's also a cronjob which updates these files (daily by default), you can start this cronjob by running `./manage.py crontab add`, it will add all defined jobs from CRONJOBS in `settings.py` to crontab (of the user which you are running this command with)
8. To see all cronjobs, run `./manage.py crontab show`
9. To remove all cronjobs, run `./manage.py crontab remove`
10. Visit `http://localhost:8000/`
11. Profit

### Tests:

* Run `./manage.py test`
* Important: do not remove `test_*` csv files from the cloud, they're used for testing the api

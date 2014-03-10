# request.data

## Development Setup

In order to run the commands below you need to have [vagrant](http://www.vagrantup.com/) installed.

    git clone https://github.com/liip/request.data.git request.data
    cd request.data/
    vagrant up

## Temp fix for crash on starting up the vagrant box

After it crashes, ssh-into the box and run `curl https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py | python`

Then run `pip install -r requirements.txt` again

Exit

Do `vagrant provision` again, that should fix it. …best to start with a fresh box though


As soon as all the dependencies are installed you can ssh into the virtualmachine and run the application

    vagrant ssh
    foreman start

As soon as all the dependencies are installed you can ssh into the virtualmachine and run the application

    vagrant ssh
    foreman start

## General development

When a change is made to the database data that should be loaded by default replace the fixtures.

    DATABASE_URL=postgres://user_default:pass@localhost:5432/request_data python /vagrant/manage.py dumpdata > fixtures/initial_data.json

Opening the django shell
  
    DATABASE_URL=postgres://user_default:pass@localhost:5432/request_data python /vagrant/manage.py shell

## Deploy on heroku

    heroku create some_cool_app_name --region eu --stack cedar
    git push heroku master

    # run the migrations
    heroku run python manage.py syncdb --noinput

    # load some sample data
    heroku run python manage.py loaddata fixtures/initial_data.json

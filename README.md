# request.data

## Development Setup

In order to run the commands below you need to have [vagrant](http://www.vagrantup.com/) installed.

    git clone https://github.com/liip/request.data.git request.data
    cd request.data/
    vagrant up


As soon as all the dependencies are installed you can ssh into the virtualmachine and run the application

    vagrant ssh
    foreman start

## General development

When a change is made to the database data that should be loaded by default replace the fixtures.

    DATABASE_URL=postgres://user_default:pass@localhost:5432/request_data python /vagrant/manage.py dumpdata > fixtures/initial_data.json

Opening the django shell
  
    DATABASE_URL=postgres://user_default:pass@localhost:5432/request_data python /vagrant/manage.py shell
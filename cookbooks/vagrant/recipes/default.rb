USER = node[:user]
HOME = "/home/#{USER}"
VAGRANT_DIR = "/vagrant"

template "#{HOME}/.bash_aliases" do
  user "vagrant"
  mode "0644"
  source ".bash_aliases.erb"
end

bash "set default locale to UTF-8" do
  code <<-EOH
update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8
dpkg-reconfigure locales
EOH
end

execute "apt-get update"

# install the software we need
%w(
curl
vim
git
libapache2-mod-wsgi
libpq5
libpq-dev
postgresql
python-pip
python-dev
python-virtualenv
python-software-properties
libfontconfig1
).each { | pkg | package pkg }


bash "install heroku toolbelt" do
  user "root"
  code <<-EOH
  wget -qO- https://toolbelt.heroku.com/install-ubuntu.sh | sh
  EOH
end

bash "create a virtualenv" do
  user USER
  not_if "test -f #{HOME}/default/bin/activate"
  code <<-EOH
  virtualenv #{HOME}/default --distribute
  EOH
end

bash "install pip requirements" do
  user USER
  code <<-EOH
  source #{HOME}/default/bin/activate
  curl https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py | python
  deactivate
  source #{HOME}/default/bin/activate
  pip install -r #{VAGRANT_DIR}/requirements.txt
  EOH
end

bash "install PhantomJs " do
  not_if "which phantomjs"
  user "root"
  code <<-EOH
    set -e
    wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-1.9.7-linux-x86_64.tar.bz2
    tar jxf phantomjs-1.9.7-linux-x86_64.tar.bz2
    rm -rf phantomjs-1.9.7-linux-x86_64.tar.bz2
    ln -sf /phantomjs-1.9.7-linux-x86_64/bin/phantomjs /usr/bin/phantomjs
  EOH
end

bash "install CasperJs " do
  not_if "which casperjs"
  user "root"
  code <<-EOH
    set -e
    git clone git://github.com/n1k0/casperjs.git
    cd casperjs
    ln -sf `pwd`/bin/casperjs /usr/local/bin/casperjs
  EOH
end

bash "make sure postgres is using UTF-8" do
  user "root"
  not_if "sudo -u postgres psql -c '\\l' | grep en_US.UTF-8"
  code <<-EOH
  service apache2 stop
  pg_dropcluster --stop 9.1 main
  pg_createcluster --start -e UTF-8 9.1 main
  service apache2 start
  EOH
end

bash "setup postgres db" do
  user "postgres"
  not_if "sudo -u postgres psql -c '\\l' | grep request_data"
  code <<-EOH
  createuser -S -D -R user_default
  psql -c "ALTER USER user_default with password 'pass'"
  createdb -O user_default request_data -E utf-8
  EOH
end

bash "run the migrations" do
  user USER
  code <<-EOH
  source #{HOME}/default/bin/activate
  DATABASE_URL=postgres://user_default:pass@localhost:5432/request_data python #{VAGRANT_DIR}/manage.py syncdb --noinput
  EOH
end

bash "load the fixtures" do
  user USER
  code <<-EOH
  source #{HOME}/default/bin/activate
  DATABASE_URL=postgres://user_default:pass@localhost:5432/request_data python #{VAGRANT_DIR}/manage.py loaddata #{VAGRANT_DIR}/fixtures/initial_data.json
  EOH
end

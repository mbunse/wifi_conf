#!/bin/bash

# create dedicated user
useradd -r -s /bin/false wifi_conf
# Add user to gpio group to grand access to /dev/mem
adduser wifi_conf gpio
# Grant access to sudo
# needed to set up wifi
adduser wifi_conf sudo

# create dedicated gunicorn user
useradd -r -s /bin/false gunicorn

# allow gunicorn to communicate with wifi_conf daemon
adduser gunicorn wifi_conf

# make conf dir and conf file
mkdir -p /etc/gunicorn
cp -f gunicorn.conf /etc/gunicorn/gunicorn.conf
chown -R gunicorn:gunicorn /etc/gunicorn
chmod ag+r /etc/kids_phone/linphone.conf
chmod g+w /etc/kids_phone/linphone.conf

# set up logging
cp -f kids_phone_log.conf /etc/rsyslog.d/kids_phone.conf
chmod ag+r /etc/rsyslog.d/kids_phone.conf

# set up service
cp -f kids_phone.service /etc/systemd/system/kids_phone.service
chmod ag+r /etc/systemd/system/kids_phone.service



## kids_phone_conf web interface
sudo mkdir -p /var/www
cp -r kids_phone_conf /var/www/.
chown -R kids_phone_www:kids_phone /var/www/kids_phone_conf

# Create dir for socket and assign to kids_phone user
mkdir -p /var/run/kids_phone
chown -R kids_phone:kids_phone /var/run/kids_phone
chmod g+w /var/run/kids_phone


# set up logging
cp kids_phone_www_log.conf /etc/rsyslog.d/kids_phone_www.conf
chmod ag+r /etc/rsyslog.d/kids_phone_www.conf

# set up service
cp kids_phone_www.service /etc/systemd/system/kids_phone_www.service
chmod ag+r /etc/systemd/system/kids_phone_www.service

# give rioghts to start and stop kids_phone
mkdir -p /etc/polkit-1/rules.d
cp -f manage-kids_phone.rules /etc/polkit-1/rules.d/manage-kids_phone.rules

# set up nginx
systemctl stop nginx
# extract IP address to be added to certificate
IP=`ifconfig wlan0 | sed -zEn 's/127.0.0.1//;s/.*inet (addr:)?(([0-9]*\.){3}[0-9]*).*/\2/p'`
echo IP is $IP

# replace server name with IP, so that certificate fits to name
cat nginx.conf | sed "s/server_name  localhost/server_name  $IP/g" >  nginx.conf_ip

# Create secret key for django
SECRET_KEY=`python -c "import string,random; uni=string.ascii_letters+string.digits+string.punctuation; print repr(''.join([random.SystemRandom().choice(uni) for i in range(random.randint(45,50))]))"`

# Create secret file for django
cat > /var/www/kids_phone_conf/kids_phone_conf/secrets.py <<EOL
SECRET_KEY = ${SECRET_KEY}

ALLOWED_HOSTS = ["${IP}"]

EOL

# Load initial data
pushd /var/www/kids_phone_conf
python3 manage.py makemigrations
python3 manage.py makemigrations call_numbers
python3 manage.py migrate
python3 manage.py loaddata call_numbers/initial_fixture.json
popd

mv nginx.conf_ip /etc/nginx/nginx.conf
rm -f /etc/nginx/sites-enabled/*

# reload units
systemctl daemon-reload

# Restart logging service
systemctl restart rsyslog

# enable services
systemctl enable kids_phone
systemctl enable kids_phone_www
systemctl restart kids_phone
systemctl restart kids_phone_www
systemctl restart nginx
# Instalar Cliente

cd /home/medis_manager && git pull

### Nginx
sudo cp /home/medis_manager/deploy/nginx.conf /etc/nginx/sites-enabled/medis

### Gunicorn
sudo cp /home/medis_manager/deploy/gunicorn.service /etc/systemd/system/medis.service
sudo systemctl daemon-reload && sudo systemctl start medis && sudo systemctl enable medis

### Apply configuration
#cd /home/medis_manager && git pull

source /home/env/medis/bin/activate
python /home/medis_manager/manage.py migrate --settings=medis_manager.settings_prod
python /home/medis_manager/manage.py collectstatic --settings=medis_manager.settings_prod


#python /home/medis_manager/manage.py collectstatic --settings=sipe.clients.altoeste.settings
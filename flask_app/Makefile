srv_start:
	sudo systemctl start newshorizon
	sudo systemctl enable newshorizon
	sudo systemctl status newshorizon

srv_stop:
	sudo systemctl disable newshorizon
	sudo systemctl stop newshorizon

srv_status:
	sudo systemctl status newshorizon

nginx_edit:
	sudo nano /etc/nginx/sites-available/newshorizon

nginx_log:
	tail /var/log/nginx/error.log

srv_edit:
	sudo nano /etc/systemd/system/newshorizon.service

flask_start:
	export FLASK_DEBUG=1
	export FLASK_ENV=development
	export FLASK_APP=newshorizon.py
	export NHHOST=LOCAL_JEAN
	python3 newshorizon.py
db_start:
	pg_ctl start -D /usr/local/var/postgres

db_stop:
	pg_ctl stop -D /usr/local/var/postgres

db_local_connect:
	psql --dbname=media -U jean

db_remote_connect:
	psql -h 35.195.3.218 -p 5432 -U postgres media

gce_connect:
	gcloud beta compute ssh --zone europe-west1-b newshorizonapp@worker --project future-oasis-286707

gce_transfer_files:
	gcloud compute scp /Users/jean/Documents/Coding/MediAnalyserPOC/ml_models/NEWS_INDEX.pickle newshorizonapp@worker:/home/newshorizonapp/MediAnalyserPOC/ml_models/
	gcloud compute scp /Users/jean/Documents/Coding/MediAnalyserPOC/ml_models/NEWS_DICT.pickle newshorizonapp@worker:/home/newshorizonapp/MediAnalyserPOC/ml_models/
	gcloud compute scp /Users/jean/Documents/Coding/MediAnalyserPOC/ml_models/NEWS_VECT.pickle newshorizonapp@worker:/home/newshorizonapp/MediAnalyserPOC/ml_models/
	gcloud compute scp /Users/jean/Documents/Coding/MediAnalyserPOC/ml_models/W2V.pickle newshorizonapp@worker:/home/newshorizonapp/MediAnalyserPOC/ml_models/
	gcloud compute scp /Users/jean/Documents/Coding/MediAnalyserPOC/ml_models/KNN.pickle newshorizonapp@worker:/home/newshorizonapp/MediAnalyserPOC/ml_models/

gce_backup_logs:
	gcloud compute scp newshorizonapp@worker:/home/newshorizonapp/MediAnalyserPOC/main/logs/crontab_log.txt /Users/jean/Documents/Coding/MediAnalyserPOC/main/logs/
	gcloud compute scp newshorizonapp@worker:/home/newshorizonapp/MediAnalyserPOC/main/logs/article_fetching_log.txt /Users/jean/Documents/Coding/MediAnalyserPOC/main/logs/
	gcloud compute scp newshorizonapp@worker:/home/newshorizonapp/MediAnalyserPOC/main/logs/email_push_notifications_log.txt /Users/jean/Documents/Coding/MediAnalyserPOC/main/logs/
	gcloud compute scp newshorizonapp@worker:/home/newshorizonapp/MediAnalyserPOC/main/logs/ml_model_creation_logs.txt /Users/jean/Documents/Coding/MediAnalyserPOC/main/logs/

max_connect:
	ssh -p 22022 jean@5.149.19.251

crontab:
	crontab main/crontab.txt

cron_log:
	grep CRON /var/log/syslog

srv_setting:
	cat main/server_setting.txt > /etc/systemd/system/newshorizon.service

list_vars:
	echo "REPOPATH $$(REPOPATH)"
	echo "GOOGLE_APPLICATION_CREDENTIALS $$(GOOGLE_APPLICATION_CREDENTIALS)"

std_vars:
	echo "#newshorizonapp" >> ~/.bashrc
	echo "export REPOPATH=/home/jean/MediAnalyserPOC" >> ~/.bashrc
	echo "export PYTHONPATH=$$(PYTHONPATH):$$(REPOPATH)" >> ~/.bashrc
	echo "export GOOGLE_APPLICATION_CREDENTIALS=$$(REPOPATH)/credentials/future-oasis-286707-c52c864bbc9e.json"  >> ~/.bashrc
	echo "" >> ~/.bashrc
	echo "#end newshorizonapp" >> ~/.bashrc

nginx_settings:
	cat main/nginx_setting.txt > /etc/nginx/sites-available/newshorizon
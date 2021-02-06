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
	echo "export NHHOST=LOCAL_JEAN" >> ~/.bashrc
	echo "#end newshorizonapp" >> ~/.bashrc

nginx_settings:
	cat main/nginx_setting.txt > /etc/nginx/sites-available/newshorizon

max_ml_copy:
	scp -p jean@5.149.19.251:/home/jean/Code/MediAnalyserPOC/ml_models/*.pickle /Users/jean/Documents/Coding/MediAnalyserPOC/ml_models/

flask_env:
	export FLASK_DEBUG=1
	export FLASK_ENV=development
	export FLASK_APP=newshorizon.py
	export NHHOST=LOCAL_JEAN
	python3 newshorizonapp

NH_DB_BACKUP_FILE_NAME := "./db_backups/db_backup_media_""`date "+%Y_%m_%d-%H_%M_%S"`"".backup"

db_backup:
	pg_dump media | gzip > $(NH_DB_BACKUP_FILE_NAME)
	gsutil cp $(NH_DB_BACKUP_FILE_NAME) gs://newshorizon_backup_db/

NH_GCS_DB_RESTORE_FILE_NAME := $(shell gsutil ls -l gs://newshorizon_backup_db/ | grep -v TOTAL | sort -r -k 2 | sed -n '1 p' | awk '{print $$3}')
NH_DB_RESTORE_FILE_NAME := $(notdir $(NH_GCS_DB_RESTORE_FILE_NAME))

db_restore:
	gsutil cp $(NH_GCS_DB_RESTORE_FILE_NAME) "./db_backups/$(NH_DB_RESTORE_FILE_NAME)"
	gunzip -c "./db_backups/${NH_DB_RESTORE_FILE_NAME}" | psql media
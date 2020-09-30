db_start:
	pg_ctl start -D /usr/local/var/postgres

db_stop:
	pg_ctl stop -D /usr/local/var/postgres

db_connect:
	psql --dbname=media -U jean

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

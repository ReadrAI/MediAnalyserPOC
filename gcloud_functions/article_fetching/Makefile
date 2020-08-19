deploy: dependencies
	gcloud functions deploy hello_pubsub --runtime python37 --region=europe-west1 --trigger-topic article-fetching
	#projects/future-oasis-286707/topics/article-fetching
	#gcloud functions deploy hello_pubsub --runtime python37 --trigger-http --allow-unauthenticated --region=europe-west1

describe:
	gcloud functions describe hello_pubsub --region=europe-west1

log:
	gcloud functions logs read hello_pubsub --region=europe-west1 --min-log-level=info

dependencies:
	rm -r -f ./utils/*
	cp /Users/jean/Documents/Coding/MediAnalyserPOC/utils/sql_utils.py ./utils/
	cp /Users/jean/Documents/Coding/MediAnalyserPOC/utils/scrape_utils.py ./utils/
	cp /Users/jean/Documents/Coding/MediAnalyserPOC/utils/models.py ./utils/
	cp /Users/jean/Documents/Coding/MediAnalyserPOC/utils/verbose.py ./utils/

	rm -r -f ./cert/*
	cp /Users/jean/.postgresql/postgresql.crt ./cert/
	cp /Users/jean/.postgresql/postgresql.key ./cert/
	cp /Users/jean/.postgresql/root.crt ./cert/

	chmod 600 ./cert/*
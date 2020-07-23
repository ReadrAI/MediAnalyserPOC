db_start:
	pg_ctl start -D /usr/local/var/postgres

db_stop:
	pg_ctl stop -D /usr/local/var/postgres

db_connect:
	psql --dbname=media -U jean
drop table if exists sources cascade;
create table sources (
	source_uuid uuid primary key default uuid_generate_v4 (),
	source_name varchar(20) unique,
	country varchar(3),
	website_url text,
	api_url text,
	api_key text,
	addedAt timestamp,
	aliases varchar(20)[]
);

insert into media.listing.sources (source_name, country, website_url, api_url, api_key, addedat)
values (
	'NYTimes', 
	'us', 
	'https://www.nytimes.com/', 
	'https://api.nytimes.com/svc/topstories/v2/home.json?api-key=API_KEY', 
	'ellopTlugRyqVlTglivpkLaSPPwGo8Jj', 
	current_timestamp);

insert into media.listing.sources (source_name, country, website_url, api_url, api_key, addedat)
values (
	'NewsAPI', 
	'n/a', 
	'n/a', 
	'https://newsapi.org/v2/everything?language=en&pageSize=100&apiKey=API_KEY',
	'e30a64cfe1734e6794bdab67106590fa', 
	current_timestamp);
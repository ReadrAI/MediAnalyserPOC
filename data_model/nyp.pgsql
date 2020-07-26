-- requires: sources.sql
insert into media.listing.sources (source_name, country, website_url, addedat, aliases) 
VALUES ('New York Post', 'us', 'https://nypost.com/', CURRENT_TIMESTAMP, '{"nypost", "ny-post"}');
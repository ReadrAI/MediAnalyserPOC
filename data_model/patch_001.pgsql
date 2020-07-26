-- required: sources.sql
alter table media.listing.sources alter column source_name type varchar(200);
alter table sources alter column aliases type varchar(200)[];
drop table if exists listing.articles cascade;
drop table if exists listing.article_contents;
create table listing.articles (
	article_uuid uuid primary key default uuid_generate_v4 (),
	article_url text unique,
	source_uuid uuid, -- where the article has been published
	provider_uuid uuid, -- where the article has been found
	title text,
	description text,
	author varchar(200),
	publishedAt timestamp,
	updatedAt timestamp,
	CONSTRAINT fk_source
      FOREIGN KEY(source_uuid) 
	  REFERENCES sources(source_uuid)
);

create table listing.article_contents(
	article_uuid uuid,
	content text,
	CONSTRAINT fk_article
      FOREIGN KEY(article_uuid) 
	  REFERENCES articles(article_uuid)
);
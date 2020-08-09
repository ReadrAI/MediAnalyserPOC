import uuid
import datetime

from sqlalchemy import Column, String, Text, DateTime, ARRAY, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

schema = "newsdb"


class Source(Base):
    """Media Sources and Information Providers."""
    __tablename__ = "sources"
    __table_args__ = {"schema": schema}

    source_uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    source_name = Column(String(100), nullable=False, unique=True)
    country = Column(Text, nullable=True)
    website_url = Column(Text, nullable=False, unique=True)
    api_url = Column(Text, unique=True)
    api_key = Column(Text)
    added_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    aliases = Column(ARRAY(String))

    def __repr__(self):
        return '<Source {}: {}>'.format(self.source_uuid, self.source_name)


class Article(Base):
    """Media Articles and News Content."""
    __tablename__ = "articles"
    __table_args__ = {"schema": schema}

    article_uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    article_url = Column(Text, nullable=False, unique=True)
    source_uuid = Column(UUID, ForeignKey(schema + ".sources.source_uuid"), nullable=False)
    provider_uuid = Column(UUID, ForeignKey(schema + ".sources.source_uuid"), nullable=False)
    title = Column(Text, nullable=False)
    description = Column(Text)
    authors = Column(ARRAY(String))
    published_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime)

    source = relationship("Source", foreign_keys=[source_uuid])
    provider = relationship("Source", foreign_keys=[provider_uuid])

    def __repr__(self):
        return '<Article {}: {}>'.format(self.article_uuid, self.title)


class ArticleContent(Base):
    """Media Articles and News Content."""
    __tablename__ = "article_contents"
    __table_args__ = {"schema": schema}

    article_uuid = Column(UUID, ForeignKey(schema + ".articles.article_uuid"), primary_key=True, nullable=False)
    article_content = Column(Text, nullable=False)

    article = relationship("Article")

    def __repr__(self):
        return '<Article Content {}: {}>'.format(self.article_uuid, self.article_content)


class RSSFeed(Base):
    """RSS Feeds for News Sources."""
    __tablename__ = "rss_feeds"
    __table_args__ = {"schema": schema}

    feed_uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False, unique=True)
    source_uuid = Column(UUID, ForeignKey(schema + ".sources.source_uuid"), nullable=False)
    feed_url = Column(Text, unique=True, nullable=False)
    feed_section = Column(Text)

    def __repr__(self):
        return '<RSS Feed {}: {}>'.format(self.feed_uuid, self.feed_url)
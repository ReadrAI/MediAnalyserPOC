import uuid
import datetime

from sqlalchemy import Column, String, Text, DateTime, ARRAY, ForeignKey, Integer, Float, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

schema = "newsdb"

"""
News Information
"""


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
    language = Column(Text, nullable=True)

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
    rss_uuid = Column(UUID, ForeignKey(schema + ".rss_feeds.feed_uuid"))
    title = Column(Text, nullable=False)
    description = Column(Text)
    authors = Column(ARRAY(String))
    published_at = Column(DateTime)
    updated_at = Column(DateTime)
    added_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)

    source = relationship("Source", foreign_keys=[source_uuid])
    provider = relationship("Source", foreign_keys=[provider_uuid])
    rss_feed = relationship("RSSFeed")

    def __repr__(self):
        return '<Article {}: {}>'.format(self.article_uuid, self.title)


class MultiLingualArticle(Base):
    """Multi-Lingual Media Articles and News Content."""
    __tablename__ = "multi_lingual_articles"
    __table_args__ = {"schema": schema}

    article_uuid = Column(UUID, ForeignKey(schema + ".articles.article_uuid"), primary_key=True, nullable=False)
    language = Column(Text, nullable=False)
    title = Column(Text, nullable=False)
    description = Column(Text)

    article = relationship("Article")

    def __repr__(self):
        return '<Article {}: ({}) {}>'.format(self.article_uuid, self.language, self.title)


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

    source = relationship("Source")

    def __repr__(self):
        return '<RSS Feed {}: {}>'.format(self.feed_uuid, self.feed_url)


"""
MailRequests
"""


class ArticleSearch(Base):
    """Email Requests for Similar Articles."""
    __tablename__ = "article_searches"
    __table_args__ = {"schema": schema}

    article_search_uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False, unique=True)
    gmail_request_uuid = Column(Text, unique=True, nullable=False)
    gmail_answer_uuid = Column(Text, unique=True)
    received_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    replied_at = Column(DateTime, default=None)

    search_url = Column(Text)
    search_article = Column(UUID, ForeignKey(schema + ".articles.article_uuid"))
    n_results = Column(Integer, default=5)
    status = Column(Text, default='')

    customer_uuid = Column(UUID, ForeignKey(schema + ".customers.customer_uuid"), nullable=False)

    article = relationship("Article")
    customer = relationship("Customer")

    def __repr__(self):
        return '<Article Search {}: {}>'.format(self.article_search_uuid, self.search_url)


class Customer(Base):
    """Customer of Requests."""
    __tablename__ = "customers"
    __table_args__ = {"schema": schema}

    customer_uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False, unique=True)
    customer_email = Column(Text, unique=True, nullable=False)
    added_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    is_blocked = Column(Boolean, nullable=False, default=lambda x: False)

    def __repr__(self):
        return '<Customer {}: {}>'.format(self.customer_uuid, self.customer_email)


class ArticleSearchResult(Base):
    """Similar Article Results."""
    __tablename__ = "article_search_results"
    __table_args__ = {"schema": schema}

    search_uuid = Column(UUID, ForeignKey(schema + ".article_searches.article_search_uuid"), primary_key=True,
                         nullable=False)
    article_uuid = Column(UUID, ForeignKey(schema + ".articles.article_uuid"), primary_key=True, nullable=False)
    distance = Column(Float)

    article = relationship("Article")
    search = relationship("ArticleSearch")

    def __repr__(self):
        return '<Article Search Result {}: {}>'.format(self.search_uuid, self.article_uuid)


class InvalidEmail(Base):
    """Invalid Email Requests."""
    __tablename__ = "invalid_emails"
    __table_args__ = {"schema": schema}

    invalid_email_uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False, unique=True)
    gmail_request_uuid = Column(Text, unique=True, nullable=False)
    customer_uuid = Column(UUID, ForeignKey(schema + ".customers.customer_uuid"), nullable=False)
    status = Column(Text)

    customer = relationship("Customer")

    def __repr__(self):
        return '<Invalid Email {}: {} - {} - {}>'.format(self.invalid_email_uuid, self.status, self.gmail_request_uuid,
                                                         self.customer_uuid)

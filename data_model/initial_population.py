from utils import sql_utils
from data_model import models

# Missing Sources
missing_sources = {
    "CP24 Toronto's Breaking News",
    'Calgary Herald',
    'Canada NewsWire',
    'Ctvnews.ca',
    'DiscoverMooseJaw.com',
    'Edmonton Journal',
    'Gizmodo.com',
    'Global News',
    'HalifaxToday.ca',
    'Lifehacker.com',
    'Montreal Gazette',
    'Net Newsledger',
    'OttawaMatters.com',
    'OurWindsor.ca',
    'Shepherdgazette.com',
    'TheChronicleHerald.ca',
    'Toronto Star',
    'Winnipeg Sun',
    'iNFOnews',
    'Adweek',
    'Androidrookies.com',
    'Business Wire',
    'Cointelegraph',
    'Fstoppers',
    'Futurity: Research News',
    'Juxtapoz.com',
    'Lifehack.org',
    'MarketWatch',
    'Mint.com',
    'Motley Fool',
    'Project Syndicate',
    'Scientific American',
    'Sky Sports',
    'Slashdot.org',
    'The Economist',
    'The Indian Express',
    'Theguardian.compolitics',
    'Theguardian.comus-news',
    'Visual.ly',
    'Wellnessmama.com',
    'Worldsoccertalk.com'}


oan_rss_feeds = [
    ("One America News Network", "http://www.oann.com/feed", None),
    ("One America News Network", "Top News", "http://www.oann.com/category/newsroom/feed"),
    ("One America News Network", "World", "http://www.oann.com/category/world/feed"),
    ("One America News Network", "Business", "http://www.oann.com/category/business/feed"),
    ("One America News Network", "Economy", "http://www.oann.com/category/economy/feed"),
    ("One America News Network", "Money", "http://www.oann.com/category/money/feed"),
    ("One America News Network", "Technology", "http://www.oann.com/category/tech/feed"),
    ("One America News Network", "Entertainment", "http://www.oann.com/category/entertainment/feed")
]


nyt_rss_feeds = [
    "Africa",
    "Americas",
    "ArtandDesign",
    "Arts",
    "AsiaPacific",
    "Automobile",
    "Baseball",
    "Books",
    "Business",
    "Climate",
    "CollegeBasketball",
    "CollegeFootball",
    "Dance",
    "Dealbook",
    "DiningandWine",
    "Economy",
    "Education",
    "EnergyEnvironment",
    "Europe",
    "FashionandStyle",
    "Golf",
    "Health",
    "Hockey",
    "HomePage",
    "Jobs",
    "Lens",
    "MediaandAdvertising",
    "MiddleEast",
    "MostEmailed",
    "MostShared",
    "MostViewed",
    "Movies",
    "Music",
    "NYRegion",
    "Obituaries",
    "PersonalTech",
    "Politics",
    "ProBasketball",
    "ProFootball",
    "RealEstate",
    "Science",
    "SmallBusiness",
    "Soccer",
    "Space",
    "Sports",
    "SundayBookReview",
    "Sunday-Review",
    "Technology",
    "Television",
    "Tennis",
    "Theater",
    "TMagazine",
    "Travel",
    "Upshot",
    "US",
    "Weddings",
    "Well",
    "YourMoney"
]


def populateNYTFeeds():
    count = 0
    for section in nyt_rss_feeds:
        count += sql_utils.populateFeeds(
            "New York Times",
            "https://rss.nytimes.com/services/xml/rss/nyt/%s.xml" % section,
            section)
    return count


def populateONAFeeds():
    count = 0
    for feed in oan_rss_feeds:
        count += sql_utils.populateFeeds(feed[0], feed[2], feed[1])
    return count


def populateSources():
    sql_utils.insertEntry(models.Source(
        source_name='New York Times',
        country='us',
        website_url='https://www.nytimes.com/',
        api_url='https://api.nytimes.com/svc/topstories/v2/home.json?api-key=API_KEY',
        api_key='ellopTlugRyqVlTglivpkLaSPPwGo8Jj',
        aliases=['NYT']
    ))
    sql_utils.insertEntry(models.Source(
        source_name='NewsAPI',
        website_url='https://newsapi.org/',
        api_url='https://newsapi.org/v2/everything?language=en&pageSize=100&apiKey=API_KEY',
        api_key='e30a64cfe1734e6794bdab67106590fa'
    ))
    sql_utils.insertEntry(models.Source(
        source_name='Houston Chronicle',
        website_url='https://www.chron.com/'
    ))
    sql_utils.insertEntry(models.Source(
        source_name='KOIN.com',
        website_url='https://www.koin.com/'
    ))
    sql_utils.insertEntry(models.Source(
        source_name='Yahoo Entertainment',
        website_url='https://www.yahoo.com/entertainment/'
    ))
    sql_utils.insertEntry(models.Source(
        source_name='WJCL News',
        website_url='https://www.wjcl.com/'
    ))
    sql_utils.insertEntry(models.Source(
        source_name='Daily Mail',
        website_url='https://www.dailymail.co.uk/'
    ))
    sql_utils.insertEntry(models.Source(
        source_name='Fairbanks Daily News-Miner',
        website_url='http://www.newsminer.com/'
    ))
    sql_utils.insertEntry(models.Source(
        source_name='PhoneArena',
        website_url='https://www.phonearena.com/'
    ))
    sql_utils.insertEntry(models.Source(
        source_name='Notebookcheck.net',
        website_url='https://www.notebookcheck.net/'
    ))
    sql_utils.insertEntry(models.Source(
        source_name='CNBC',
        website_url='https://www.cnbc.com/'
    ))
    sql_utils.insertEntry(models.Source(
        source_name='Forbes',
        website_url='https://www.forbes.com/'
    ))
    sql_utils.insertEntry(models.Source(
        source_name='Financial Times',
        website_url='https://www.ft.com/'
    ))
    sql_utils.insertEntry(models.Source(
        source_name='Express',
        website_url='https://www.express.co.uk/'
    ))
    sql_utils.insertEntry(models.Source(
        source_name='YouTube',
        website_url='https://www.youtube.com/'
    ))
    sql_utils.insertEntry(models.Source(
        source_name='Daily Beast',
        website_url='https://www.thedailybeast.com/'
    ))
    sql_utils.insertEntry(models.Source(
        source_name='CNET',
        website_url='https://www.cnet.com/'
    ))
    sql_utils.insertEntry(models.Source(
        source_name='The Cut',
        website_url='https://www.thecut.com/'
    ))
    sql_utils.insertEntry(models.Source(
        source_name='Green Bay Press Gazette',
        website_url='https://eu.greenbaypressgazette.com/'
    ))
    sql_utils.insertEntry(models.Source(
        source_name='Thurrott.com',
        website_url='https://www.thurrott.com/'
    ))
    sql_utils.insertEntry(models.Source(
        source_name='OregonLive',
        website_url='https://www.oregonlive.com/'
    ))
    sql_utils.insertEntry(models.Source(
        source_name='WANE',
        website_url='https://www.wane.com/'
    ))
    sql_utils.insertEntry(models.Source(
        source_name='New York Post',
        country='us',
        website_url="https://nypost.com/",
        aliases=["nypost", "ny-post"]
    ))

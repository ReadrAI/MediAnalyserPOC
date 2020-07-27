from utils import sql_utils
from data_model import models


def populate():
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

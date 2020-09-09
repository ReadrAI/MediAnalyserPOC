from utils import sql_utils
from utils.sql_utils import populateFeeds
from utils import models


oan_rss_feeds = [
    ("http://www.oann.com/feed", None),
    ("Top News", "http://www.oann.com/category/newsroom/feed"),
    ("World", "http://www.oann.com/category/world/feed"),
    ("Business", "http://www.oann.com/category/business/feed"),
    ("Economy", "http://www.oann.com/category/economy/feed"),
    ("Money", "http://www.oann.com/category/money/feed"),
    ("Technology", "http://www.oann.com/category/tech/feed"),
    ("Entertainment", "http://www.oann.com/category/entertainment/feed")
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

cnn_rss_feeds = [
    ("Top Stories", "http://rss.cnn.com/rss/edition.rss"),
    ("World", "http://rss.cnn.com/rss/edition_world.rss"),
    ("Africa", "http://rss.cnn.com/rss/edition_africa.rss"),
    ("Americas", "http://rss.cnn.com/rss/edition_americas.rss"),
    ("Asia", "http://rss.cnn.com/rss/edition_asia.rss"),
    ("Europe", "http://rss.cnn.com/rss/edition_europe.rss"),
    ("Middle East", "http://rss.cnn.com/rss/edition_meast.rss"),
    ("U.S.", "http://rss.cnn.com/rss/edition_us.rss"),
    ("Money", "http://rss.cnn.com/rss/money_news_international.rss"),
    ("Technology", "http://rss.cnn.com/rss/edition_technology.rss"),
    ("Science & Space", "http://rss.cnn.com/rss/edition_space.rss"),
    ("Entertainment", "http://rss.cnn.com/rss/edition_entertainment.rss"),
    ("World Sport", "http://rss.cnn.com/rss/edition_sport.rss"),
    ("Football", "http://rss.cnn.com/rss/edition_football.rss"),
    ("Golf", "http://rss.cnn.com/rss/edition_golf.rss"),
    ("Motorsport", "http://rss.cnn.com/rss/edition_motorsport.rss"),
    ("Tennis", "http://rss.cnn.com/rss/edition_tennis.rss"),
    ("Travel", "http://rss.cnn.com/rss/edition_travel.rss"),
    ("Video", "http://rss.cnn.com/rss/cnn_freevideo.rss"),
    ("Most Recent", "http://rss.cnn.com/rss/cnn_latest.rss")
]

fox_rss_feeds = [
    ("Headlines", "http://feeds.foxnews.com/foxnews/latest"),
    ("National", "http://feeds.foxnews.com/foxnews/national"),
    ("World", "http://feeds.foxnews.com/foxnews/world"),
    ("Politics", "http://feeds.foxnews.com/foxnews/politics"),
    ("Business", "http://feeds.foxnews.com/foxnews/business"),
    ("SciTech", "http://feeds.foxnews.com/foxnews/scitech"),
    ("Health", "http://feeds.foxnews.com/foxnews/health"),
    ("Entertainment", "http://feeds.foxnews.com/foxnews/entertainment"),
    ("Views", "http://feeds.foxnews.com/foxnews/views"),
    ("Blogs", "http://feeds.foxnews.com/foxnews/foxblogs"),
    ("Mike Straka's Grrr!", "http://feeds.foxnews.com/foxnews/column/grrr"),
    ("Pop Tarts", "http://feeds.foxnews.com/foxnews/column/poptarts"),
    ("FOX 411", "http://feeds.foxnews.com/foxnews/column/fox411")
]

yahoo_rss_feeds = [
    ("Headlines", "https://www.yahoo.com/news/rss"),
    ("Finance", "https://finance.yahoo.com/news/rssindex"),
    ("Entertainment", "https://www.yahoo.com/entertainment/rss"),
    ("Lifestyle", "https://www.yahoo.com/lifestyle/rss"),
    ("Good Morning America", "https://www.yahoo.com/gma/rss"),
    ("World", "https://news.yahoo.com/rss/world")
]

buzzfeed_rss_feeds = [
    ("Homepage", "https://www.buzzfeed.com/index.xml"),
    ("Raw Feed", "https://www.buzzfeed.com/raw.xml"),
    ("USNews", "https://www.buzzfeed.com/usnews.xml"),
    ("Quiz", "https://www.buzzfeed.com/quiz.xml"),
    ("LOL", "https://www.buzzfeed.com/lol.xml"),
    ("WTF", "https://www.buzzfeed.com/wtf.xml"),
    ("Fail", "https://www.buzzfeed.com/fail.xml"),
    ("Win", "https://www.buzzfeed.com/win.xml"),
    ("OMG", "https://www.buzzfeed.com/omg.xml"),
    ("Animals", "https://www.buzzfeed.com/animals.xml"),
    ("Australia", "https://www.buzzfeed.com/australia.xml"),
    ("Books", "https://www.buzzfeed.com/books.xml"),
    ("Brasil", "https://www.buzzfeed.com/brasil.xml"),
    ("Celebrity", "https://www.buzzfeed.com/celebrity.xml"),
    ("Comedy", "https://www.buzzfeed.com/comedy.xml"),
    ("Comics", "https://www.buzzfeed.com/comics.xml"),
    ("Community", "https://www.buzzfeed.com/community.xml"),
    ("Cute", "https://www.buzzfeed.com/cute.xml"),
    ("DIY", "https://www.buzzfeed.com/diy.xml"),
    ("Entertainment", "https://www.buzzfeed.com/tvandmovies.xml"),
    ("Espanol", "https://www.buzzfeed.com/espanol.xml"),
    ("Food", "https://www.buzzfeed.com/food.xml"),
    ("France", "https://www.buzzfeed.com/france.xml"),
    ("FWD", "https://www.buzzfeed.com/fwd.xml"),
    ("Geeky", "https://www.buzzfeed.com/geeky.xml"),
    ("Health", "https://www.buzzfeed.com/health.xml"),
    ("Japan", "https://www.buzzfeed.com/japan.xml"),
    ("JapanNews", "https://www.buzzfeed.com/japannews.xml"),
    ("LGBT", "https://www.buzzfeed.com/lgbt.xml"),
    ("Longform", "https://www.buzzfeed.com/longform.xml"),
    ("Politics", "https://www.buzzfeed.com/politics.xml"),
    ("Puzzles", "https://www.buzzfeed.com/puzzles.xml"),
    ("Reader", "https://www.buzzfeed.com/reader.xml"),
    ("Rewind", "https://www.buzzfeed.com/rewind.xml"),
    ("Sports", "https://www.buzzfeed.com/sports.xml"),
    ("Tech", "https://www.buzzfeed.com/tech.xml"),
    ("Trashy", "https://www.buzzfeed.com/trashy.xml"),
    ("Travel", "https://www.buzzfeed.com/travel.xml"),
    ("UKCelebrity", "https://www.buzzfeed.com/ukcelebrity.xml"),
    ("UKMusic", "https://www.buzzfeed.com/ukmusic.xml"),
    ("UKTVAndMovies", "https://www.buzzfeed.com/uktvandmovies.xml"),
    ("Weddings", "https://www.buzzfeed.com/weddings.xml"),
    ("World", "https://www.buzzfeed.com/world.xml"),
    ("Business", "https://www.buzzfeed.com/business.xml"),
    ("Celebrity", "https://www.buzzfeed.com/category/celebrity.xml"),
    ("Collections", "https://www.buzzfeed.com/badge/collection.xml"),
    ("Culture", "https://www.buzzfeed.com/category/culture.xml"),
    ("Food", "https://www.buzzfeed.com/category/food.xml"),
    ("Gross", "https://www.buzzfeed.com/ew.xml"),
    ("Music", "https://www.buzzfeed.com/music.xml"),
    ("NSFW", "https://www.buzzfeed.com/nsfw.xml"),
    ("Pics", "https://www.buzzfeed.com/pics.xml"),
    ("Science", "https://www.buzzfeed.com/science.xml"),
    ("Style", "https://www.buzzfeed.com/style.xml"),
    ("TV", "https://www.buzzfeed.com/tv.xml")
]

guardian_rss_feeds = [
    ("Coronavirus", "https://www.theguardian.com/world/coronavirus-outbreak/rss"),
    ("World news", "https://www.theguardian.com/world/rss"),
    ("UK news", "https://www.theguardian.com/uk-news/rss"),
    ("Environment", "https://www.theguardian.com/uk/environment/rss"),
    ("Science", "https://www.theguardian.com/science/rss"),
    ("Global development", "https://www.theguardian.com/global-development/rss"),
    ("Football", "https://www.theguardian.com/football/rss"),
    ("Tech", "https://www.theguardian.com/uk/technology/rss"),
    ("Business", "https://www.theguardian.com/uk/business/rss"),
    ("Obituaries", "https://www.theguardian.com/tone/obituaries/rss"),
    ("The Guardian view", "https://www.theguardian.com/profile/editorial/rss"),
    ("Columnists", "https://www.theguardian.com/index/contributors/rss"),
    ("Cartoons", "https://www.theguardian.com/cartoons/archive/rss"),
    ("Opinion videos", "https://www.theguardian.com/type/video+tone/comment/rss"),
    ("Letters", "https://www.theguardian.com/tone/letters/rss"),
    ("Football", "https://www.theguardian.com/football/rss"),
    ("Cricket", "https://www.theguardian.com/sport/cricket/rss"),
    ("Rugby union", "https://www.theguardian.com/sport/rugby-union/rss"),
    ("Tennis", "https://www.theguardian.com/sport/tennis/rss"),
    ("Cycling", "https://www.theguardian.com/sport/cycling/rss"),
    ("F1", "https://www.theguardian.com/sport/formulaone/rss"),
    ("Golf", "https://www.theguardian.com/sport/golf/rss"),
    ("US sports", "https://www.theguardian.com/sport/us-sport/rss"),
    ("Books", "https://www.theguardian.com/books/rss"),
    ("Music", "https://www.theguardian.com/music/rss"),
    ("TV & radio", "https://www.theguardian.com/uk/tv-and-radio/rss"),
    ("Art & design", "https://www.theguardian.com/artanddesign/rss"),
    ("Film", "https://www.theguardian.com/uk/film/rss"),
    ("Games", "https://www.theguardian.com/games/rss"),
    ("Classical", "https://www.theguardian.com/music/classicalmusicandopera/rss"),
    ("Stage", "https://www.theguardian.com/stage/rss"),
    ("Fashion", "https://www.theguardian.com/fashion/rss"),
    ("Food", "https://www.theguardian.com/food/rss"),
    ("Recipes", "https://www.theguardian.com/tone/recipes/rss"),
    ("Love & sex", "https://www.theguardian.com/lifeandstyle/love-and-sex/rss"),
    ("Health & fitness", "https://www.theguardian.com/lifeandstyle/health-and-wellbeing/rss"),
    ("Home & garden", "https://www.theguardian.com/lifeandstyle/home-and-garden/rss"),
    ("Women", "https://www.theguardian.com/lifeandstyle/women/rss"),
    ("Men", "https://www.theguardian.com/lifeandstyle/men/rss"),
    ("Family", "https://www.theguardian.com/lifeandstyle/family/rss"),
    ("Travel", "https://www.theguardian.com/uk/travel/rss"),
    ("Money", "https://www.theguardian.com/uk/money/rss")
]

washington_post_rss_feeds = [
    ("PowerPost", "http://feeds.washingtonpost.com/rss/rss_powerpost?itid=lk_inline_manual_4/rss"),
    ("The Fact Checker", "http://feeds.washingtonpost.com/rss/rss_fact-checker?itid=lk_inline_manual_5/rss"),
    ("The Fix", "http://feeds.washingtonpost.com/rss/rss_the-fix?itid=lk_inline_manual_6/rss"),
    ("Monkey Cage", "http://feeds.washingtonpost.com/rss/rss_monkey-cage?itid=lk_inline_manual_7/rss"),
    ("Alyssa Rosenberg's 'Act Four'", "http://feeds.washingtonpost.com/rss/rss_act-four?itid=lk_inline_manual_10/rss"),
    ("All Opinions Are Local", "http://feeds.washingtonpost.com/rss/rss_all-opinions-are-local?itid=lk_inline_manual_11/rss"),
    ("Alexandra Petri", "http://feeds.washingtonpost.com/rss/rss_compost?itid=lk_inline_manual_12/rss"),
    ("Carlos Lozada’s ‘Book Party’", "http://feeds.washingtonpost.com/rss/rss_book-party?itid=lk_inline_manual_13/rss"),
    ("Erik Wemple", "http://feeds.washingtonpost.com/rss/rss_erik-wemple?itid=lk_inline_manual_14/rss"),
    ("Greg Sargent's 'The Plum Line'", "http://feeds.washingtonpost.com/rss/rss_plum-line?itid=lk_inline_manual_15/rss"),
    ("PostPartisan", "http://feeds.washingtonpost.com/rss/rss_post-partisan?itid=lk_inline_manual_16/rss"),
    ("PostEverything", "http://feeds.washingtonpost.com/rss/rss_post-everything?itid=lk_inline_manual_17/rss"),
    ("Catherine Rampell", "http://feeds.washingtonpost.com/rss/rss_rampage?itid=lk_inline_manual_18/rss"),
    ("Jennifer Rubin", "http://feeds.washingtonpost.com/rss/rss_right-turn?itid=lk_inline_manual_19/rss"),
    ("Tom Toles", "http://feeds.washingtonpost.com/rss/rss_tom-toles?itid=lk_inline_manual_20/rss"),
    ("Radley Balko", "http://feeds.washingtonpost.com/rss/rss_the-watch?itid=lk_inline_manual_21/rss"),
    ("Capital Weather Gang", "http://feeds.washingtonpost.com/rss/rss_capital-weather-gang?itid=lk_inline_manual_25/rss"),
    ("High School Sports", "http://feeds.washingtonpost.com/rss/rss_recruiting-insider?itid=lk_inline_manual_31/rss"),
    ("DC Sports Bog", "http://feeds.washingtonpost.com/rss/rss_dc-sports-bog?itid=lk_inline_manual_32/rss"),
    ("Washington Redskins", "http://feeds.washingtonpost.com/rss/rss_football-insider?itid=lk_inline_manual_33/rss"),
    ("Maryland Terrapins", "http://feeds.washingtonpost.com/rss/rss_terrapins-insider?itid=lk_inline_manual_34/rss"),
    ("Soccer", "http://feeds.washingtonpost.com/rss/rss_soccer-insider?itid=lk_inline_manual_35/rss"),
    ("Washington Capitals", "http://feeds.washingtonpost.com/rss/rss_capitals-insider?itid=lk_inline_manual_36/rss"),
    ("Washington Nationals", "http://feeds.washingtonpost.com/rss/rss_nationals-journal?itid=lk_inline_manual_37/rss"),
    ("Washington Wizards", "http://feeds.washingtonpost.com/rss/rss_wizards-insider?itid=lk_inline_manual_38/rss"),
    ("Innovations", "http://feeds.washingtonpost.com/rss/rss_innovations?itid=lk_inline_manual_41/rss"),
    ("Morning Mix", "http://feeds.washingtonpost.com/rss/rss_morning-mix?itid=lk_inline_manual_42/rss"),
    ("Leadership", "http://feeds.washingtonpost.com/rss/rss_on-leadership?itid=lk_inline_manual_46/rss"),
    ("Arts & Entertainment", "http://feeds.washingtonpost.com/rss/rss_arts-post?itid=lk_inline_manual_49/rss"),
    ("Relationships", "http://feeds.washingtonpost.com/rss/rss_soloish?itid=lk_inline_manual_50/rss"),
    ("The Reliable Source", "http://feeds.washingtonpost.com/rss/rss_reliable-source?itid=lk_inline_manual_51/rss"),
    ("Comics", "http://feeds.washingtonpost.com/rss/rss_comic-riffs?itid=lk_inline_manual_54/rss"),
    ("Going Out Guide", "http://feeds.washingtonpost.com/rss/rss_going-out-gurus?itid=lk_inline_manual_55/rss"),
    ("Entertainment", "http://feeds.washingtonpost.com/rss/entertainment?itid=lk_inline_manual_53"),
    ("United States", "http://feeds.washingtonpost.com/rss/local?itid=lk_inline_manual_23")
]

cnbc_rss_feeds = [
    ("Top News", "https://www.cnbc.com/id/100003114/device/rss/rss.html/rss"),
    ("World News", "https://www.cnbc.com/id/100727362/device/rss/rss.html/rss"),
    ("US News", "https://www.cnbc.com/id/15837362/device/rss/rss.html/rss"),
    ("Asia News", "https://www.cnbc.com/id/19832390/device/rss/rss.html/rss"),
    ("Europe News", "https://www.cnbc.com/id/19794221/device/rss/rss.html/rss"),
    ("Business", "https://www.cnbc.com/id/10001147/device/rss/rss.html/rss"),
    ("Earnings", "https://www.cnbc.com/id/15839135/device/rss/rss.html/rss"),
    ("Commentary", "https://www.cnbc.com/id/100370673/device/rss/rss.html/rss"),
    ("Economy", "https://www.cnbc.com/id/20910258/device/rss/rss.html/rss"),
    ("Finance", "https://www.cnbc.com/id/10000664/device/rss/rss.html/rss"),
    ("Technology", "https://www.cnbc.com/id/19854910/device/rss/rss.html/rss"),
    ("Politics", "https://www.cnbc.com/id/10000113/device/rss/rss.html/rss"),
    ("Health Care", "https://www.cnbc.com/id/10000108/device/rss/rss.html/rss"),
    ("Real Estate", "https://www.cnbc.com/id/10000115/device/rss/rss.html/rss"),
    ("Wealth", "https://www.cnbc.com/id/10001054/device/rss/rss.html/rss"),
    ("Autos", "https://www.cnbc.com/id/10000101/device/rss/rss.html/rss"),
    ("Energy", "https://www.cnbc.com/id/19836768/device/rss/rss.html/rss"),
    ("Media", "https://www.cnbc.com/id/10000110/device/rss/rss.html/rss"),
    ("Retail", "https://www.cnbc.com/id/10000116/device/rss/rss.html/rss"),
    ("Travel", "https://www.cnbc.com/id/10000739/device/rss/rss.html/rss"),
    ("Small Business", "https://www.cnbc.com/id/44877279/device/rss/rss.html/rss"),
    ("Investing", "https://www.cnbc.com/id/15839069/device/rss/rss.html/rss"),
    ("Financial Advisors", "https://www.cnbc.com/id/100646281/device/rss/rss.html/rss"),
    ("Personal Finance", "https://www.cnbc.com/id/21324812/device/rss/rss.html/rss"),
    ("Charting Asia", "https://www.cnbc.com/id/23103686/device/rss/rss.html/rss"),
    ("Funny Business", "https://www.cnbc.com/id/17646093/device/rss/rss.html/rss"),
    ("Market Insider", "https://www.cnbc.com/id/20409666/device/rss/rss.html/rss"),
    ("NetNet", "https://www.cnbc.com/id/38818154/device/rss/rss.html/rss"),
    ("Trader Talk", "https://www.cnbc.com/id/20398120/device/rss/rss.html/rss"),
    ("Buffett Watch", "https://www.cnbc.com/id/19206666/device/rss/rss.html/rss"),
    ("Top Video", "https://www.cnbc.com/id/15839263/device/rss/rss.html/rss"),
    ("Digital Workshop", "https://www.cnbc.com/id/100616801/device/rss/rss.html/rss"),
    ("Latest Video", "https://www.cnbc.com/id/100004038/device/rss/rss.html/rss"),
    ("CEO Interviews", "https://www.cnbc.com/id/100004032/device/rss/rss.html/rss"),
    ("Analyst Interviews", "https://www.cnbc.com/id/100004033/device/rss/rss.html/rss"),
    ("Must Watch", "https://www.cnbc.com/id/101014894/device/rss/rss.html/rss"),
    ("Squawk Box", "https://www.cnbc.com/id/15838368/device/rss/rss.html/rss"),
    ("Squawk on the Street", "https://www.cnbc.com/id/15838381/device/rss/rss.html/rss"),
    ("Power Lunch", "https://www.cnbc.com/id/15838342/device/rss/rss.html/rss"),
    ("Street Signs ", "https://www.cnbc.com/id/15838408/device/rss/rss.html/rss"),
    ("Options Action", "https://www.cnbc.com/id/28282083/device/rss/rss.html/rss"),
    ("Closing Bell", "https://www.cnbc.com/id/15838421/device/rss/rss.html/rss"),
    ("Fast Money", "https://www.cnbc.com/id/15838499/device/rss/rss.html/rss"),
    ("Mad Money", "https://www.cnbc.com/id/15838459/device/rss/rss.html/rss"),
    ("Kudlow Report", "https://www.cnbc.com/id/15838446/device/rss/rss.html/rss"),
    ("Futures Now", "https://www.cnbc.com/id/48227449/device/rss/rss.html/rss"),
    ("Suze Orman", "https://www.cnbc.com/id/15838523/device/rss/rss.html/rss"),
    ("Capital Connection", "https://www.cnbc.com/id/17501773/device/rss/rss.html/rss"),
    ("Squawk Box Europe", "https://www.cnbc.com/id/15838652/device/rss/rss.html/rss"),
    ("Worldwide Exchange", "https://www.cnbc.com/id/15838355/device/rss/rss.html/rss"),
    ("Squawk Box Asia", "https://www.cnbc.com/id/15838831/device/rss/rss.html/rss"),
    ("The Call", "https://www.cnbc.com/id/37447855/device/rss/rss.html/rss")
]

rt_rss_feeds = [
    ("General", "https://www.rt.com/rss"),
    ("News", "https://www.rt.com/rss/news"),
    ("USA", "https://www.rt.com/rss/usa"),
    ("UK", "https://www.rt.com/rss/uk"),
    ("Sport", "https://www.rt.com/rss/sport"),
    ("Russia", "https://www.rt.com/rss/russia"),
    ("Business", "https://www.rt.com/rss/business"),
    ("Op-ed", "https://www.rt.com/rss/op-ed"),
    ("RT360", "https://www.rt.com/rss/applenews/rt360"),
    ("Newsline", "https://www.rt.com/rss/newsline"),
    ("Podcasts", "https://www.rt.com/rss/podcasts"),
    ("RSS Feed", "https://www.rt.com/rss-feed")
]

npr_rss_feeds = [
    ("Wait Wait...Don't Tell Me!", "https://feeds.npr.org/35/rss.xml/rss"),
    ("World of Opera", "https://feeds.npr.org/36/rss.xml/rss"),
    ("All Songs Considered", "https://feeds.npr.org/37/rss.xml/rss"),
    ("On Point", "https://feeds.npr.org/38/rss.xml/rss"),
    ("Tell Me More", "https://feeds.npr.org/46/rss.xml/rss"),
    ("The Bryant Park Project", "https://feeds.npr.org/47/rss.xml/rss"),
    ("TED Radio Hour", "https://feeds.npr.org/57/rss.xml/rss"),
    ("Ask Me Another", "https://feeds.npr.org/58/rss.xml/rss"),
    ("Vermont Edition", "https://feeds.npr.org/59/rss.xml/rss"),
    ("Here & Now", "https://feeds.npr.org/60/rss.xml/rss"),
    ("Science Friday", "https://feeds.npr.org/61/rss.xml/rss"),
    ("Snap Judgment", "https://feeds.npr.org/62/rss.xml/rss"),
    ("Invisibilia", "https://feeds.npr.org/64/rss.xml/rss"),
    ("1A", "https://feeds.npr.org/65/rss.xml/rss"),
    ("News", "https://feeds.npr.org/1001/rss.xml"),
    ("News", "https://feeds.npr.org/1002/rss.xml"),
    ("National", "https://feeds.npr.org/1003/rss.xml"),
    ("World", "https://feeds.npr.org/1004/rss.xml"),
    ("Summer Reading 2006", "https://feeds.npr.org/1005/rss.xml"),
    ("Business", "https://feeds.npr.org/1006/rss.xml"),
    ("Science", "https://feeds.npr.org/1007/rss.xml"),
    ("Arts & Life", "https://feeds.npr.org/1008/rss.xml"),
    ("Middle East", "https://feeds.npr.org/1009/rss.xml"),
    ("Archived Topic: Iraq", "https://feeds.npr.org/1010/rss.xml"),
    ("Election 2004", "https://feeds.npr.org/1011/rss.xml"),
    ("Politics", "https://feeds.npr.org/1012/rss.xml"),
    ("Education", "https://feeds.npr.org/1013/rss.xml"),
    ("Politics", "https://feeds.npr.org/1014/rss.xml"),
    ("Race", "https://feeds.npr.org/1015/rss.xml"),
    ("Religion", "https://feeds.npr.org/1016/rss.xml"),
    ("Economy", "https://feeds.npr.org/1017/rss.xml"),
    ("Your Money", "https://feeds.npr.org/1018/rss.xml"),
    ("Technology", "https://feeds.npr.org/1019/rss.xml"),
    ("Media", "https://feeds.npr.org/1020/rss.xml"),
    ("Radio Expeditions", "https://feeds.npr.org/1023/rss.xml"),
    ("Research News", "https://feeds.npr.org/1024/rss.xml"),
    ("Environment", "https://feeds.npr.org/1025/rss.xml"),
    ("Space", "https://feeds.npr.org/1026/rss.xml"),
    ("Health Care", "https://feeds.npr.org/1027/rss.xml"),
    ("On Aging", "https://feeds.npr.org/1028/rss.xml"),
    ("Mental Health", "https://feeds.npr.org/1029/rss.xml"),
    ("Children's Health", "https://feeds.npr.org/1030/rss.xml"),
    ("Global Health", "https://feeds.npr.org/1031/rss.xml"),
    ("Books", "https://feeds.npr.org/1032/rss.xml"),
    ("Author Interviews", "https://feeds.npr.org/1033/rss.xml"),
    ("Book Reviews", "https://feeds.npr.org/1034/rss.xml"),
    ("Music", "https://feeds.npr.org/1039/rss.xml"),
    ("In Performance", "https://feeds.npr.org/1040/rss.xml"),
    ("Movies", "https://feeds.npr.org/1045/rss.xml"),
    ("Performing Arts", "https://feeds.npr.org/1046/rss.xml"),
    ("Art & Design", "https://feeds.npr.org/1047/rss.xml"),
    ("Pop Culture", "https://feeds.npr.org/1048/rss.xml"),
    ("Diversions", "https://feeds.npr.org/1051/rss.xml"),
    ("Games & Humor", "https://feeds.npr.org/1052/rss.xml"),
    ("Food", "https://feeds.npr.org/1053/rss.xml"),
    ("Gardening", "https://feeds.npr.org/1054/rss.xml"),
    ("Sports", "https://feeds.npr.org/1055/rss.xml"),
    ("World Story of the Day", "https://feeds.npr.org/1056/rss.xml"),
    ("Opinion", "https://feeds.npr.org/1057/rss.xml"),
    ("Analysis", "https://feeds.npr.org/1059/rss.xml"),
    ("From Our Listeners", "https://feeds.npr.org/1061/rss.xml"),
    ("Obituaries", "https://feeds.npr.org/1062/rss.xml"),
    ("Summer Reading 2006: Excerpts", "https://feeds.npr.org/1064/rss.xml"),
    ("Holidays", "https://feeds.npr.org/1065/rss.xml"),
    ("Your Health", "https://feeds.npr.org/1066/rss.xml"),
    ("Election 2006", "https://feeds.npr.org/1067/rss.xml"),
    ("Summer Reading 2006: Cookbooks", "https://feeds.npr.org/1068/rss.xml"),
    ("Law", "https://feeds.npr.org/1070/rss.xml"),
    ("Summer Olympics '04", "https://feeds.npr.org/1071/rss.xml"),
    ("Democratic Convention 2004", "https://feeds.npr.org/1072/rss.xml"),
    ("Republican Convention 2004", "https://feeds.npr.org/1073/rss.xml"),
    ("Lost & Found Sound", "https://feeds.npr.org/1074/rss.xml"),
    ("Low-Wage America", "https://feeds.npr.org/1076/rss.xml"),
    ("The Second Term", "https://feeds.npr.org/1077/rss.xml"),
    ("The Impact of War", "https://feeds.npr.org/1078/rss.xml"),
    ("Indian Ocean Tsunami 2004-05", "https://feeds.npr.org/1081/rss.xml"),
    ("Social Security Debate", "https://feeds.npr.org/1083/rss.xml"),
    ("Summer Reading 2005", "https://feeds.npr.org/1084/rss.xml"),
    ("Summer Reading: Fiction", "https://feeds.npr.org/1085/rss.xml"),
    ("Summer Reading: Kids", "https://feeds.npr.org/1086/rss.xml"),
    ("Summer Reading: Cooking", "https://feeds.npr.org/1087/rss.xml"),
    ("Summer", "https://feeds.npr.org/1088/rss.xml"),
    ("Summer Reading: Nonfiction", "https://feeds.npr.org/1089/rss.xml"),
    ("Story of the Day", "https://feeds.npr.org/1090/rss.xml"),
    ("Winter Olympics '06", "https://feeds.npr.org/1092/rss.xml"),
    ("Katrina & Beyond", "https://feeds.npr.org/1093/rss.xml"),
    ("Business Story of the Day", "https://feeds.npr.org/1095/rss.xml"),
    ("Holiday Story of the Day", "https://feeds.npr.org/1096/rss.xml"),
    ("Holiday Books 2005", "https://feeds.npr.org/1097/rss.xml"),
    ("Holiday Music 2005", "https://feeds.npr.org/1098/rss.xml"),
    ("Holiday Food 2005", "https://feeds.npr.org/1099/rss.xml"),
    ("World Cup 2006", "https://feeds.npr.org/1100/rss.xml"),
    ("Archived Topic: Israeli-Palestinian Coverage", "https://feeds.npr.org/1101/rss.xml"),
    ("Election 2008", "https://feeds.npr.org/1102/rss.xml"),
    ("Studio Sessions", "https://feeds.npr.org/1103/rss.xml"),
    ("Music Reviews", "https://feeds.npr.org/1104/rss.xml"),
    ("Music Interviews", "https://feeds.npr.org/1105/rss.xml"),
    ("Music News", "https://feeds.npr.org/1106/rss.xml"),
    ("Music Lists", "https://feeds.npr.org/1107/rss.xml"),
    ("New Music", "https://feeds.npr.org/1108/rss.xml"),
    ("Concerts", "https://feeds.npr.org/1109/rss.xml"),
    ("Music Videos", "https://feeds.npr.org/1110/rss.xml"),
    ("Election 2008: Issues", "https://feeds.npr.org/1111/rss.xml"),
    ("Election 2008: Voting Groups", "https://feeds.npr.org/1112/rss.xml"),
    ("Election 2008: Money, Media & Influence", "https://feeds.npr.org/1113/rss.xml"),
    ("Election 2008: Congressional & State Races", "https://feeds.npr.org/1114/rss.xml"),
    ("Election 2008: On the Campaign Trail", "https://feeds.npr.org/1115/rss.xml"),
    ("Sen. Hillary Clinton (D-NY)", "https://feeds.npr.org/1116/rss.xml"),
    ("Sen. Barack Obama (D-IL)", "https://feeds.npr.org/1117/rss.xml"),
    ("Sen. John McCain (R-AZ)", "https://feeds.npr.org/1118/rss.xml"),
    ("Sen. Joseph Biden (D-DE)", "https://feeds.npr.org/1119/rss.xml"),
    ("Gov. Sarah Palin", "https://feeds.npr.org/1120/rss.xml"),
    ("Election 2008: Voting Problems", "https://feeds.npr.org/1121/rss.xml"),
    ("National Security", "https://feeds.npr.org/1122/rss.xml"),
    ("Europe", "https://feeds.npr.org/1124/rss.xml"),
    ("Asia", "https://feeds.npr.org/1125/rss.xml"),
    ("Africa", "https://feeds.npr.org/1126/rss.xml"),
    ("Latin America", "https://feeds.npr.org/1127/rss.xml"),
    ("Health", "https://feeds.npr.org/1128/rss.xml"),
    ("Energy", "https://feeds.npr.org/1131/rss.xml"),
    ("Animals", "https://feeds.npr.org/1132/rss.xml"),
    ("On Disabilities", "https://feeds.npr.org/1133/rss.xml"),
    ("Fitness & Nutrition", "https://feeds.npr.org/1134/rss.xml"),
    ("Medical Treatments", "https://feeds.npr.org/1135/rss.xml"),
    ("History", "https://feeds.npr.org/1136/rss.xml"),
    ("Movie Interviews", "https://feeds.npr.org/1137/rss.xml"),
    ("Television", "https://feeds.npr.org/1138/rss.xml"),
    ("Recipes", "https://feeds.npr.org/1139/rss.xml"),
    ("Fine Art", "https://feeds.npr.org/1141/rss.xml"),
    ("Architecture", "https://feeds.npr.org/1142/rss.xml"),
    ("Photography", "https://feeds.npr.org/1143/rss.xml"),
    ("Theater", "https://feeds.npr.org/1144/rss.xml"),
    ("Dance", "https://feeds.npr.org/1145/rss.xml"),
    ("Strange News", "https://feeds.npr.org/1146/rss.xml"),
    ("Archived Topic: Afghanistan", "https://feeds.npr.org/1149/rss.xml"),
    ("Investigations", "https://feeds.npr.org/1150/rss.xml"),
    ("Music Quizzes", "https://feeds.npr.org/1151/rss.xml"),
    ("Book News & Features", "https://feeds.npr.org/1161/rss.xml"),
    ("Impact", "https://feeds.npr.org/1162/rss.xml"),
    ("TV Reviews", "https://feeds.npr.org/1163/rss.xml"),
    ("Family", "https://feeds.npr.org/1164/rss.xml"),
    ("Weather", "https://feeds.npr.org/1165/rss.xml"),
    ("Arts", "https://feeds.npr.org/2000/rss.xml"),
    ("Design", "https://feeds.npr.org/2001/rss.xml"),
    ("Fashion & Beauty", "https://feeds.npr.org/2002/rss.xml"),
    ("Food", "https://feeds.npr.org/2003/rss.xml"),
    ("Books", "https://feeds.npr.org/2004/rss.xml"),
    ("Performing Arts", "https://feeds.npr.org/2005/rss.xml"),
    ("Visual Arts", "https://feeds.npr.org/2006/rss.xml"),
    ("Business", "https://feeds.npr.org/2007/rss.xml"),
    ("Business News", "https://feeds.npr.org/2008/rss.xml"),
    ("Careers", "https://feeds.npr.org/2009/rss.xml"),
    ("Investing", "https://feeds.npr.org/2010/rss.xml"),
    ("Management & Marketing", "https://feeds.npr.org/2011/rss.xml"),
    ("Shopping", "https://feeds.npr.org/2012/rss.xml"),
    ("Comedy", "https://feeds.npr.org/2013/rss.xml"),
    ("Education", "https://feeds.npr.org/2014/rss.xml"),
    ("Education Technology", "https://feeds.npr.org/2015/rss.xml"),
    ("Higher Education", "https://feeds.npr.org/2016/rss.xml"),
    ("K-12", "https://feeds.npr.org/2017/rss.xml"),
    ("Language Courses", "https://feeds.npr.org/2018/rss.xml"),
    ("Training", "https://feeds.npr.org/2019/rss.xml"),
    ("Leisure", "https://feeds.npr.org/2020/rss.xml"),
    ("Automotive", "https://feeds.npr.org/2021/rss.xml"),
    ("Aviation", "https://feeds.npr.org/2022/rss.xml"),
    ("Hobbies", "https://feeds.npr.org/2023/rss.xml"),
    ("Other Games", "https://feeds.npr.org/2024/rss.xml"),
    ("Video Games", "https://feeds.npr.org/2025/rss.xml"),
    ("Government", "https://feeds.npr.org/2026/rss.xml"),
    ("Local", "https://feeds.npr.org/2027/rss.xml"),
    ("National", "https://feeds.npr.org/2028/rss.xml"),
    ("Non-Profit", "https://feeds.npr.org/2029/rss.xml"),
    ("Regional", "https://feeds.npr.org/2030/rss.xml"),
    ("Health & Fitness", "https://feeds.npr.org/2031/rss.xml"),
    ("Alternative Health", "https://feeds.npr.org/2032/rss.xml"),
    ("Fitness & Nutrition", "https://feeds.npr.org/2033/rss.xml"),
    ("Self-Help", "https://feeds.npr.org/2034/rss.xml"),
    ("Sexuality", "https://feeds.npr.org/2035/rss.xml"),
    ("Kids & Family", "https://feeds.npr.org/2036/rss.xml"),
    ("Music", "https://feeds.npr.org/2037/rss.xml"),
    ("News", "https://feeds.npr.org/2038/rss.xml"),
    ("Religion & Spirituality", "https://feeds.npr.org/2039/rss.xml"),
    ("Buddhism", "https://feeds.npr.org/2040/rss.xml"),
    ("Christianity", "https://feeds.npr.org/2041/rss.xml"),
    ("Hinduism", "https://feeds.npr.org/2042/rss.xml"),
    ("Islam", "https://feeds.npr.org/2043/rss.xml"),
    ("Judaism", "https://feeds.npr.org/2044/rss.xml"),
    ("Other", "https://feeds.npr.org/2045/rss.xml"),
    ("Spirituality", "https://feeds.npr.org/2046/rss.xml"),
    ("Science", "https://feeds.npr.org/2047/rss.xml"),
    ("Medicine", "https://feeds.npr.org/2048/rss.xml"),
    ("Natural Sciences", "https://feeds.npr.org/2049/rss.xml"),
    ("Social Sciences", "https://feeds.npr.org/2050/rss.xml"),
    ("Society & Culture", "https://feeds.npr.org/2051/rss.xml"),
    ("History", "https://feeds.npr.org/2052/rss.xml"),
    ("Personal Journals", "https://feeds.npr.org/2053/rss.xml"),
    ("Philosophy", "https://feeds.npr.org/2054/rss.xml"),
    ("Places & Travel", "https://feeds.npr.org/2055/rss.xml"),
    ("Sports", "https://feeds.npr.org/2056/rss.xml"),
    ("Amateur", "https://feeds.npr.org/2057/rss.xml"),
    ("College & High School", "https://feeds.npr.org/2058/rss.xml"),
    ("Outdoor", "https://feeds.npr.org/2059/rss.xml"),
    ("Professional", "https://feeds.npr.org/2060/rss.xml"),
    ("Technology", "https://feeds.npr.org/2061/rss.xml"),
    ("Gadgets", "https://feeds.npr.org/2062/rss.xml"),
    ("Tech News", "https://feeds.npr.org/2063/rss.xml"),
    ("Podcasting", "https://feeds.npr.org/2064/rss.xml"),
    ("Software How-To", "https://feeds.npr.org/2065/rss.xml"),
    ("TV & Film", "https://feeds.npr.org/2066/rss.xml"),
    ("Fiction", "https://feeds.npr.org/2067/rss.xml"),
    ("History", "https://feeds.npr.org/2068/rss.xml"),
    ("True Crime", "https://feeds.npr.org/2069/rss.xml"),
    ("Drama", "https://feeds.npr.org/2070/rss.xml"),
    ("Science Fiction", "https://feeds.npr.org/2071/rss.xml"),
    ("Comedy Fiction", "https://feeds.npr.org/2072/rss.xml"),
    ("Management", "https://feeds.npr.org/2073/rss.xml"),
    ("Marketing", "https://feeds.npr.org/2074/rss.xml"),
    ("Improv", "https://feeds.npr.org/2075/rss.xml"),
    ("Comedy Interviews", "https://feeds.npr.org/2076/rss.xml"),
    ("Standup", "https://feeds.npr.org/2077/rss.xml"),
    ("Language Learning", "https://feeds.npr.org/2078/rss.xml"),
    ("How To", "https://feeds.npr.org/2079/rss.xml"),
    ("Self Improvement", "https://feeds.npr.org/2080/rss.xml"),
    ("Courses", "https://feeds.npr.org/2081/rss.xml"),
    ("Crafts", "https://feeds.npr.org/2082/rss.xml"),
    ("Games", "https://feeds.npr.org/2083/rss.xml"),
    ("Home & Garden", "https://feeds.npr.org/2084/rss.xml"),
    ("Animation & Manga", "https://feeds.npr.org/2085/rss.xml"),
    ("Fitness", "https://feeds.npr.org/2086/rss.xml"),
    ("Nutrition", "https://feeds.npr.org/2087/rss.xml"),
    ("Mental Health", "https://feeds.npr.org/2088/rss.xml"),
    ("Education for Kids", "https://feeds.npr.org/2089/rss.xml"),
    ("Stories for Kids", "https://feeds.npr.org/2090/rss.xml"),
    ("Parenting", "https://feeds.npr.org/2091/rss.xml"),
    ("Pets & Animals", "https://feeds.npr.org/2092/rss.xml"),
    ("Music Commentary", "https://feeds.npr.org/2093/rss.xml"),
    ("Music History", "https://feeds.npr.org/2094/rss.xml"),
    ("Music Interviews", "https://feeds.npr.org/2095/rss.xml"),
    ("Daily News", "https://feeds.npr.org/2096/rss.xml"),
    ("Politics", "https://feeds.npr.org/2097/rss.xml"),
    ("Sports News", "https://feeds.npr.org/2098/rss.xml"),
    ("News Commentary", "https://feeds.npr.org/2099/rss.xml"),
    ("Entertainment News", "https://feeds.npr.org/2100/rss.xml"),
    ("Religion", "https://feeds.npr.org/2101/rss.xml"),
    ("Mathematics", "https://feeds.npr.org/2102/rss.xml"),
    ("Nature", "https://feeds.npr.org/2103/rss.xml"),
    ("Astronomy", "https://feeds.npr.org/2104/rss.xml"),
    ("Chemistry", "https://feeds.npr.org/2105/rss.xml"),
    ("Earth Sciences", "https://feeds.npr.org/2106/rss.xml"),
    ("Life Sciences", "https://feeds.npr.org/2107/rss.xml"),
    ("Physics", "https://feeds.npr.org/2108/rss.xml"),
    ("Documentary", "https://feeds.npr.org/2109/rss.xml"),
    ("Relationships", "https://feeds.npr.org/2110/rss.xml"),
    ("Soccer", "https://feeds.npr.org/2111/rss.xml"),
    ("Football", "https://feeds.npr.org/2112/rss.xml"),
    ("Basketball", "https://feeds.npr.org/2113/rss.xml"),
    ("Baseball", "https://feeds.npr.org/2114/rss.xml"),
    ("Hockey", "https://feeds.npr.org/2115/rss.xml"),
    ("Running", "https://feeds.npr.org/2116/rss.xml"),
    ("Rugby", "https://feeds.npr.org/2117/rss.xml"),
    ("Golf", "https://feeds.npr.org/2118/rss.xml"),
    ("Cricket", "https://feeds.npr.org/2119/rss.xml"),
    ("Wrestling", "https://feeds.npr.org/2120/rss.xml"),
    ("Tennis", "https://feeds.npr.org/2121/rss.xml"),
    ("Volleyball", "https://feeds.npr.org/2122/rss.xml"),
    ("Swimming", "https://feeds.npr.org/2123/rss.xml"),
    ("Fantasy Sports", "https://feeds.npr.org/2124/rss.xml"),
    ("Fantasy", "https://feeds.npr.org/2125/rss.xml"),
    ("TV Reviews", "https://feeds.npr.org/2126/rss.xml"),
    ("After Shows", "https://feeds.npr.org/2127/rss.xml"),
    ("Film Reviews", "https://feeds.npr.org/2128/rss.xml"),
    ("Film History", "https://feeds.npr.org/2129/rss.xml"),
    ("Film Interviews", "https://feeds.npr.org/2130/rss.xml"),
    ("Entrepreneurship", "https://feeds.npr.org/2131/rss.xml"),
    ("Medicine", "https://feeds.npr.org/2132/rss.xml"),
    ("About 'All Things Considered'", "https://feeds.npr.org/5002/rss.xml"),
    ("About 'Morning Edition'", "https://feeds.npr.org/5003/rss.xml"),
    ("Performance Today", "https://feeds.npr.org/5004/rss.xml"),
    ("About 'Talk of the Nation'", "https://feeds.npr.org/5005/rss.xml"),
    ("About 'Weekend Edition Saturday'", "https://feeds.npr.org/5007/rss.xml"),
    ("About 'Weekend Edition Sunday'", "https://feeds.npr.org/5010/rss.xml"),
    ("About 'News & Notes'", "https://feeds.npr.org/5011/rss.xml"),
    ("About 'Fresh Air'", "https://feeds.npr.org/5013/rss.xml"),
    ("The Tavis Smiley Show", "https://feeds.npr.org/5014/rss.xml"),
    ("The Motley Fool", "https://feeds.npr.org/5015/rss.xml"),
    ("Special Coverage : Iraq", "https://feeds.npr.org/5016/rss.xml"),
    ("About 'Day to Day'", "https://feeds.npr.org/5017/rss.xml"),
    ("About 'JazzSet with Dee Dee Bridgewater'", "https://feeds.npr.org/5020/rss.xml"),
    ("About 'Marian McPartland's Piano Jazz'", "https://feeds.npr.org/5024/rss.xml"),
    ("Wait Wait...Don't Tell Me!", "https://feeds.npr.org/5035/rss.xml"),
    ("World of Opera", "https://feeds.npr.org/5036/rss.xml"),
    ("About 'All Songs Considered'", "https://feeds.npr.org/5037/rss.xml"),
    ("World Cafe", "https://feeds.npr.org/5039/rss.xml"),
    ("About 'Tell Me More'", "https://feeds.npr.org/5046/rss.xml"),
    ("The Bryant Park Project", "https://feeds.npr.org/5047/rss.xml"),
    ("About 'TED Radio Hour'", "https://feeds.npr.org/5057/rss.xml"),
    ("About 'Ask Me Another'", "https://feeds.npr.org/5058/rss.xml"),
    ("About 'Invisibilia'", "https://feeds.npr.org/5064/rss.xml")
]

abc_news_rss_feeds = [
    ("Money", "https://abcnews.go.com/abcnews/moneyheadlines/rss"),
    ("Headlines", "http://feeds.abcnews.com/abcnews/topstories/rss"),
    ("International Headlines", "http://feeds.abcnews.com/abcnews/internationalheadlines/rss"),
    ("United States", "https://abcnews.go.com/abcnews/usheadlines/rss"),
    ("Sports", "https://abcnews.go.com/abcnews/sportsheadlines/rss"),
    ("Entertainment", "http://feeds.abcnews.com/abcnews/entertainmentheadlines/rss"),
    ("Politics", "https://abcnews.go.com/abcnews/politicsheadlines/rss"),
    ("Technology", "http://feeds.abcnews.com/abcnews/technologyheadlines/rss"),
    ("Good Morning America", "https://abcnews.go.com/abcnews/gmaheadlines/rss"),
    ("Health", "https://abcnews.go.com/abcnews/healthheadlines/rss"),
    ("2020", "https://abcnews.go.com/abcnews/2020headlines/rss"),
    ("Nightline", "https://abcnews.go.com/abcnews/nightlineheadlines/rss")
]

spiegel_rss_feed = [
    ("Headlines", "https://www.spiegel.de/schlagzeilen/tops/index.rss"),
    ("Breaking News", "https://www.spiegel.de/schlagzeilen/eilmeldung/index.rss"),
    ("None", "https://www.spiegel.de/schlagzeilen/index.rss"),
    ("Videos", "https://www.spiegel.de/video/index.rss"),
    ("Politics", "https://www.spiegel.de/politik/index.rss"),
    ("German Politics", "https://www.spiegel.de/politik/deutschland/index.rss"),
    ("World Politics", "https://www.spiegel.de/politik/ausland/index.rss"),
    ("Politics & Business Videos", "https://www.spiegel.de/video/politik_wirtschaft/index.rss"),
    ("Economy", "https://www.spiegel.de/wirtschaft/index.rss"),
    ("Consumer & Services", "https://www.spiegel.de/wirtschaft/service/index.rss"),
    ("Comanies and Businesses", "https://www.spiegel.de/wirtschaft/unternehmen/index.rss"),
    ("Government and Social Affairs", "https://www.spiegel.de/wirtschaft/soziales/index.rss"),
    ("Panorama", "https://www.spiegel.de/panorama/index.rss"),
    ("Justice", "https://www.spiegel.de/panorama/justiz/index.rss"),
    ("Society", "https://www.spiegel.de/panorama/gesellschaft/index.rss"),
    ("Peolpe", "https://www.spiegel.de/panorama/haben/index.rss"),
    ("Panorama Videos", "https://www.spiegel.de/video/panorama/index.rss"),
    ("Sports", "https://www.spiegel.de/sport/index.rss"),
    ("Football", "https://www.spiegel.de/sport/fussball/index.rss"),
    ("Formula 1", "https://www.spiegel.de/sport/formel1/index.rss"),
    ("Videos From Sport", "https://www.spiegel.de/video/sport/index.rss"),
    ("Culture", "https://www.spiegel.de/kultur/index.rss"),
    ("Cinema", "https://www.spiegel.de/kultur/kino/index.rss"),
    ("Music", "https://www.spiegel.de/kultur/musik/index.rss"),
    ("TV", "https://www.spiegel.de/kultur/tv/index.rss"),
    ("Literature", "https://www.spiegel.de/kultur/literatur/index.rss"),
    ("Videos About Cinema", "https://www.spiegel.de/video/kino/index.rss"),
    ("Videos On Culture", "https://www.spiegel.de/video/kultur/index.rss"),
    ("The Netzwelt", "https://www.spiegel.de/netzwelt/index.rss"),
    ("Netzpolitik", "https://www.spiegel.de/netzwelt/netzpolitik/index.rss"),
    ("Web", "https://www.spiegel.de/netzwelt/web/index.rss"),
    ("Gadgets", "https://www.spiegel.de/netzwelt/gadgets/index.rss"),
    ("Games", "https://www.spiegel.de/netzwelt/games/index.rss"),
    ("Photo", "https://www.spiegel.de/thema/fotografie/index.rss"),
    ("Videos On Science And Technology", "https://www.spiegel.de/video/wissenschaft_technik/index.rss"),
    ("Science", "https://www.spiegel.de/wissenschaft/index.rss"),
    ("Human", "https://www.spiegel.de/wissenschaft/mensch/index.rss"),
    ("Nature", "https://www.spiegel.de/wissenschaft/natur/index.rss"),
    ("Technology", "https://www.spiegel.de/wissenschaft/technik/index.rss"),
    ("Space", "https://www.spiegel.de/wissenschaft/weltall/index.rss"),
    ("Medicine", "https://www.spiegel.de/wissenschaft/medizin/index.rss"),
    ("Videos On Science And Technology", "https://www.spiegel.de/video/wissenschaft_technik/index.rss"),
    ("Health", "https://www.spiegel.de/gesundheit/index.rss"),
    ("Diagnosis & Therapy", "https://www.spiegel.de/gesundheit/diagnose/index.rss"),
    ("Nutrition & Fitness", "https://www.spiegel.de/gesundheit/ernaehrung/index.rss"),
    ("Psychology", "https://www.spiegel.de/gesundheit/psychologie/index.rss"),
    ("Sex & Partnership", "https://www.spiegel.de/gesundheit/sex/index.rss"),
    ("Pregnancy & Child", "https://www.spiegel.de/gesundheit/schwangerschaft/index.rss"),
    ("The Travel Section", "https://www.spiegel.de/reise/index.rss"),
    ("City Trips", "https://www.spiegel.de/reise/staedte/index.rss"),
    ("Germany", "https://www.spiegel.de/reise/deutschland/index.rss"),
    ("Europe", "https://www.spiegel.de/reise/europa/index.rss"),
    ("Wanderlust", "https://www.spiegel.de/reise/fernweh/index.rss"),
    ("One Day - Contemporary Stories", "https://www.spiegel.de/einestages/index.rss"),
    ("The Mobility Department", "https://www.spiegel.de/auto/index.rss"),
    ("Driving Reports", "https://www.spiegel.de/auto/fahrberichte/index.rss"),
    ("Driving Culture", "https://www.spiegel.de/auto/fahrkultur/index.rss"),
    ("Current Videos", "https://www.spiegel.de/video/aktuell/index.rss"),
    ("Politics And Business", "https://www.spiegel.de/video/politik_wirtschaft/index.rss"),
    ("Panorama", "https://www.spiegel.de/video/panorama/index.rss"),
    ("Cinema", "https://www.spiegel.de/video/kino/index.rss"),
    ("Culture", "https://www.spiegel.de/video/kultur/index.rss"),
    ("Sport", "https://www.spiegel.de/video/sport/index.rss"),
    ("Science And Technology", "https://www.spiegel.de/video/wissenschaft_technik/index.rss"),
    ("TV Magazine", "https://www.spiegel.de/video/spiegelv/index.rss")
]

the_independent_rss_feeds = [
    ("UK", "https://www.independent.co.uk/news/uk/rss"),
    ("World", "https://www.independent.co.uk/news/world/rss"),
    ("Business", "https://www.independent.co.uk/news/business/rss"),
    ("People", "https://www.independent.co.uk/news/people/rss"),
    ("Science", "https://www.independent.co.uk/news/science/rss"),
    ("Media", "https://www.independent.co.uk/news/media/rss"),
    ("Education", "https://www.independent.co.uk/news/education/rss"),
    ("Obituaries", "https://www.independent.co.uk/news/obituaries/rss"),
    ("VOICES", "https://www.independent.co.uk/voices/?service=rss"),
    ("Editorials", "https://www.independent.co.uk/voices/editorials/?service=rss"),
    ("Comment", "https://www.independent.co.uk/voices/comment/?service=rss"),
    ("IV Drip", "https://www.independent.co.uk/voices/iv-drip/?service=rss"),
    ("Our Voices", "https://www.independent.co.uk/voices/our-voices/?service=rss"),
    ("Debate", "https://www.independent.co.uk/voices/debate/?service=rss"),
    ("Letters", "https://www.independent.co.uk/voices/debate/?service=rss"),
    ("ENVIRONMENT", "https://www.independent.co.uk/environment/rss"),
    ("Climate change", "https://www.independent.co.uk/environment/climate-change/rss"),
    ("Green Living", "https://www.independent.co.uk/environment/green-living/rss"),
    ("Nature", "https://www.independent.co.uk/environment/nature/rss"),
    ("SPORT", "https://www.independent.co.uk/sport/rss"),
    ("Athletics", "https://www.independent.co.uk/sport/general/athletics/rss"),
    ("Football", "https://www.independent.co.uk/sport/football/rss"),
    ("Golf", "https://www.independent.co.uk/sport/golf/rss"),
    ("Motor Racing", "https://www.independent.co.uk/sport/motor-racing/rss"),
    ("Racing", "https://www.independent.co.uk/sport/racing/rss"),
    ("Rugby Union", "https://www.independent.co.uk/sport/rugby/rugby-union/rss"),
    ("Others", "https://www.independent.co.uk/sport/general/others/rss"),
    ("LIFE & STYLE", "https://www.independent.co.uk/life-style/rss"),
    ("Fashion", "https://www.independent.co.uk/life-style/fashion/rss"),
    ("Food & Drink", "https://www.independent.co.uk/life-style/food-and-drink/rss"),
    ("Health & Families", "https://www.independent.co.uk/life-style/health-and-wellbeing/rss"),
    ("House & Home", "https://www.independent.co.uk/life-style/house-and-home/rss"),
    ("Gadgets & Tech", "https://www.independent.co.uk/life-style/gadgets-and-tech/rss"),
    ("Motoring", "https://www.independent.co.uk/life-style/motoring/rss"),
    ("Pets", "https://www.independent.co.uk/life-style/pets/rss"),
    ("Love & Sex", "https://www.independent.co.uk/life-style/love-sex/rss"),
    ("ARTS & ENTERTAINMENT", "https://www.independent.co.uk/arts-entertainment/rss"),
    ("Art", "https://www.independent.co.uk/arts-entertainment/art/rss"),
    ("Architecture", "https://www.independent.co.uk/arts-entertainment/architecture/rss"),
    ("Classical", "https://www.independent.co.uk/arts-entertainment/classical/rss"),
    ("Films", "https://www.independent.co.uk/arts-entertainment/films/rss"),
    ("TV & Radio", "https://www.independent.co.uk/arts-entertainment/tv/rss"),
    ("Theatre & Dance", "https://www.independent.co.uk/arts-entertainment/theatre-dance/rss"),
    ("Comedy", "https://www.independent.co.uk/arts-entertainment/comedy/rss"),
    ("Interviews", "https://www.independent.co.uk/arts-entertainment/interviews/rss"),
    ("TRAVEL", "https://www.independent.co.uk/travel/rss"),
    ("News", "https://www.independent.co.uk/travel/news-and-advice/rss"),
    ("48 Hours In", "https://www.independent.co.uk/travel/48-hours-in/rss"),
    ("Africa", "https://www.independent.co.uk/travel/africa/rss"),
    ("Americas", "https://www.independent.co.uk/travel/americas/rss"),
    ("Asia", "https://www.independent.co.uk/travel/asia/rss"),
    ("Australasia & Pacific", "https://www.independent.co.uk/travel/ausandpacific/rss"),
    ("Europe", "https://www.independent.co.uk/travel/europe/rss"),
    ("Middle East", "https://www.independent.co.uk/travel/middle-east/rss"),
    ("UK", "https://www.independent.co.uk/travel/uk/rss"),
    ("Skiing", "https://www.independent.co.uk/travel/skiing/rss"),
    ("Money", "https://www.independent.co.uk/money/rss"),
    ("Spend & Save", "https://www.independent.co.uk/money/spend-save/rss"),
    ("Loans & Credit", "https://www.independent.co.uk/money/loans-credit/rss"),
    ("Mortgages", "https://www.independent.co.uk/money/mortgages/rss"),
    ("Pensions", "https://www.independent.co.uk/money/pensions/rss"),
    ("Insurance", "https://www.independent.co.uk/money/insurance/rss"),
    ("Tax", "https://www.independent.co.uk/money/tax/rss")
]

# More feeds at https://blog.feedspot.com/world_news_rss_feeds/
# Imported until entry 24 The Independent (included)
feed_list_list = [
    ("One America News Network", oan_rss_feeds),
    ("Fox News", fox_rss_feeds),
    ("CNN", cnn_rss_feeds),
    ("Yahoo News", yahoo_rss_feeds),
    ("BuzzFeed", buzzfeed_rss_feeds),
    ("The Guardian", guardian_rss_feeds),
    ("Washington Post", washington_post_rss_feeds),
    ("CNBC", cnbc_rss_feeds),
    ("RT", rt_rss_feeds),
    ("NPR", npr_rss_feeds),
    ("ABC News", abc_news_rss_feeds),
    ("Der Spiegel", spiegel_rss_feed),
    ("The Independent", the_independent_rss_feeds)
]


def populateAllFeeds():
    count = 0
    count += populateVariousFeeds()
    for name, feed_list in feed_list_list:
        count += populateFeedList(name, feed_list)
    return count


def populateFeedList(name, rss_feeds):
    count = 0
    for section in rss_feeds:
        count += populateFeeds(
            name,
            section[1],
            section[0])
    return count


def populateNYTFeeds():
    count = 0
    for section in nyt_rss_feeds:
        count += populateFeeds(
            "New York Times",
            "https://rss.nytimes.com/services/xml/rss/nyt/%s.xml" % section,
            section)
    return count


def populateVariousFeeds():
    count = 0
    # for more reddit feeds:
    # https://www.reddit.com/r/rss/comments/gxsmq4/news_feeds/
    # https://feeder.co/knowledge-base/rss-feed-creation/reddit-rss/
    count += populateFeeds('Reddit', 'https://www.reddit.com/r/worldnews/.rss', 'World News')
    # TODO: add http://feeds.reuters.com/reuters/topnews when DNS error is gone
    # https://blog.feedspot.com/reuters_rss_feeds/
    count += populateFeeds('Thomson Reuters', 'https://ir.thomsonreuters.com/rss/news-releases.xml?items=100',
                           'Finance')
    count += populateFeeds('Al Jazeera', 'https://www.aljazeera.com/xml/rss/all.xml', 'Headlines')
    count += populateFeeds('Defense Blog', 'http://defence-blog.com/feed', "Defense")
    count += populateFeeds('E-International Relations', 'https://www.e-ir.info/feed/')
    count += populateFeeds('Global Issues', 'http://www.globalissues.org/news/feed')
    count += populateFeeds('The Cipher Brief', 'https://www.thecipherbrief.com/feed')
    count += populateFeeds('WorldNewsSuperFast',
                           'https://worldnewssuperfast.blogspot.com/feeds/posts/default?alt=rss')
    count += populateFeeds('Times of India', 'https://timesofindia.indiatimes.com/rssfeeds/296589292.cms')
    count += populateFeeds('NPR', 'https://feeds.npr.org/1004/rss.xml', 'World')
    count += populateFeeds('NPR', 'https://feeds.npr.org/510355/podcast.xml', 'Consider This')
    count += populateFeeds('NPR', 'https://feeds.npr.org/2/rss.xml', 'All Things Considered')
    count += populateFeeds('NPR', 'https://feeds.npr.org/3/rss.xml', 'Morning Edition')
    count += populateFeeds('NPR', 'https://feeds.npr.org/4/rss.xml', 'Performance Today')
    count += populateFeeds('NPR', 'https://feeds.npr.org/5/rss.xml', 'Talk of the Nation')
    count += populateFeeds('NPR', 'https://feeds.npr.org/7/rss.xml', 'Weekend Edition Saturday')
    count += populateFeeds('NPR', 'https://feeds.npr.org/10/rss.xml', 'Weekend Edition Sunday')
    count += populateFeeds('NPR', 'https://feeds.npr.org/11/rss.xml', 'News & Notes')
    count += populateFeeds('NPR', 'https://feeds.npr.org/13/rss.xml', 'Fresh Air')
    count += populateFeeds('NPR', 'https://feeds.npr.org/14/rss.xml', 'The Tavis Smiley Show')
    count += populateFeeds('NPR', 'https://feeds.npr.org/15/rss.xml', 'The Motley Fool')
    count += populateFeeds('NPR', 'https://feeds.npr.org/22/rss.xml', 'Latino USA')
    count += populateFeeds('Sputnik News', 'https://sputniknews.com/export/rss2/world/index.xml', 'Headlines')
    count += populateFeeds('', '', '')
    count += populateFeeds('', '', '')
    count += populateFeeds('', '', '')
    count += populateFeeds('', '', '')
    count += populateFeeds('', '', '')
    count += populateFeeds('', '', '')
    count += populateFeeds('', '', '')
    count += populateFeeds('', '', '')
    count += populateFeeds('', '', '')
    count += populateFeeds('', '', '')
    count += populateFeeds('', '', '')
    count += populateFeeds('', '', '')
    count += populateFeeds('', '', '')
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

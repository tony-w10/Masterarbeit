import asyncpraw

# Verbindung zur Reddit API herstellen (Erlaubt den Zugriff auf vordefinierte Reddit-Objekte und die Verabeitung derer)
def initialize_reddit():
    return asyncpraw.Reddit(
        client_id="YOUR DATA",
        client_secret="YOUR DATA",
        user_agent="YOUR DATA",
)


# Frägt die gewünschte Filterart für das entsprechende Subreddit ab
async def fetch_posts_by_type(subreddit, post_type, post_limit, time_filter = None):
    match post_type:
        case "top":
            return subreddit.top(time_filter=time_filter, limit = post_limit)
        case "new":
            return subreddit.new(limit = post_limit)
        case "rising":
            return subreddit.rising(limit = post_limit)
        case _:
            return subreddit.hot(limit = post_limit)    
        
        
# Ignoriert Beiträge von Moderatoren (diese sind oft automatisierte Statistiken oder Bilder) und Bots (generierte und wertfreie Beiträge)
def is_mod_or_bot(author):    
    if author is None:
        return True
    
    if hasattr(author, 'is_mod') and author.is_mod:
        return True
    
    if hasattr(author, 'name') and "bot" and "mod" in author.name.lower():
        return True
    return False
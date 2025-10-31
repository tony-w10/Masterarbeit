import nest_asyncio
import numpy as np
from reddit_functions import initialize_reddit
from reddit_functions import fetch_posts_by_type
from reddit_functions import is_mod_or_bot
from comment_and_replies import process_comments_and_replies
from sentiment_and_calculations import calculate_and_weight_output

nest_asyncio.apply()

# Programm Hauptfunktion zur Suche und Auswahl der entsprechenden Reddit Posts
async def main(subreddit_name, keywords, post_type, post_limit, time_filter, comment_limit, reply_limit):
    
    # API-Aufruf (Erläuterung in der Funktion selbst)
    reddit = initialize_reddit()
    subreddit = await reddit.subreddit(subreddit_name)

    # Initialisierung dreier Listen für die gewichteten Durchschnittswerte pro Post (Sentiment, Buy-Intent, Sell-Intent) und eines Postzählers
    all_average_weighted_sentiments = []
    all_average_weighted_buy_intents = []
    all_average_weighted_sell_intents = []
    
    post_counter = 0
    posts = await fetch_posts_by_type(subreddit, post_type, post_limit, time_filter)
    
    # Schleife für die Analysen und Berechnungen über die Posts
    async for post in posts:
        if any(keyword.lower() in post.title.lower() for keyword in keywords):
            await post.load()
            
            # Bereinigungsfunktion (Erläuterung in der Funktion selbst)
            if is_mod_or_bot(post.author):
                continue
            
            # Initialisierung der Liste für Posttitel, Kommentare und Replies für die Analysen
            reddit_inhalte = [f"Post: {post.title} | {post.score}"]
            post_counter += 1
            
            # Erweiterung der Liste mit den Kommentaren und Replies (Erläuterung in der Funktion selbst)
            reddit_inhalte += await process_comments_and_replies(post, comment_limit, reply_limit)

            # Berechne der gewichteten Durchschnittswerte nach der Sentimentanalyse (Erläuterung in der Funktion selbst)
            average_weighted_sentiment, average_weighted_buy_intent, average_weighted_sell_intent = calculate_and_weight_output(reddit_inhalte)
            
            # Speichern der drei gewichteten Durchschnittswerte für einen gesamten Post
            all_average_weighted_sentiments.append(average_weighted_sentiment)
            all_average_weighted_buy_intents.append(average_weighted_buy_intent)
            all_average_weighted_sell_intents.append(average_weighted_sell_intent)

    # Finale Durchschnittsberechnung über alle gefundene Posts für die drei Kennzahlen um drei Gesamtwerte zu erhalten
    # If-Prüfung zur Vermeidung einer Division durch 0 falls keine Posts gefunden wurden 
    if all_average_weighted_sentiments:
        final_sentiment = sum(all_average_weighted_sentiments) / len(all_average_weighted_sentiments) 
        final_average_weighted_buy_intent = sum(all_average_weighted_buy_intents) / len(all_average_weighted_buy_intents) 
        final_average_weighted_sell_intent = sum(all_average_weighted_sell_intents) / len(all_average_weighted_sell_intents) 

        # Finale Berechnung der gewichteten Buy-Sell-Ratio mithilfe des Laplace-Smoothings um eine Division durch 0 zu vermeiden falls kein Sell-Intentions gefunden wurden
        final_buy_sell_intention = np.log((final_average_weighted_buy_intent + 1) / (final_average_weighted_sell_intent + 1))     
        final_buy_sell_intention = np.clip(final_buy_sell_intention, -1, 1)
        
        return round(final_sentiment, 2), round(final_buy_sell_intention, 2), post_counter
    else: 
        return None, None, post_counter
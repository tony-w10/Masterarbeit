import asyncpraw
from reddit_functions import is_mod_or_bot
from general_functions import clean_text

# Funktion zur Erfassung der Kommentare und Replies der zu analysierenden Posts
async def process_comments_and_replies(post, comment_limit, reply_limit):
    
    reddit_inhalte = []
    await post.comments.replace_more(limit=0)
    
    # Comment Counter für den Abbruch sobald das Limit vom Frontend Eingabefeld erreicht wurde
    comment_counter = 0
    for comment in post.comments:
        if comment_counter >= comment_limit:
            break
        # Analog zu den Posts überprüfung auf Echtheit der Autoren (Erläuterung in der Funktion selbst)
        if isinstance(comment, asyncpraw.models.Comment) and not is_mod_or_bot(comment.author):
            cleaned_comment = clean_text(comment.body)
                   
            if cleaned_comment:
                # Kommentar zur Postliste hinzufügen für die entsprechenden Analysen (Reddit Score wird für die Gewichtung und Berechnung benötigt)
                reddit_inhalte.append(f"Comment: {cleaned_comment} | {comment.score}")
                comment_counter += 1
            
            # Reply Counter für den Abbruch sobald das Limit vom Frontend Eingabefeld erreicht wurde
            reply_counter = 0
            for reply in comment.replies:
                if reply_counter >= reply_limit:
                    break
                # Analog zu den Posts überprüfung auf Echtheit der Autoren (Erkäuterung in der Funktion selbst)
                if isinstance(reply, asyncpraw.models.Comment) and not is_mod_or_bot(reply.author):
                    cleaned_reply = clean_text(reply.body)
                    if cleaned_reply:
                        # Replies ebenfalls zur Postliste hinzufügen für die entsprechenden Analysen
                        reddit_inhalte.append(f"Reply: {cleaned_reply} | {reply.score}")
                        reply_counter += 1
                        
    return reddit_inhalte

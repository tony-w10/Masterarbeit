import openai

# Verbindung zur OpenAI-API herstellen um die Analysen mit Hilfe von GPT 4o durchzuführen
openai.api_key = 'YOUR DATA'

# Funktion für die Ermittlung der gewichteten Analysewerte
def calculate_and_weight_output(reddit_inhalte):
    
    # Initialisierung der gewichteten Gesamtkennzahlen für jeden Post
    total_weighted_sentiment = 0
    total_weighted_buy_intent = 0
    total_weighted_sell_intent = 0
    total_reddit_score = 0

    # Übergabe der Einträge in der Liste mit den Posts, Kommentaren und Replies und Abtrennung des Reddit Scores (Lediglich der Text wird analysiert - Reddit Score zur Berechnung)
    for eintrag in reddit_inhalte:
        
        parts = eintrag.split('|')
        text = parts[0].strip()
        reddit_score = int(parts[1].strip())
        
        # Funktionsaufruf zur Ermittlung der drei Kennzahlen pro Post, Kommentar und Reply
        sentiment_value, buy_intent, sell_intent = analyze_output(text)

        # Berechnung der gewichteten Werte von Post, Kommentar und Reply mit ihrem zugehörigen Reddit Score
        weighted_sentiment = round(sentiment_value * reddit_score, 2)
        weighted_buy_intent = buy_intent * reddit_score
        weighted_sell_intent = sell_intent * reddit_score

        # Aufsummieren aller gewichteten Posts, Kommentare und Replies
        total_weighted_sentiment += weighted_sentiment
        total_weighted_buy_intent += weighted_buy_intent
        total_weighted_sell_intent += weighted_sell_intent
        total_reddit_score += reddit_score
        
    # Berechnung der gewichteten Durchschnittswerte für jeden Post um drei Gesamtkennzahlen zu erhalten
    average_weighted_sentiment = round(total_weighted_sentiment / total_reddit_score, 2) 
    average_weighted_buy_intent = round(total_weighted_buy_intent / total_reddit_score, 2) 
    average_weighted_sell_intent = round(total_weighted_sell_intent / total_reddit_score, 2) 
    
    # Rückgabe der durchschnittlich gewichteten Kennzahlen pro Post
    return average_weighted_sentiment, average_weighted_buy_intent, average_weighted_sell_intent


# Funktion für die Analysen (Sentimentanalyse und Ermittlung der Buy bzw. Sell Intention) mit hilfe des antrainierten Modells auf Basis von GPT 4o
def analyze_output(text):
    response = openai.ChatCompletion.create(
        # Verwendung des antrainierten Modells (Prompt Übergabe an der Stelle trotz Training nötig da generative Tools "rückfällig" werden und ansonsten Text ausgeben)
        model="ft:gpt-4o-mini-2024-07-18:personal:final:AufSoNCz",
        messages=[
            {"role": "system", "content": "You are a model that analyzes finance-oriented Reddit posts, comments, and replies. Your task is to: 1. Analyze the sentiment of each text on a scale from -1 (very negative) to +1 (very positive). Consider context and potential sarcasm. 2. Determine if there is a current or future intent to buy or hold the stock mentioned in the post. Return 1 for buy/hold intent, otherwise 0. 3. Determine if there is a current or future intent to sell the stock. Return 1 for sell intent, otherwise 0. Always return the results as a single numeric string in the format: 'sentiment value | buy intent | sell intent'."},
            {"role": "user", "content": text}
        ],
        # Definition der Ausgabeparameter (Tokens als maximale Länge des Outputs und Temperatur für die Varianz des Outputs - beides niedrig für Konsistente numerische Ausgabe)
        max_tokens = 10,
        temperature = 0
    )
    
    model_output = response['choices'][0]['message']['content'].strip()
    values = values = [value.strip().replace("'", "").replace('"', "") for value in model_output.split('|')]
  
    sentiment_value = float(values[0])
    buy_intent = int(values[1])
    sell_intent = int(values[2])
    
    return sentiment_value, buy_intent, sell_intent

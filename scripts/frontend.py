import streamlit as st
import asyncio
from backend import main
from general_functions import create_bar_chart

st.title("Reddit Sentiment Analyse")
st.markdown("Zur Analyse von Aktientrends in finzorientierten Subreddits")

# Darstellung und Initialisierung der Eingabeparametern über Spalten per Streamlit
col1, col2 = st.columns([3, 1])
with col1:
    
    # Eingabeparameter für die populärsten Finanz Subreddits und entsprechende Keywords
    subreddit_name = ["wallstreetbets", "investing", "stocks", "cryptocurrency", "finance", "StockMarket"]
    selected_subreddit = st.selectbox("Subreddit:", options=subreddit_name, index=0)
    
    keywords = st.text_input("Keywords (Kommatrennung):", value="")
    keywords_list = [kw.strip() for kw in keywords.split(",") if kw.strip()]

with col2:
    # Eingabeparameter für die Filterart, Zeitfilter und zu analysierenden Posts
    post_type = st.selectbox(
        "Filterart:",
        ("hot", "new", "top", "rising")
        )

    time_filter = st.selectbox(
            "Zeitintervall",
            ("day", "week", "month", "year", "all"),
            disabled = (post_type != "top")
            )
    
post_limit = st.number_input(
    "Anzahl der zu analysierenden Posts (min. 10 - max. 100):", 
    min_value = 10, 
    max_value = 200, 
    value = 50,
    step = 10
    )

col_left, col_right = st.columns([1, 1])
with col_left:
    # Eingabeparameter für die Festlegung der zu analysiernden Kommentare und Replies
    comment_limit  = st.number_input(
        "Anzahl der zu analysierenden Kommentare pro Post:",
        min_value = 0,
        max_value = 5,
        value = 0,
        step = 1
        )

with col_right:
    reply_limit = st.number_input(
        "Anzahl der zu analysierenden Antworten pro Kommentar:",
        min_value = 0,
        max_value = 5,
        value = 1,
        step = 1,
        disabled = comment_limit == 0
        )

# Initialisierung der Ausgabeparameter
final_sentiment, final_buy_sell_intention, post_counter = None, None, None
error_message = ""

# Festlegung zweier Buttons 
col_left, col_right = st.columns([1.45, 6])
with col_left:
        if st.button("Analyse starten"):
            if not keywords_list:
                error_message = "Bitte geben Sie mindestens ein Keyword ein. Achten Sie bei mehreren Keywords auf die Kommatrennung."
            else:
                try:
                    final_sentiment, final_buy_sell_intention, post_counter = asyncio.run(main(selected_subreddit, keywords_list, post_type, post_limit, time_filter, comment_limit, reply_limit))
                    if post_counter == 0:
                        error_message = "Es wurden keine Posts mit den angegebenen Parametern gefunden - Bitte erweitern Sie die Suche"      
                except ValueError as ve:
                    error_message = str(ve)
                
# Reset Button               
with col_right:
        if st.button("Reset"):
            st.rerun()
  
# Workaround um Fehlermeldungen von oben in ganzer Breite darzustellen anstatt in jeweiliger Spaltenbreite
if error_message:
    st.error(error_message)

# Optische Ausgabeparameter der zwei zentralen Kennzahlen (Sentiment Score und Buy-Sell-Ratio) und dem Post Counter
if post_counter is not None and post_counter > 0:
    if final_sentiment is not None and final_buy_sell_intention is not None:
        
        col1, col2 = st.columns([3, 2])
        with col1: 
            
            # Grafiken für die beiden Kennzahlen (Erläuterung in der Funktion selbst)
            st.write("")
            st.write("Sentiment Score:")
            fig = create_bar_chart(final_sentiment, -1, -0.33, 0.33, 1)
            st.pyplot(fig)
            
            st.write("Buy-Sell-Intention:")
            fig2 = create_bar_chart(final_buy_sell_intention, -1, -0.33, 0.33, 1)
            st.pyplot(fig2)
   
        with col2:
            
            # Erläuterung der beiden Kennzahlen
            st.write(f"Auf Basis von **{post_counter}** gefundenen Posts:")
            st.markdown(f"""
                    **Sentiment Score:** Der Sentiment Score gibt Aufschluss über die Diskussionsstimmung im Subreddit **{selected_subreddit}** und liegt bei **{final_sentiment}**.<br><br>
                    **Buy-Sell-Intention:** Die Buy-Sell-Ratio spiegelt das Verhältnis der Kaufabsichten in Relation zu möglichen Verkäufen und liegt bei **{final_buy_sell_intention}**.<br>""", 
                    unsafe_allow_html=True)
       
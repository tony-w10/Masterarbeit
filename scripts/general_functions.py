import re
import matplotlib.pyplot as plt


# Funktion um die Beiträge von Bildern, Links, Links zu Bildern zu befreien und unnötige Sonder- und Leerzeichen zu entfernen
# Smileys werden erlaubt um die Analysen zu verbessern
def clean_text(text):
    if not text:
        return ""
    
    # Enfternt Bilder
    text = re.sub(r'\[img\]\(emote\|[^\)]+\)', '', text)
    text = re.sub(r'\[img\]\(https?:\/\/[^\)]+\)', '', text)
    
    # Entferne Gifs
    text = re.sub(r'https?:\/\/\S+\.gif(\?[^ ]*)?', '', text)
    text = re.sub(r'<[^>]*\.gif[^>]*>', '', text)
    text = re.sub(r'<a[^>]+href="https?:\/\/[^"]+\.gif[^"]*"[^>]*>.*?<\/a>', '', text)
    
    # Entfernt alle HTTPS-Tags
    text = re.sub(r'\[a\]\(https?:\/\/[^\)]+\)', '', text)
    text = re.sub(r'http[s]?://\S+', '', text)
    
    # Entfernt HTML-Tags und sonstige ungewollte Zeichen
    text = re.sub(r'<[^>]+>', '', text)
    
    # Entfernt Leerzeichen und Zeilenumbrüche
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'\*\*([^\*]+)\*\*', r'\1', text)  
    text = re.sub(r'\*([^\*]+)\*', r'\1', text) 

    if not text.strip():
        return None  
    return text


# Funktion für die Optische Ausgabe als Balkendiagramm
def create_bar_chart(value, lower_limit, threshold1, threshold2, upper_limit, title =None):
    # Erstellen eines neuen Balkens mit entsprechenden Formatparametern (Maße und Transparenz)
    fig, ax = plt.subplots(figsize=(5, 0.5)) 
    fig.patch.set_alpha(0)  
    ax.patch.set_alpha(0)   

    # Horizontale Gestaltung und Festlegung des Farbverlaufs
    bar_height = 0.2
    ax.barh([0], threshold1 - lower_limit, left=lower_limit, color='red', height=bar_height)
    ax.barh([0], threshold2 - threshold1, left=threshold1, color='yellow', height=bar_height)
    ax.barh([0], upper_limit - threshold2, left=threshold2, color='green', height=bar_height)

    # Vertikale Ausgestaltung
    ax.vlines(value, ymin=-bar_height/2 - 0.4, ymax=bar_height/2 + 0.4, color='black', linewidth=1.5)

    # Ausgestlatung und Positionierung des Indikators für den Ausgabewert
    ax.text(value, bar_height/2 + 0.6, f'{value}', color='black', va='bottom', ha='center', fontsize=10, fontweight='bold')

    # Positionierung des Ausgabewertes über dem Indikator
    ax.text(lower_limit, bar_height/2 + 0.15, f'{lower_limit}', color='black', va='bottom', ha='left', fontsize=9)
    ax.text(upper_limit, bar_height/2 + 0.15, f'{upper_limit}', color='black', va='bottom', ha='right', fontsize=9)

    # Offset Einstellungen zur Feinjustierung
    ax.set_xlim(lower_limit, upper_limit)
    ax.set_ylim(-0.5, 0.5)  
    ax.set_yticks([])
    ax.axis('off')
    plt.subplots_adjust(left=0)

    return fig





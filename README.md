# Masterarbeit: Entwicklung eines KI-Systems zur Analyse der Börsenstimmung innerhalb der Nachrichtenplattform Reddit
## Ziel der Arbeit ist die Entwicklung eines vollumfänglichen KI-Systems, welches die Börsenstimmung in finanzorientierten Subreddits automatisch erfasst und in aggregierter Form und anhand von zwei numerischen Kennzahlen ausgibt: 
- **Sentimentwert** 
- **Buy-Sell-Intention**

## Key Learnings / Highlights:
- Numerische Erfassung der Börsenstimmung durch individualisierte Sentimentanalyse und einer Buy-Sell-Intention mit OpenAI
- Aggregierte Daten schließen auf eine Korrelation zwischen Stimmung und Kursentwicklung

### Tools & Technologien:
- Python (Automatisierung und API-Abwicklung)
- FineTuning mit OpenAI (Individualisierung des LLMs)
- Microsoft Excel (Anschließender Korrelationstest mit der Kursentwicklung)

### Projektstruktur:
1. **Trainingsdaten** für den FineTuning Prozess generieren und formatieren 
2. **Beiträge durchsuchen** und an die Sentimentanalyse übergeben
3. **Numerische Verrechnung und Gewichtung** des Analyseoutputs im Backend
4. **Übermittlung an das Frontend** und Ausgabe der aggregierten Ergebnisse

### Hinweise:
- Alle Python-Skripte befinden sich im Ordner "scripts" und sind gemäß ihrer Funktionen gekennzeichnet
- Der Traininsdatensatz befindet sich im Ordner "data" und ist aus Gründen des Datenschutzes in anonymisierter und exemplarischer Form bereitgestellt
- API-Keys sind aus Sicherheitsgründen durch eigene zu ersetzen

### Weitere Hinweise:
Im System selbst wurden die Trainingsdaten mit der Standardversion von OpenAI *gpt-4o-mini* automatisch erfasst und beinhalten tatsächliche Reddit-Beiträge. Die Trainingsdaten wurden in einem vordefinierten Format als JSONL-Datei erfasst und unter festgelegten Entscheidungsregeln manuell angepasst, um die gewünschte Funktionsweise zu garantieren. Die zugehörigen Entscheidungsregeln für die Trainingsdaten sowie die konkrete Auswertung der Korrelation sind kein Bestandteil dieses Repositorys.

### Exemplarische Visualisierung der Benutzeroberfläche:
**Input:**

<img src="Tesla%20Input.jpg" alt="Frontend Pre-Analysis" width="50%">
</p>

**Output:**

<img src="Tesla%20Output.jpg" alt="Frontend Post-Analysis" width="50%">
</p>



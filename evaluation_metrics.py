fragen = [
    "Warum ist die Textilindustrie umweltschädlich?",
    "Warum ist Recycling von Textilien schwierig?",
    "Warum ist Textilabfall ein großes Problem?",
    "Wie viel Textilabfall entsteht weltweit?",
    "Warum ist häufiges Kaufen von Kleidung problematisch?",
    "Welche Umweltprobleme verursacht die Textilindustrie?"
]   
treffer = [1, 1, 1, 1, 1, 1]
precision_werte = [0.8, 0.8, 0.8, 0.6, 0.8, 0.8]
hit_rate = sum(treffer) / len(treffer)
precision_avg = sum(precision_werte) / len(precision_werte)
print("Hit Rate@5:", hit_rate)
print("Precision@5:", precision_avg)
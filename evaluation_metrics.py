fragen = [
    "Warum ist die Textilindustrie umweltschädlich?",
    "Warum ist Recycling von Textilien schwierig?",
    "Warum ist Textilabfall ein großes Problem?",
    "Wie viel Textilabfall entsteht weltweit?",
    "Warum ist häufiges Kaufen von Kleidung problematisch?",
    "Welche Umweltprobleme verursacht die Textilindustrie?"
]   

erfolg = [1, 1, 1, 1, 1, 1]


genauigkeit = [0.8, 0.8, 0.8, 0.6, 0.8, 0.8]

trefferquote = sum(erfolg)/len(erfolg)
durchschnitt_precision = sum(genauigkeit)/len(genauigkeit)
print("Hit Rate@5:", trefferquote)
print("Precision@5:", durchschnitt_precision)
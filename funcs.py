import numpy as np

def berechne_ebenen_normal(p1, p2, p3):

    # Berechne die Richtungsvektoren zwischen den Punkten
    v1 = np.array([p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]])
    v2 = np.array([p3[0] - p1[0], p3[1] - p1[1], p3[2] - p1[2]])
    print(v1,v2)

    # Berechne den Normalenvektor der Ebene durch das Kreuzprodukt
    normale = np.cross(v1, v2)
    normale /= np.linalg.norm(normale)  # Normalisieren des Normalenvektors
    print(normale)

    if normale.any() == 0:
        raise ValueError("Die drei Punkte sind kollinear und definieren keine gültige Ebene.")
    
    return normale



def korrigiere_orientierung(p, normale):

    # Extrahiere Rotationen des Punkts p (xr, yr)
    xr, yr, _ = p[3], p[4], p[5]  # zr wird ignoriert, da wir die Orientierung in der x-y-Ebene betrachten
    
    # Berechne den Normalenvektor des Punkts p basierend auf seinen Rotationen
    aktuelle_normale = np.array([
        np.cos(yr) * np.cos(xr),
        np.sin(xr) * np.cos(yr),
        np.sin(yr)
    ])
    
    # Überprüfen, ob die Orientierung von p mit der berechneten Normale übereinstimmt
    if not np.allclose(np.dot(aktuelle_normale, normale), 1, atol=1e-3):
        # Anpassung der Rotationen, um den Punkt korrekt auszurichten
        korrigierte_yr = np.arctan2(normale[2], np.sqrt(normale[0]**2 + normale[1]**2))
        korrigierte_xr = np.arctan2(normale[1], normale[0])
        
        return (korrigierte_xr, korrigierte_yr, 0)  # Setze zr auf 0, um die Ausrichtung in der x-y-Ebene sicherzustellen
    
    return (xr, yr, 0)  # Keine Korrektur nötig; zr bleibt auf 0



def hauptfunktion(p1, p2, p3):
    # Berechne den Normalenvektor der Ebene, die durch p1, p2 und p3 definiert wird
    normale = berechne_ebenen_normal(p1, p2, p3)
    
    # Überprüfe und korrigiere die Orientierung von p1
    korrigierte_orientierung = korrigiere_orientierung(p1, normale)
    
    # Ausgabe der Normalenvektoren und der korrigierten Orientierung von p1
    return {
        'normale': normale,
        'korrigierte_orientierung': korrigierte_orientierung
    }

# Beispielpunkte
p1 = (1.0, 2.0, 10.0, 0.1, 0.2, 0.0)  # Position und Rotation (xr, yr, zr)
p2 = (4.0, 5.0, 6.0, 0.0, 0.0, 0.0)
p3 = (7.0, 8.0, 9.0, 0.0, 0.0, 0.0)

ergebnis = hauptfunktion(p1, p2, p3)
print("Normalenvektor der Ebene:", ergebnis['normale'])
print("Korrigierte Orientierung von p1:", ergebnis['korrigierte_orientierung'])

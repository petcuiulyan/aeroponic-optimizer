def calculeaza_materiale(total_turnuri, L, W, H):
    """
    Estimare simplă structură metalică
    """

    nr_arce = int(L / 2)
    lungime_arc = W * 1.2

    teava_totala = nr_arce * lungime_arc

    return {
        "Arce metalice": nr_arce,
        "Lungime țeavă (m)": round(teava_totala, 2),
        "Turnuri": total_turnuri
    }

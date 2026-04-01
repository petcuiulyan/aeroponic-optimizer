import streamlit as st
import distributie_turnuri as dist
import automatizare as auto

# ... (partea de Layout rămâne neschimbată) ...

if pagina == "🤖 Sistem Automatizare (Control)":
    st.header("🤖 Control Automatizat cu Interval (Range)")
    
    sistem = auto.AutomatizareSera()

    # 1. SETĂRI INTERVALE (Input-uri pentru utilizator)
    col_set1, col_set2 = st.columns(2)
    with col_set1:
        st.subheader("Target pH")
        ph_range = st.slider("Interval pH Optim", 4.0, 9.0, (5.9, 6.5))
        sistem.ph_min, sistem.ph_max = ph_range
    with col_set2:
        st.subheader("Target EC")
        ec_range = st.slider("Interval EC Optim (ms/cm)", 0.5, 3.0, (1.1, 1.6))
        sistem.ec_min, sistem.ec_max = ec_range

    st.divider()

    # 2. CITIRI SENZORI (Simulare Gravity DFRobot)
    c1, c2, c3 = st.columns(3)
    with c1:
        ph_input = st.number_input("Senzor pH", value=6.8, step=0.1)
    with c2:
        ec_input = st.number_input("Senzor EC", value=1.0, step=0.1)
    with c3:
        st.metric("Nivel IBC 2", "65%", delta="OK")

    # 3. PROCESARE AUTOMATĂ
    decizii = sistem.proceseaza_dozare_automata(ph_input, ec_input)

    # 4. AFIȘARE STATUS ECHIPAMENTE (MARTORI VIRTUALI)
    st.subheader("⚡ Monitorizare Actuatori (Relee + MOSFET)")
    cols = st.columns(5)
    
    # Afișăm statusul pompelor tale specifice
    for i, (nume, stare) in enumerate(sistem.status.items()):
        color = "green" if stare else "gray"
        label = "🟢 PORNIT" if stare else "⚪ OPRIT"
        cols[i].markdown(f"**{nume}**")
        cols[i].markdown(f"<p style='color:{color}; font-weight:bold;'>{label}</p>", unsafe_allow_label=True)

    st.divider()
    
    # Jurnal de bord
    st.subheader("📋 Jurnal Sistem")
    for d in decizii:
        if "✅" in d:
            st.success(d)
        else:
            st.warning(d)

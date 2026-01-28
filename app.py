import pandas as pd
import scipy.stats
import streamlit as st
import time

# =========================
# Estado de la sesión
# =========================
if 'experiment_no' not in st.session_state:
    st.session_state.experiment_no = 0

if 'df_experiment_results' not in st.session_state:
    st.session_state.df_experiment_results = pd.DataFrame(
        columns=['no', 'iteraciones', 'media']
    )

# =========================
# UI
# =========================
st.header('🪙 Lanzar una moneda')

number_of_trials = st.slider(
    '¿Número de intentos?',
    min_value=1,
    max_value=1000,
    value=10
)

start_button = st.button('Ejecutar')

chart = st.line_chart([0.5])

# =========================
# Lógica
# =========================
def toss_coin(n: int) -> float:
    """Simula n lanzamientos de una moneda y grafica la media acumulada."""
    outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)

    heads_count = 0

    for i, result in enumerate(outcomes, start=1):
        if result == 1:
            heads_count += 1

        mean = heads_count / i
        chart.add_rows([mean])
        time.sleep(0.05)

    return mean

# =========================
# Ejecución
# =========================
if start_button:
    st.write(f'Experimento con **{number_of_trials}** intentos en curso…')

    st.session_state.experiment_no += 1
    mean = toss_coin(number_of_trials)

    new_row = pd.DataFrame(
        [[st.session_state.experiment_no, number_of_trials, mean]],
        columns=['no', 'iteraciones', 'media']
    )

    st.session_state.df_experiment_results = pd.concat(
        [st.session_state.df_experiment_results, new_row],
        ignore_index=True
    )

# =========================
# Resultados
# =========================
st.subheader('📊 Resultados acumulados')
st.write(st.session_state.df_experiment_results)

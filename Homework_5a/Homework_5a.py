import numpy as np
import plotly.graph_objs as go
import streamlit as st
from plotly.subplots import make_subplots


# Function to simulate one generation
def simulate_generation(pop, fAfA, fAfa, fafa, wAA, wAa, waa):

    # Calculate the weighted frequencies for selection
    weighted_freqs = [fAfA * wAA, fAfa * wAa, fafa * waa]
    weighted_freqs /= np.sum(weighted_freqs)
    
    # Simulate the next generation's allele frequencies
    offspring = np.random.choice(['AA', 'Aa', 'aa'], size=pop, p=weighted_freqs)
    fAfA = np.sum(offspring == 'AA') / pop
    fAfa = np.sum(offspring == 'Aa') / pop
    fafa = np.sum(offspring == 'aa') / pop

    # Translate into allele frequencies for A and a
    pA = fAfA + (0.5 * fAfa)
    pa = fafa + (0.5 * fAfa)

    return pA, pa, fAfA, fAfa, fafa


# Main simulation function
def simulate_allele_frequencies(initA, inita, wAA, wAa, waa, pop, gen, sim):
    all_frequencies = []
    final_frequencies = []

    # Runs desired num of simulations
    for _ in range(sim):
        pA = initA
        pa = inita

        fAfA = initA ** 2
        fAfa = 2 * (initA * inita)
        fafa = inita ** 2
        freq = []

        # Runs gen num of generations for each simulation
        for _ in range(gen):
            pA, pa, fAfA, fAfa, fafa = simulate_generation(pop, fAfA, fAfa, fafa, wAA, wAa, waa)
            fAfA = pA ** 2
            fAfa = 2 * (pA * pa)
            fafa = pa ** 2
            
            # Tracks for Allele A - (Can change for Allele a if desired)
            freq.append(pA)
        
        all_frequencies.append(freq)
        final_frequencies.append(freq[-1])
    
    return all_frequencies, final_frequencies


# Plotting functions using plotly.graph_objs
def plot_allele_frequencies(all_frequencies, gen):
    layout = go.Layout(
        title="Allele Frequencies Over Generations",
        xaxis=dict(
            title="Generation",
            range=[0, gen]
        ),
        yaxis=dict(
            title="Frequency of Allele A",
            range=[0,1]
        ),
        showlegend=True
    )

    fig = go.Figure(layout=layout)

    # Show each simulation with a line
    for frequencies in all_frequencies:
        fig.add_trace(go.Scatter(x=list(range(gen)), y=frequencies, mode='lines', line=dict(width=1), opacity=0.8))
    return fig


def plot_final_frequencies_histogram(final_frequencies):
    layout = go.Layout(
        title="Distribution of Final Allele Frequencies",
        xaxis=dict(
            title="Final Frequency of Allele A",
            range=[0,1]
        ),
        yaxis=dict(
            title="Count"
        )
    )

    # Show histogram of Final Allele Frequencies
    fig = go.Figure(data=[go.Histogram(x=final_frequencies, nbinsx=20, marker=dict(color='blue'), opacity=0.75)], layout=layout)
    return fig


def main():
    with st.sidebar:
        st.sidebar.header("Simulation Parameters")
        sim = st.slider('Number of Simulations:',min_value=1,max_value=100,step=1,value=1)
        pop = st.select_slider('Population Size:',[10,50,100,500,1000],value=100)
        gen = st.slider("Number of Generations:",min_value=50,max_value=500,step=50,value=100)
        initA = st.slider("Starting frequency of A:", min_value=0.01,max_value=0.99,step=0.01, value=0.5)
        wAA = st.slider('Fitness of AA:',min_value=0.,max_value=1.,step=0.05,value=1.)
        wAa = st.slider('Fitness of Aa:',min_value=0.,max_value=1.,step=0.05,value=1.)
        waa = st.slider('Fitness of aa:',min_value=0.,max_value=1.,step=0.05,value=1.)


    all_frequencies, final_frequencies = simulate_allele_frequencies(initA, 1 - initA, wAA, wAa, waa, pop, gen, sim)
    fig1 = plot_allele_frequencies(all_frequencies, gen)
    fig1['layout'].update(height=450, width=600)
    fig1['layout'].update(showlegend=False)

    fig2 = plot_final_frequencies_histogram(final_frequencies)
    fig2['layout'].update(height=450, width=600)
    fig2['layout'].update(showlegend=False)

    st.header("Allele Frequencies Over Generations")
    st.plotly_chart(fig1)
    
    st.header("Distribution of Final Allele Frequencies")
    st.plotly_chart(fig2)


if __name__ == "__main__":
    main()
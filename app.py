import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import base64
import os

# Load the dataset
df = pd.read_csv("Violin_Piano_Scaled_Color_Chart.csv")

# Audio playback
def get_audio_html(note):
    filename = f"sounds/{note.replace('#', 's')}.wav"
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            audio_bytes = f.read()
        b64 = base64.b64encode(audio_bytes).decode()
        return f'<audio controls src="data:audio/wav;base64,{b64}"></audio>'
    else:
        return "<i>No audio available</i>"

st.title("Interactive Violin Fingerboard - Piano-Based Color Scale")

# Create visual grid of violin notes
fig = go.Figure()
strings = ['G', 'D', 'A', 'E']  # Top to bottom
positions = list(range(0, 13))

for _, row in df.iterrows():
    y = strings.index(row['String'])
    x = row['Position']
    color = row['Hex Color'] if pd.notnull(row['Hex Color']) else '#888888'
    fig.add_shape(type="rect",
                  x0=x, x1=x+1,
                  y0=y, y1=y+1,
                  line=dict(color="black"),
                  fillcolor=color)
    fig.add_annotation(x=x+0.5, y=y+0.5, text=row['Note'],
                       showarrow=False, font=dict(color="black", size=10))

fig.update_yaxes(showticklabels=True, tickvals=[0.5,1.5,2.5,3.5], ticktext=strings[::-1])
fig.update_xaxes(title="Position", range=[0, 13], showgrid=False)
fig.update_layout(
    yaxis=dict(scaleanchor="x", title="String"),
    height=400,
    margin=dict(l=0, r=0, t=40, b=0),
    showlegend=False,
    plot_bgcolor="white",
    title="Violin Fingerboard (Piano-Scaled Color Mapping)"
)

st.plotly_chart(fig, use_container_width=True)

selected_note = st.selectbox("Select a note to hear:", df['Note'].unique())
st.markdown(get_audio_html(selected_note), unsafe_allow_html=True)

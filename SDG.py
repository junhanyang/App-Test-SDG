import streamlit as st
import pandas as pd
import altair as alt
from textwrap import wrap


st.header('SDG Test')

path = 'Portfolio SDG.csv'
data = pd.read_csv(path)

portfolios = ['Asia Tech',' Australian Financials',' Australian REITs','Cloud Computing',
'Cyber Security','Dogs of the Dow','Electric Vehicle','Hong Kong Consumer','Hong Hong Technology',
'Mainland Europe Financials','Mainland Europe Healthcare','Mainland Europe Technology','Metaverse',
'Resuregent Industrials','Singapore Cash is King','Singapore Stable REITs','Stable Aussie Giants',
'Stable Singpore Giants','Stable US Consumer Giants','Stable US Giants','Stable Healthcare Giants',
'Stable US Industrial Giants','UK Financials','US Financials','US Tech Leaders','Yummy']
SDG = ['SDG 01 - No Poverty','SDG 02 - Zero Hunger','SDG 03 - Good Health and Well-being',
'SDG 04 - Quality Education','SDG 05 - Gender Equality','SDG 06 - Clean Water and Sanitation',
'SDG 07 - Affordable and Clean Energy','SDG 08 - Decent Work and Economic Growth',
'SDG 09 - Industry, Innovation and Infrastructure','SDG 10 - Reduced Inequalities',
'SDG 11 - Sustainable Cities and Communities','SDG 12 - Responsible Consumption and Production',
'SDG 13 - Climate Action', 'SDG 14 - Life Below Water', 'SDG 15 - Life on Land', 
'SDG 16 - Peace, Justice and Strong Insttitutions', 'SDG 17 - Partnerships for the Goals']


choices = {'Portfolio':'', 'SDG Chosen': ''}

Portfolios = st.multiselect('Please choose the portoflio you are interested in',portfolios)
SDG_Chosen = st.multiselect('Please choose the SDG you are interested in',SDG)

#st.write(Portfolios)

df_port = data[data['Portfolio'].isin(Portfolios)]

alt.renderers.enable('mimetype')

sdg_perc = pd.DataFrame(columns=['SDG','Percentage','Alignment'])
for sdg in SDG_Chosen:
    cur_col = df_port[f'SDG_{sdg[4:6]}_NET_ALIGNMENT']
    dt_sdg = cur_col.value_counts()/len(cur_col.dropna())
    for ind in dt_sdg.index:
        sdg_perc = sdg_perc.append(pd.DataFrame({'SDG':sdg,'Percentage':dt_sdg[ind],'Alignment':ind},index=[0]))

#st.write(sdg_perc)

bar = alt.Chart(sdg_perc).mark_bar().encode(
    x=alt.X('SDG', axis=alt.Axis(labelAngle=30,labelLimit=400,labelFontSize=12)),
    y=alt.Y('Percentage',
    stack='normalize',
    axis=alt.Axis(format='%',title='Percentage')),
    color=alt.Color('Alignment', scale=alt.Scale(
        domain=['Aligned','Misaligned','Neutral'], 
        range=['Green','Red','Orange']))).properties(
        width=200*len(SDG_Chosen),
        height=500)

text = bar.mark_text(
    align='center',
    baseline='top',
    fill='white',
    fontSize=15
).encode(
    x='SDG',
    y=alt.Y('Percentage',
    stack='normalize'),
    text=alt.Text('Percentage', format='.1%')
)

bar+text




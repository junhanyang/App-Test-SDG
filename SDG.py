import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image


st.header('Personal Impact Dashboard')

path = 'Full_SDG.csv'
data = pd.read_csv(path)
#st.write(data)

portfolios = ['Aggressive',
 'All Weather',
 'Balanced',
 'Cautious',
 'China Growth',
 'Defensive',
 'Future World',
 'Gen Z Winners',
 'Growth',
 'Impact Investing',
 'Cyber Security',
 'Asia Tech',
 'Metaverse',
 'US Tech Leaders',
 'Dogs of the Dow',
 'UK Financials',
 'Stable US Giants',
 'Australian REITs',
 'Hong Kong Technology',
 'Singapore Cash is King',
 'Hong Kong Consumer',
 'Mainland Europe Technology',
 'Australian Financials',
 'Electric Vehicle',
 'Mainland Europe Healthcare',
 'Resurgent Industrials',
 'Yummy',
 'Mainland Europe Financials',
 'Stable Aussie Giants',
 'Stable Singapore Giants',
 'Stable US Healthcare Giants',
 'Stable US Industrial Giants',
 'Singapore Stable REITs',
 'US Financials',
 'Stable US Consumer Giants',
 'Cloud Computing']
SDG = ['SDG 01 - No Poverty','SDG 02 - Zero Hunger','SDG 03 - Good Health and Well-being',
'SDG 04 - Quality Education','SDG 05 - Gender Equality','SDG 06 - Clean Water and Sanitation',
'SDG 07 - Affordable and Clean Energy','SDG 08 - Decent Work and Economic Growth',
'SDG 09 - Industry, Innovation and Infrastructure','SDG 10 - Reduced Inequalities',
'SDG 11 - Sustainable Cities and Communities','SDG 12 - Responsible Consumption and Production',
'SDG 13 - Climate Action', 'SDG 14 - Life Below Water', 'SDG 15 - Life on Land', 
'SDG 16 - Peace, Justice and Strong Insttitutions', 'SDG 17 - Partnerships for the Goals']
images = [f'/Users/junhanyang/Desktop/SDG Icons/SDG0{x}.png' for x in range(1,10)]
images.extend([f'/Users/junhanyang/Desktop/SDG Icons/SDG{x}.png' for x in range(10,18)])
images=dict(zip(SDG,images))


Portfolios = st.multiselect('Please choose the portoflio you are interested in:',portfolios)
SDG_Chosen = st.multiselect('Please choose the SDG Values you believe in:',SDG)

amt_filled = False
if len(Portfolios)>0 and len(SDG_Chosen)>0:
    #collect info on amounts
    st.write('Amount Invested in Each Portfolio:')
    cols = st.columns(max(1,len(Portfolios)))
    values = {}
    for (i,p) in enumerate(Portfolios):
        #style ='<p style="font-family:Courier; color:Blue; font-size: 20px;">Degree of Alignment of Your Overall Investment</p>'
        values[p]=cols[i].number_input(p)
    total_amt = sum(list(values.values()))
    if total_amt > 0:
        amt_filled = True

#collect info on priorities
if amt_filled:
    st.write('Please check the box if an SDG value is super important to you')
    cols = st.columns(max(1,len(SDG_Chosen)))
    priorities = {}
    for (i,p) in enumerate(SDG_Chosen):
        priorities[p] = 2 if cols[i].checkbox(p) else 1
    total_points = sum(list(priorities.values()))

    #filter out non-related data
    df_port = data[data['Portfolio'].isin(Portfolios)]

    #consolidate info
    sdg_perc = pd.DataFrame(columns=['SDG','Aligned'])
    for sdg in SDG_Chosen:
        cur_amount_aligned = 0
        cur_col = df_port[['Portfolio','WEIGHT',f'FUND_SDG{sdg[4:6]}_ACHIEVE_SIGNAL']][df_port[f'FUND_SDG{sdg[4:6]}_ACHIEVE_SIGNAL']=='Aligned']
        dt_sdg = cur_col.groupby('Portfolio').sum('WEIGHT')['WEIGHT']
        #st.write(dt_sdg)
        for ind in dt_sdg.index:
            cur_amount_aligned += dt_sdg[ind]*values[ind]
        #st.write(cur_amount_aligned)
        sdg_perc=sdg_perc.append(pd.DataFrame({'SDG':sdg,'Aligned':cur_amount_aligned/total_amt if total_amt > 0 else 0},index=[0]))


    #Title of Rating Chart
    st.write('')
    st.write('')
    st.write('')
    title = '<p style="font-family:Times New Roman; color:Black; font-size: 20px; text-align:center">Degree of Alignment against Your Impact Values</p>'
    st.markdown(title, unsafe_allow_html=True)

    #Showing Degree of Alignment and Giving final rating
    weighted_perc = 0
    for row in sdg_perc.iterrows():
        cols = st.columns(16)
        cur_row = row[1]
        cols[4].image(Image.open(images[cur_row['SDG']]).resize((300,300)),width=45,use_column_width='never')
        n_square = int(cur_row['Aligned']*100//20)
        #cols[1].image(Image.open(f'/Users/junhanyang/Desktop/Star Ratings/{n_square}.png').resize((300,200)),width=100)
        for i in range(n_square):
            cols[6+i].markdown('🟢')
        for i in range(n_square,5):
            cols[6+i].markdown('⚪️')

        weighted_perc += priorities[cur_row['SDG']]*cur_row['Aligned']
        
    weighted_perc /= total_points


    #Title of Rating Chart
    st.write('')
    st.write('')
    st.write('')
    #col2 = st.columns(3)[1]
    title = '<p style="font-family:Times New Roman; color:Black; font-size: 20px; text-align:center">My Personal Impact Alignment</p>'
    st.markdown(title, unsafe_allow_html=True)

    col = st.columns(3)[1]
    if weighted_perc > 2/3:
        col.image(Image.open('/Users/junhanyang/Desktop/Ratings/a.png'),use_column_width = True)
    elif weighted_perc > 1/3:
        col.image(Image.open('/Users/junhanyang/Desktop/Ratings/b.png'),use_column_width = True)
    else:
        col.image(Image.open('/Users/junhanyang/Desktop/Ratings/c.png'),use_column_width = True)

    st.write('')
    st.write('')
    st.write('')
    #col = st.columns(3)[1]
    st.write(sdg_perc)
    st.write(f'Priority-Weighted Percentage of Alignment: {"{:.2%}".format(weighted_perc)}')






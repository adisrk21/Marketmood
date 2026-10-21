import os, streamlit as st, plotly.graph_objects as go
from database.repository import read_all
from services.updater import update
st.set_page_config(page_title='India Market Mood',page_icon='📈',layout='wide')
st.title('🇮🇳 India Market Mood')
st.caption('Nifty 500 breadth, momentum and market-regime dashboard')
with st.sidebar:
    st.header('Controls')
    if st.button('Refresh market data',use_container_width=True):
        with st.spinner('Downloading Nifty 500 data...'): update(False,False)
        st.rerun()

df=read_all()
if df.empty:
    st.warning('Database is empty. Click Refresh market data, or run python scripts/backfill.py once.')
    st.stop()
r=df.iloc[-1]
cols=st.columns(3)
for col,label,val in [(cols[0],'Market Mood',r.mood_score),(cols[1],'Short-Term',r.short_score),(cols[2],'Long-Term',r.long_score)]:
    fig=go.Figure(go.Indicator(mode='gauge+number',value=val,title={'text':label},gauge={'axis':{'range':[0,100]},'steps':[{'range':[0,35]},{'range':[35,55]},{'range':[55,100]}],'threshold':{'line':{'width':4},'value':val}}))
    fig.update_layout(height=260,margin=dict(l=20,r=20,t=50,b=20)); col.plotly_chart(fig,use_container_width=True)
st.subheader(f"Regime: {r.regime} · Last market date: {r.date.date()}")
a,b,c,d=st.columns(4)
a.metric('Above 21 DMA',f'{r.pct_above_21:.1f}%'); b.metric('Above 50 DMA',f'{r.pct_above_50:.1f}%'); c.metric('Above 200 DMA',f'{r.pct_above_200:.1f}%'); d.metric('A/D ratio',f'{r.ad_ratio:.2f}')
st.subheader('Trend breadth')
st.line_chart(df.set_index('date')[['pct_above_21','pct_above_50','pct_above_200']],height=380)
c1,c2=st.columns(2)
with c1:
    st.subheader('52-week highs vs lows'); st.line_chart(df.set_index('date')[['high52','low52']],height=300)
with c2:
    st.subheader('RSI breadth'); st.line_chart(df.set_index('date')[['rsi_overbought','rsi_oversold']],height=300)
st.subheader('Market breadth')
show=df[['date','advancers','decliners','ad_ratio','up3','down3','up5','down5','up10','down10','up20','down20']].tail(30).sort_values('date',ascending=False)
st.dataframe(show,use_container_width=True,hide_index=True)
st.subheader('Historical Market Mood')
st.line_chart(df.set_index('date')[['mood_score','short_score','long_score']],height=350)
st.caption('Breadth analytics are informational and are not investment advice. Data availability can vary by source.')

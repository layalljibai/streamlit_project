import pandas as pd
import streamlit as st
import plotly.offline as py
import plotly.figure_factory as ff
import plotly.graph_objects as go
import altair as alt
import seaborn as sns

@st.cache
def load_data(n):
    data = pd.read_csv("country_vaccinations.csv",nrows=n)
    return data

df = load_data(43342)

df_grouped_by_vaccine = df.groupby(["country",'vaccines'])['total_vaccinations',
                         'people_vaccinated','people_fully_vaccinated',
                        'daily_vaccinations','total_vaccinations_per_hundred',
                        'people_vaccinated_per_hundred',"people_fully_vaccinated_per_hundred"
    ,'daily_vaccinations_per_million'].max().reset_index()
st.title('Data visualization using streamlit')
st.header('Country vaccination dataset')
if st.checkbox('show first ten rows'):
    st.subheader('country_vaccinations data')
    st.write(load_data(10))
st.header('visualizations')
if st.checkbox('Let us explore People vaccinated vs people fully vaccinated by country'):

    c = alt.Chart(df_grouped_by_vaccine).mark_circle().encode( x='people_vaccinated', y='people_fully_vaccinated', size='total_vaccinations', color='total_vaccinations', tooltip=['country'])
    st.write(c)



if st.checkbox('Let us explore the Number of total vaccinations for the first 20 most vaccinated countries  '):

  st.set_option('deprecation.showPyplotGlobalUse', False)
  sns.barplot(x="total_vaccinations", y="country", hue=None, data=df_grouped_by_vaccine[['country','total_vaccinations']].nlargest(20,'total_vaccinations'))
  st.pyplot()

if st.checkbox('Let us explore the total vaccinations by country'):
  fig = go.Figure()
  fig.add_trace(go.Scatter(x=df.country, y=df.total_vaccinations, mode = 'lines+markers'))
  fig.update_layout(

    xaxis_title="Country",
    yaxis_title="Total vaccinations",
    font=dict(
        family="Arial, monospace",
        size=12,
        color="black"
    )
  )
  st.plotly_chart(fig,use_container_width=True)

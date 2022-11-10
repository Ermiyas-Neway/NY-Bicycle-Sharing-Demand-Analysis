import streamlit as st
import pandas as pd
import plotly.express as px
import base64

st.set_page_config (
    page_title="Bike Sharing Demand Analysis Dashboard",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded",)

def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://www.dcnewsnow.com/wp-content/uploads/sites/14/2021/03/4d650de0c16b4cc882a34afa5b816aca.jpg");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_url() 
@st.cache(allow_output_mutation=True, suppress_st_warning=True)

def read_and_preprocess():
    data = pd.read_csv("bike-sharing_hourly.csv")

    # Creating Day variable and changind data type of the date column
    data['dteday'] = data['dteday'].astype('datetime64[ns]')
    data["day"] = data.dteday.dt.day

    #creating date formatted column for comparision with input date
    data['dateFormated'] = data.dteday.dt.date
    data['timeFormated'] = data.dteday.dt.time

    def peakHours(timeOf):
        if (((timeOf >= 23) | ((timeOf >= 1) & (timeOf <= 4) )) | ((timeOf >= 10) & (timeOf <= 14))):
            return "Peak Hour"
        else:
            return "Non-Peak Hour"

    data['peakHour'] = data['hr'].apply(lambda x:peakHours(x))
    return data
data = read_and_preprocess()
st.session_state['data'] = data

def plot_charts(data):
     col1, col2, col3 = st.columns(3) 
     with col1:
         fig1 = px.bar(data.groupby('season', as_index=False)['cnt'].mean(), x='season', y='cnt')
         fig1.update_xaxes(title="Seasons")
         fig1.update_yaxes(title="Average Demand of Bikes")
         st.plotly_chart(fig1, use_container_width=True) 
     with col2:
         fig2 = px.bar(data.groupby('yr', as_index=False)['cnt'].mean(), x='yr', y='cnt')
         fig2.update_xaxes(title="Year")
         fig2.update_yaxes(title="Average Demand of Bikes")
         st.plotly_chart(fig2, use_container_width=True)
     with col3:
         fig3 = px.bar(data.groupby('mnth', as_index=False)['cnt'].mean(), x='mnth', y='cnt')
         fig3.update_xaxes(title="Month")
         fig3.update_yaxes(title="Average Demand of Bikes")
         st.plotly_chart(fig3, use_container_width=True)    
     col4, col5, col6 = st.columns(3)
     with col4:
         fig4 = px.bar(data.groupby('hr', as_index=False)['cnt'].mean(), x='hr', y='cnt')
         fig4.update_xaxes(title="Hour")
         fig4.update_yaxes(title="Average Demand of Bikes")
         st.plotly_chart(fig4, use_container_width=True) 
     with col5:
         fig5 = px.bar(data.groupby('holiday', as_index=False)['cnt'].mean(), x='holiday', y='cnt')
         fig5.update_xaxes(title="Holiday")
         fig5.update_yaxes(title="Average Demand of Bikes")
         st.plotly_chart(fig5, use_container_width=True)
     with col6:
         fig6 = px.bar(data.groupby('weekday', as_index=False)['cnt'].mean(), x='weekday', y='cnt')
         fig6.update_xaxes(title="Weekday")
         fig6.update_yaxes(title="Average Demand of Bikes")
         st.plotly_chart(fig6, use_container_width=True) 
     col7, col8, col9 = st.columns(3)
     with col7:
         fig7 = px.bar(data.groupby('workingday', as_index=False)['cnt'].mean(), x='workingday', y='cnt')
         fig7.update_xaxes(title="Working Day")
         fig7.update_yaxes(title="Average Demand of Bikes")
         st.plotly_chart(fig7, use_container_width=True) 
     with col8:
         fig8 = px.bar(data.groupby('weathersit', as_index=False)['cnt'].mean(), x='weathersit', y='cnt')
         fig8.update_xaxes(title="Weather Situation")
        # fig8.update_yaxes(title="Average Demand of Bikes")
         st.plotly_chart(fig8, use_container_width=True)
     with col9:
         fig9 = px.histogram(data, x=data['temp'])
         fig9.update_xaxes(title="Temperature in °C")
         #fig9.update_yaxes(title="Total Demand of Bikes")
         st.plotly_chart(fig9, use_container_width=True) 
     col10, col11, col12 = st.columns(3)
     with col10:
         fig10 = px.histogram(data, x=data['atemp'])
         fig10.update_xaxes(title="Feeling Temperature in °C")
         #fig10.update_yaxes(title="Total Demand of Bikes")
         st.plotly_chart(fig10, use_container_width=True) 
     with col11:
         fig11 = px.histogram(data, x=data['hum'])
         fig11.update_xaxes(title="Humidity")
         #fig11.update_yaxes(title="Total Demand of Bikes")
         st.plotly_chart(fig11, use_container_width=True)
     with col12:
         fig12 = px.histogram(data, x=data['windspeed'])
         fig12.update_xaxes(title="Windspeed")
        #fig12.update_yaxes(title="Total Demand of Bikes")
         st.plotly_chart(fig12, use_container_width=True)  
     col13, col14, col15 = st.columns(3)
     with col13:
         fig13 = px.histogram(data, x=data['casual'])
         fig13.update_xaxes(title="Causal Customers")
         #fig13.update_yaxes(title="Total Demand of Bikes")
         st.plotly_chart(fig13, use_container_width=True) 
     with col14:
         fig14 = px.histogram(data, x=data['registered'])
         fig14.update_xaxes(title="Registered Customers")
        # fig14.update_yaxes(title="Total Demand of Bikes")
         st.plotly_chart(fig14, use_container_width=True)
     with col15:
         fig15 = px.histogram(data, x=data['cnt'])
         fig15.update_xaxes(title="Total Bike Demand(cnt)")
         #fig15.update_yaxes(title="Total Demand of Bikes")
         st.plotly_chart(fig15, use_container_width=True)   


def statistical(data):
    row = st.sidebar.slider("Number of rows", min_value=0, max_value=data.shape[0])
    col = list(data.columns)
    col.insert(0,'All')
    colmn = st.sidebar.selectbox('Choose Columns ', col)
    subTitle = '<p style="font-family:sans-serif; color:White;font-size:20px; display: table; background-color:Red; text-align: center">Statistical Analysis</p>'
    if row:
        if colmn!='All':
            st.write(data[colmn].head(row))
            st.markdown(subTitle, unsafe_allow_html=True)
            try:
                st.write(data[colmn].describe())
            except:
                st.write("Non numerical column! Data type of column: ", type(colmn))
            fig = px.histogram(data, x=data[colmn])
            st.plotly_chart(fig, use_container_width=True) 
        else:
            st.write(data.head(row))
            st.markdown(subTitle, unsafe_allow_html=True)
            st.write(data.describe())
            plot_charts(data)
     
    else:
        if colmn!='All':
            st.write(data[colmn].head())
            st.markdown(subTitle, unsafe_allow_html=True)
            try:
                st.write(data[colmn].describe())
            except:
                st.write("Non numerical column! Data type of column: ", type(colmn))
            fig = px.histogram(data, x=data[colmn])
            st.plotly_chart(fig, use_container_width=True) 
        else:
            st.write(data.head())
            st.markdown(subTitle, unsafe_allow_html=True)
            st.write(data.describe())
            plot_charts(data)

def main():
    # image = read_image()
    # add_bg_from_local(image)
    title = '<p style="font-family:sans-serif; color:White; background-color:Red; text-align: center; font-size: 32px;">Bike Sharing Demand Analysis</p>'
    st.markdown(title, unsafe_allow_html=True)
    st.sidebar.header("Explore Analysis Types")
    statistical(data)
      
if __name__ == "__main__":
     
    # Call main function
    main()
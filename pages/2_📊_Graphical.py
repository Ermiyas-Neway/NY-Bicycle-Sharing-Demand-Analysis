import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config (
    #page_title="Bike Sharing Demand Analysis Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",)

data = st.session_state['data']
st.subheader("Graphical Analysis")

typeAnalysis = st.sidebar.selectbox('Select Analysis Type?', ('Time', 'Weather'))
if typeAnalysis == 'Time':
    # Fig1 Draw Distribution of cnts
    minday = data.dateFormated.min()
    maxday = data.dateFormated.max()

    startDate = st.sidebar.date_input( "From", value=minday,
                                            min_value=minday, max_value=maxday)
        
    endDate = st.sidebar.date_input( "To", value=maxday,
                                            min_value=minday, max_value=maxday)    
    data1 = data[(data["dateFormated"]>=startDate) & (data["dateFormated"]<=endDate)]

    # Fig2 Evolution of total bikes per day segmented by User Type
    dfCasual = data1.copy().reset_index()
    dfCasual['userType'] = 'casual'
    dfReg = data1.copy().reset_index()
    dfReg['userType'] = 'registered'
    dfUser = pd.merge(dfCasual, dfReg, how='outer')
    dfUser.loc[dfUser.userType == 'casual', 'cnt'] = dfUser['casual']
    dfUser.loc[dfUser.userType == 'registered', 'cnt'] = dfUser['registered']
    # dfUser = dfUser.drop(['casual','registered'], axis=1)
    # dfUser.sort_values(by='instant').head(4)
    fig6 = px.histogram(dfUser, x='dteday', y="cnt", color='userType', title='Total Bikes per Day - Segmented by User Type')
    fig6.update_xaxes(title="Date")
    fig6.update_yaxes(title="Total Number of Bikes")
    st.plotly_chart(fig6, use_container_width=True)

    # Fig10 Bike Demand of each user type over different hours of a day
    hr_UserType = dfUser.groupby(['hr','userType'])['casual','registered'].mean().reset_index(drop=False)
    fig10 = px.bar(hr_UserType, x='hr', y=["casual",'registered'], color='userType', title='Total Bikes per Hour - Segmented by User Type')
    fig10.update_xaxes(title="Time of a Day")
    fig10.update_yaxes(title="Average Demand of Bikes")
    st.plotly_chart(fig10, use_container_width=True)

    # Fig2 Average Demand over each hours of a day
    st.write("Average Demand over a day")
    peakhour = data1.groupby(["hr","workingday"], as_index=False)["cnt"].mean()
    fig2 = px.line(peakhour, x='hr', y="cnt", color='workingday', markers=True)
    fig2.add_bar(x=peakhour['hr'], y=peakhour["cnt"], name="Average Total Demand")
    fig2.update_xaxes(title="Time of a Day")
    fig2.update_yaxes(title="Average Number of Bikes")
    st.plotly_chart(fig2, use_container_width=True)
    expander1 = st.expander("See explanation")
    expander1.write("""
        For the total dataset  the demand for bikes in working days gets at its peak in the morning at 8 and in the afternoon from 16 to 19 hour.
        In non working days, the demand increase to the maximum during the mean day and drops slowly in the afternoon 
    """)

    c1, c2 = st.columns((4, 3))
    days = {0 : "Monday", 1 : "Tuesday", 2 : "Wednesday", 3 : "Thursday", 4 : "Friday",
            5 : "Saturday", 6 : "Sunday"}
    weekData = data1.groupby(["hr","workingday",'peakHour','weekday']).mean().reset_index(drop=False)
    weekData["nameOfDay"] = weekData["weekday"].map(days)
    with c1:
        weekly = dfUser.loc[dfUser.holiday == 0,:].groupby(["weekday","userType"], as_index=False)["cnt"].mean()
        fig7 = px.bar(weekly, x='weekday', y="cnt", color='userType', title="Weekday trend, segmenting by userType (excluding special holidays)")
        st.plotly_chart(fig7, use_container_width=True)
    with c2:
        fig3c2 = px.sunburst(weekData, path=['peakHour', 'nameOfDay'], values='cnt', color='nameOfDay')
        st.plotly_chart(fig3c2, use_container_width=True)
        expander2 = st.expander("See explanation")
        expander2.write("""
        For the total dataset  the demand for bikes in non-peak hours is higher than that of peak hours.
        Non peak hours on Thursday, Saturday, and Tuesday take the top demands of bikes in the week. 
    """)
    # Fig4 Average Demand over different days of month
    daydata = data1.groupby(["day","workingday"]).mean().reset_index(drop=False)
    fig4 = px.line(daydata, x='day', y="cnt", color='workingday', markers=True, 
                    symbol="workingday",title="Average Demand over days of a month")
    fig4.update_xaxes(title="Days of Month")
    fig4.update_yaxes(title="Average Number of Bikes")
    st.plotly_chart(fig4, use_container_width=True)
    expander = st.expander("See explanation")
    expander.write("""
        For the total dataset the demand for bikes for non working days from 21 to 27 is much less than the other days of the month, while for working days it is higher.
        The demand for working days between 7 and 9, and day 28 the demand shows sharp decline. 
    """)

    # Fig5 Average Demand over different months of a year
    seasons = {1 : "springer", 2 : "summer", 3 : "fall", 4 : "winter"}
    monthly = data1.groupby(["season","mnth"]).mean().reset_index(drop=False)
    monthly["Season"] = monthly["season"].map(seasons)
    c1, c2 = st.columns((3, 3))
    with c1:   
        fig5c1 = px.bar(monthly, y="mnth", x=["casual", "registered"], title="Demand in different months",orientation='h')
        fig5c1.update_layout(showlegend=False)
        fig5c1.update_xaxes(title="Average Number of Bikes")
        fig5c1.update_yaxes(title="Months")
        st.plotly_chart(fig5c1, use_container_width=True)
    with c2:
        fig5c2 = px.bar(monthly, x="Season", y=["casual", "registered"], title="Demand in different seasons")
        st.plotly_chart(fig5c2, use_container_width=True) 

elif typeAnalysis == 'Weather':
    # Fig8 Demand with Temperature
    fig8 = px.scatter(data, x="temp", y="cnt", title="Bike Demand with Temperature")
    fig8.update_xaxes(title="Temperature")
    fig8.update_yaxes(title="Total Number of Bikes")
    st.plotly_chart(fig8, use_container_width=True)   

    # # Fig9 Demand with humidity
    fig9 = px.scatter(data, x="hum", y="cnt", title="Bike Demand with Humidity")
    fig9.update_xaxes(title="Humidity")
    fig9.update_yaxes(title="Total Number of Bikes")
    st.plotly_chart(fig9, use_container_width=True)   

    # # Fig9 Demand with Windspeed
    fig9 = px.scatter(data, x="windspeed", y="cnt", title="Bike Demand with Windspeed")
    fig9.update_xaxes(title="Windspeed")
    fig9.update_yaxes(title="Total Number of Bikes")
    st.plotly_chart(fig9, use_container_width=True)  
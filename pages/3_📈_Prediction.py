import streamlit as st
import pandas as pd
import numpy as np
import datetime
import holidays
import joblib
import time

st.set_page_config (
    #page_title="Bike Sharing Demand Analysis Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",)

data = st.session_state['data']

us_holidays = holidays.country_holidays('US',subdiv='NY')            # Import dictionary that contains holidays for NewYork
loaded_model = joblib.load('Completed_model.joblib')

col = ['hr', 'holiday', 'workingday', 'temp', 'hum^2', 'windspeed',
                'temp*windspeed', 'day_night', 'pct_registered_hourly',
                'pct_registered_monthly', 'season_1', 'season_2', 'season_3',
                'season_4', 'mnth_1', 'mnth_2', 'mnth_3', 'mnth_4', 'mnth_5',
                'mnth_6', 'mnth_7', 'mnth_8', 'mnth_9', 'mnth_10', 'mnth_11',
                'mnth_12', 'weekday_0', 'weekday_1', 'weekday_2', 'weekday_3',
                'weekday_4', 'weekday_5', 'weekday_6', 'weathersit_1',
                'weathersit_2', 'weathersit_3', 'weathersit_4',
                'dayInstant_afternoon', 'dayInstant_midday', 'dayInstant_morning',
                'dayInstant_night']

minday=datetime.date(2012, 12, 31)
cc1, cc2, cc3 = st.columns(3)
with cc1:
    predDate = st.date_input("Predition Date", value=datetime.datetime.now(),
                                        min_value=minday)
with cc2:
    predTemp = st.slider("Temperature in Celicius", -30,41)
with cc3:
    predHum = st.slider("Humidity", 0,100)
cc4, cc5, cc6 = st.columns(3)
with cc4:
    predWeathersit = st.selectbox('Weather Situation',
                                    ('Clear or Few clouds or Partly cloudy',
                                    'Mist + Cloudy or Mist + Broken clouds or Mist + Few clouds or Mist',
                                    'Light Snow or Light Rain + Thunderstorm + Scattered clouds or Light Rain + Scattered clouds',
                                    'Heavy Rain + Ice Pallets + Thunderstorm + Mist or Snow + Fog'))
with cc5:
    predHr = st.slider("Hour of the day", 0,24)
with cc6:
    predWindspeed = st.slider("Windspeed", 0,67)
cc7, cc8, cc9= st.columns(3)
with cc7:
    st.text("Press here to predict 👉")
with cc8:
    predict = st.button('Predict')
with cc9:
    predAtemp = st.slider('Feeling Temperature', -30,50)
if predict:

    info = pd.DataFrame(np.nan, index = range(1), columns = [col])
    info['temp'] = predTemp
    info['windspeed'] = predWindspeed
    info['hr'] = predHr
    info['predDate'] = predDate
    info['weekday'] = predDate.weekday()
    info['mnth'] = predDate.month
    #info['yr'] = predDate.year
    info['day'] = predDate.day
    #Checking season
    if predDate.month in [3,4,5]:
        info['season'] = 1
        season = 1
    elif predDate.month in [6,7,8]:
        info['season'] = 2
        season = 2
    elif predDate.month in [9,10,11]:
        info['season'] = 3
        season = 3
    else:
        info['season'] = 4
        season = 4
    #Checking holiday
    if predDate in us_holidays:
        info['holiday'] = 1
    else:
        info['holiday'] = 0
    # creating working day column
    if ((predDate.weekday() in [5,6]) | (predDate in us_holidays)):
        info['workingday'] = 0
    else:
        info['workingday'] = 1
    # Encoding weathersituation
    if predWeathersit == 'Clear or Few clouds or Partly cloudy':
        info['weathersit'] = 1
        weathersit = 1
    elif predWeathersit == 'Mist + Cloudy or Mist + Broken clouds or Mist + Few clouds or Mist':
        info['weathersit'] = 2
        weathersit = 2
    elif predWeathersit == 'Light Snow or Light Rain + Thunderstorm + Scattered clouds or Light Rain + Scattered clouds':
        info['weathersit'] = 3
        weathersit = 3
    elif predWeathersit == 'Heavy Rain + Ice Pallets + Thunderstorm + Mist or Snow + Fog':
        info['weathersit'] = 4
        weathersit = 4

    #Creating DayInstant
    if ((6 <= predHr) & (predHr <= 9)) : 
        info['dayInstant'] = 'morning'
        dayInstant = 'morning'
    elif ((10 <= predHr) & (predHr <= 17)): 
        info['dayInstant'] = 'midday'
        dayInstant = 'midday'
    elif ((18 <= predHr) & (predHr <= 21)): 
        info['dayInstant'] = 'afternoon'
        dayInstant = 'afternoon'
    else: 
        info['dayInstant'] = 'night'
        dayInstant = 'night'

    # Daynight
    if (predHr >= 7) & (predHr <= 23):
        info["day_night"] = 1
    else:
        info["day_night"] = 0

    info['temp^2'] = predTemp**2
    info['temp atemp'] = predTemp * predAtemp
    info['temp hum'] = predTemp * predHum
    info['temp*windspeed'] = predTemp * predWindspeed
    info['atemp^2'] = predAtemp**2
    info['atemp hum'] = predAtemp * predHum
    info['atemp windspeed'] = predAtemp * predWindspeed
    info['hum^2'] = predHum**2
    info['hum windspeed'] = predHum * predWindspeed
    info['windspeed^2'] = predWindspeed**2
    #Dummyfying
    info[f"mnth_{predDate.month}"] = 1
    info[f"season_{season}"] = 1
    info[f"weekday_{predDate.weekday()}"] = 1
    info[f"weathersit_{weathersit}"] = 1
    info[f"dayInstant_{dayInstant}"] = 1
    info.drop(['season','mnth','weekday','weathersit','predDate','dayInstant'], axis=1, inplace=True)
    info.fillna(0, inplace=True)
    pred = loaded_model.predict(info[col])
    cc10, cc11 = st.columns(2)
    with st.spinner('Wait for it...'):
        time.sleep(5)
        st.success('Done!')
    with cc10:
        st.subheader("Our best prediction demand is:")
    with cc11:
        st.subheader(round(pred[0],ndigits=0))



#Prediction to csv
st.sidebar.write("Upload csv file to have predictions *Optional")
uploaded_file = st.sidebar.file_uploader("Choose csv file")
Predict_csv = st.sidebar.button('Make Prediction')

if uploaded_file is not None:
    if Predict_csv:
        uplodedFile= pd.read_csv(uploaded_file)
        uplodedFile.drop(['instant','dteday'], axis=1, inplace=True)
        merged = uplodedFile
        # Feature Engineering
        #Creating DayInstant
        merged['dayInstant'] = merged.hr.apply(lambda x:'morning' if ((x <= 9)&(x>=6)) else 'midday' if ((x>=10) & (x<=17)) else 'afternoon' if ((x>=18) & (x<=21)) else 'night')


        # Daynight
        merged["day_night"] = merged.hr.apply(lambda x: 1 if ((x >= 7) & (x <= 23)) else 0)

        merged['temp^2'] = uplodedFile.temp**2
        merged['temp atemp'] = uplodedFile.temp * uplodedFile.atemp
        merged['temp hum'] = uplodedFile.temp * uplodedFile.hum
        merged['temp*windspeed'] = uplodedFile.temp * uplodedFile.windspeed
        merged['atemp^2'] = uplodedFile.atemp**2
        merged['atemp hum'] = uplodedFile.atemp * uplodedFile.hum
        merged['atemp windspeed'] =  uplodedFile.atemp *  uplodedFile.windspeed
        merged['hum^2'] = uplodedFile.hum**2
        merged['hum windspeed'] = uplodedFile.hum * uplodedFile.windspeed
        merged['windspeed^2'] = uplodedFile.windspeed**2

        # Aggregating and add feature
        data['pct_registered'] = data['registered']/data['cnt']
        pct_registered_hourly = data.groupby('hr')['pct_registered'].mean().to_dict()
        merged['pct_registered_hourly'] = merged['hr'].map(pct_registered_hourly)
        pct_registered_monthly = data.groupby('mnth')['pct_registered'].mean().to_dict()
        merged['pct_registered_monthly'] = merged['mnth'].map(pct_registered_monthly)
        
        #Dummyfying
        merged = pd.get_dummies(merged, columns=['season','mnth','weekday','weathersit','dayInstant'])
        merged.fillna(0, inplace=True)
        #st.dataframe(merged)
        csvPred = loaded_model.predict(merged[col])
        uplodedFile['Predicted'] = csvPred.tolist()
        download = uplodedFile.to_csv().encode('utf-8')
        st.success('Successful!', icon="✅")
        st.sidebar.download_button(
            label="Download prediction as CSV",
            data=download,
            file_name='Predictions.csv',
            mime='text/csv',)
        
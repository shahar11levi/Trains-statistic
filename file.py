import streamlit as st
import pandas as pd
import numpy as np
import urllib


st.title('Trains statistics')

DATA_PATH = '.'


@st.cache_data
def load_data(file, p, i=None):
    return pd.read_csv(p / (file + ".csv"), index_col=i)


# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = pd.read_csv('./trains.csv' ,delimiter='|')
data.columns = ['Year', 'Month', 'train_station', 'late', 'count']

# Notify the reader that the data was successfully loaded.
data_load_state.text("")
station = st.sidebar.selectbox('train_station',data['train_station'].unique())

station_data = data[data['train_station'] == station]
station_data['date'] = pd.to_datetime(station_data[['Year', 'Month']].assign(day=1))
station_data = station_data[['date', 'late', 'count']]


station_data_late = (station_data[station_data['late'] == 'איחור']).reset_index()
station_data_early = (station_data[station_data['late'] == 'הקדמה ביציאה']).reset_index()
station_data_on_time = (station_data[station_data['late'] == 'בזמן']).reset_index()

new_data = pd.DataFrame({
    'date': station_data_late['date'],
    'late': station_data_late['count'],
    'early': station_data_early['count'],
    'on_time': station_data_on_time['count']
})

new_data = new_data.sort_values(by='date').reset_index(drop=True)

st.line_chart(new_data[['late', 'early', 'on_time']])

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(new_data)


st.subheader('Number of late trains by train station')


# st.bar_chart(data.value_counts())
# st.bar_chart(data['late'].value_counts())
# hist_values = np.histogram(data[''].dt.hour, bins=24, range=(0,24))[0]
# st.bar_chart(hist_values)
# #
# st.subheader('Number of pickups by minute')
# hist_minute_values = np.histogram(data[DATE_COLUMN].dt.minute, bins=60, range=(0,60))[0]
# st.bar_chart(hist_minute_values)
#
# hour_to_filter = st.slider('hour', 0, 23, 17)  # min: 0h, max: 23h, default: 17h
# filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
# st.subheader(f'Map of all pickups at {hour_to_filter}:00')
# st.map(filtered_data)
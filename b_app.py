import pandas as pd
import tensorflow as tf
import streamlit as st

from keras import backend as K

def root_mean_squared_error(y_true, y_pred):
    '''
    RMSE for tensorflow
    '''
    return K.sqrt(K.mean(K.square(y_pred - y_true))) 

# load pre-trained model
mod = tf.keras.models.load_model('dnn_three_feature_model'
    , custom_objects = {'root_mean_squared_error': root_mean_squared_error})

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title = 'Compare Two Cities'
    , page_icon = ':office:'
    , layout = 'wide')

st.title('Compare Two Cities')
st.write('Select two cities to compare')

city_list = [
    ''
    , 'My City Is Not Listed'
    , 'Albuquerque, New Mexico'
    , 'Atlanta, Georgia'
    , 'Austin, Texas'
    , 'Boise, Idaho'
    , 'Boston, Massachusetts'
    , 'Charlotte, North Carolina'
    , 'Chicago, Illinois'
    , 'Dallas, Texas'
    , 'Denver, Colorado'
    , 'Detroit, Michigan'
    , 'Honolulu, Hawaii'
    , 'Houston, Texas'
    , 'Jacksonville, Florida'
    , 'Jersey City, New Jersey'
    , 'Las Vegas, Nevada'
    , 'Los Angeles, California'
    , 'Minneapolis - St. Paul, Minnesota'
    , 'Miami, Florida'
    , 'Nashville, Tennessee'
    , 'New York City, New York'
    , 'Orlando, Florida'
    , 'Pittsburgh, Pennsylvania'
    , 'Portland, Oregon'
    , 'Salt Lake City, Utah'
    , 'San Antonio, Texas'
    , 'San Francisco, California'
    , 'San Jose, California'
    , 'Seattle, Washington'
    , 'Tampa, Florida'
    , 'Washington D.C.'
]

def add_country_to_city(city_name):
    if city_name == 'New York City, New York':
        return 'New York City, United States'
    else:
        return f'{city_name}, United States'

def get_price_index(input_df, city_name_country):
    filt1 = df['City'] == city_name_country

    idx = df[filt1].index[0]
    return df.at[idx, 'Price_Index']

def get_pct_diff_pi(pi1, pi2):
    '''
    returns percentage difference of two price indicies
    '''
    print(pi2 - pi1)
    print((pi2 - pi1) / pi1)
    print(((pi2 - pi1) / pi1) * 100)
    pct_diff = ((pi2 - pi1) / pi1) * 100
    return pct_diff
    

df = pd.read_csv('price_indicies.csv')

left_column, right_column = st.columns(2)
with left_column:
    st.subheader('City 1')
    city_name1 = st.selectbox(label = 'Select a city'
        , options = city_list
        , key = 'city1')
    city_name1_selected = city_name1
    # lookup price index
    try:
        city_name_country1 = add_country_to_city(city_name1)

        pi1 = get_price_index(input_df = df
            , city_name_country = city_name_country1)
    except:
        city_name_country1 = 'Please select a City!'
        pi1 = ''

    # for debugging
    # st.write(f'Price Index: {pi1}')

with right_column:
    st.subheader('City 2')
    city_name2 = st.selectbox(label = 'Select a city'
        , options = city_list
        , key = 'city2')
    city_name2_selected = city_name2
    city_name_country2 = add_country_to_city(city_name2)

     # lookup price index
    try:
        city_name_country2 = add_country_to_city(city_name2)

        pi2 = get_price_index(input_df = df
            , city_name_country = city_name_country2)
    except:
        city_name_country2 = 'Please select a City!'
        pi2 = ''

    # for debugging
    # st.write(f'Price Index: {pi2}')

fast_food_col_name = 'Combo meal in fast food restaurant (big mac meal or similar)'
rent_col_name = 'Monthly rent for 85 m2 (900 sqft) furnished accommodation in expensive area'
transit_col_name = 'Monthly ticket public transport'

# ---- SIDEBAR ----
if city_name1_selected == 'My City Is Not Listed':
    st.sidebar.header('Custom City 1')
    city_name1    = st.sidebar.text_input('City name', key = 'city1')
    rent1         = st.sidebar.number_input('Monthly Rent (900 sqft) in expensive area', key = 'rent1')
    fast_food1    = st.sidebar.number_input('Combo meal in fast food restaurant (big mac meal or similar)', key = 'fast_food1')
    public_trans1 = st.sidebar.number_input('Monthly ticket for public transport', key = 'public_trans1')

    city1_df = pd.DataFrame({
        fast_food_col_name: [fast_food1]
        , rent_col_name: [rent1]
        , transit_col_name: [public_trans1]
    })

    # get the predicted price index
    pi1 = mod.predict(city1_df)[0][0]

    # for debugging
    # st.sidebar.write(pi1)

if city_name2_selected == 'My City Is Not Listed':
    st.sidebar.header('Custom City 2')
    city_name2    = st.sidebar.text_input('City name', key = 'city2')
    rent2         = st.sidebar.number_input('Monthly Rent (900 sqft) in expensive area', key = 'rent2')
    fast_food2    = st.sidebar.number_input('Combo meal in fast food restaurant (big mac meal or similar)', key = 'fast_food2')
    public_trans2 = st.sidebar.number_input('Monthly ticket for public transport', key = 'public_trans2')

    city2_df = pd.DataFrame({
        fast_food_col_name: [fast_food2]
        , rent_col_name: [rent2]
        , transit_col_name: [public_trans2]
    })

    # get the predicted price index
    pi2 = mod.predict(city2_df)[0][0]

    # for debugging
    # st.sidebar.write(pi2)

if st.button('Compare Cities'):
    try:
        if pi2 > pi1:
            more_less = 'more'
        if pi2 < pi1:
            more_less = 'less'
        # calculate percentage difference
        pct_diff_pi = abs(get_pct_diff_pi(pi1, pi2))
        pct_diff_pi = f'{pct_diff_pi:.1f}%'
        final_str = f'{city_name2} is {pct_diff_pi} {more_less} expensive than {city_name1}.'
        if pi2 == pi1:
            final_str = f'{city_name2} is the same as {city_name1}.'
    except Exception as e:
        final_str = 'Please select different two cities.'

    st.subheader(final_str)
   
# Hide Streamlit branding
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html = True)

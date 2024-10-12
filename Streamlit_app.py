# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col


# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom smoothie")

# Establish connection
cnx = st.connection("snowflake")
session = cnx.session()

# Fetch fruit options
my_dataframe = session.table("smoothies.public.fruit_options").select(col("fruit_name")).to_pandas()

# Get user input
name_on_order = st.text_input("Name on smoothie")
ingredients_list = st.multiselect(
    label='Choose up to 5 ingredients',
    options=my_dataframe['FRUIT_NAME'].tolist(),
    max_selections=5
)

if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)
    st.write(f"Selected ingredients: {ingredients_string}")
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (INGREDIENTS, NAME_ON_ORDER)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """
    time_to_insert = st.button("Submit order")

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f"Your smoothie is ordered, {name_on_order}!", icon="✅")

import requests


# Fetch data from Fruityvice API
try:
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
    fruityvice_data = fruityvice_response.json()  # Ensure response is in JSON format
    st.json(fruityvice_data)  # Display raw JSON data

    # If the response is complex, you might need to handle it more carefully
    fv_df = st.dataframe(data=fruityvice_data, use_container_width=True)
except requests.exceptions.JSONDecodeError:
    st.error("Failed to decode JSON. Please check the API response.")
except Exception as e:
    st.error(f"An error occurred: {e}")

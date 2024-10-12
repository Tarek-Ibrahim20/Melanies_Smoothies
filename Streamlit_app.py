# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")

st.write(
            """Choose the fruits you want in your custom smoothie"""
)

from snowflake.snowpark.functions import col

cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("fruit_name"))
# st.dataframe(data=my_dataframe, use_container_width=True)

name_on_order = st.text_input("Name on smoothies ")

ingredients_list  = st.multiselect(
                        label = 'Choose up to 5 ingredients' ,
                        options= my_dataframe ,
                        max_selections = 5
                    )

                    
if ingredients_list:
    #st.text(ingredients_list )
    
    ingredients_string = ''

    for f in ingredients_list:
        ingredients_string += f +' '
    
    st.write(ingredients_string)


    my_insert_stmt = """
                      insert into smoothies.public.orders(ingredients, NAME_ON_ORDER)
                      values ('""" + ingredients_string + """',
                             '""" + name_on_order + """')
                     """
    

    #st.write(my_insert_stmt)
    #st.stop()
    time_to_insert = st.button("submet order")

    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        
        st.success(f'Your Smoothie is ordered\, {name_on_order}!', icon="✅")







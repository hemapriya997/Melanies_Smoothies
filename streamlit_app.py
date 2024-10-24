# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customise Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruit you want to use.
    """
)


cnx=st.connection("snowflake")
session = cnx.session()

name_on_order = st.text_input("Name of Smoothie:")
st.write("The name on your smoothie will be:", name_on_order)
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect('Choose upto 5 ingredients:',my_dataframe,max_selections=5)

if ingredients_list:

    ingredients_string=''

    for fruit_chosen in ingredients_list:
        ingredients_string +=fruit_chosen + ' '

    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','
            """ + name_on_order + """ ')"""

    
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
    st.text(fruityvice_response)
    time_to_insert = st.button('Submit')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")



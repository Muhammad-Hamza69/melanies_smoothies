# # Import python packages
# import streamlit as st
# import requests
# from snowflake.snowpark.functions import col

# # Write directly to the app
# st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
# st.write(
#   """choose the fruits u want in your custom Smoothie! 
#   """
# )



# name_on_order = st.text_input("Name on Smoothie: ")
# st.write("The name on your Smoothie will be: ", name_on_order)


# cnx = st.connection("snowflake")
# session = cnx.session()
# my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# # st.dataframe(data=my_dataframe, use_container_width=True)
# ingredients_list = st.multiselect(
#     'Choose up to 5 ingredients: '
#     , my_dataframe
#     , max_selections = 5
# )
# if ingredients_list:
#     ingredients_string = ''
  
#     for fruit_chosen in ingredients_list:
#         ingredients_string+=fruit_chosen + ' '
#         st.subheader(fruit_chosen + ' Nutrition Information')
#         smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
#         sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

#     my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
#             values ('""" + ingredients_string + """', '""" + name_on_order + """')"""

    
#     time_to_insert = st.button('Submit Order')

#     if time_to_insert:
#         session.sql(my_insert_stmt).collect()
#         st.success(f'Your Smoothie is ordered! {name_on_order}!', icon="✅")




# import streamlit as st
# import requests
# import pandas as pd # Pandas import karna zaroori hai
# from snowflake.snowpark.functions import col

# st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
# st.write("Choose the fruits u want in your custom Smoothie!")

# name_on_order = st.text_input("Name on Smoothie: ")
# st.write("The name on your Smoothie will be: ", name_on_order)

# # Snowflake Connection
# cnx = st.connection("snowflake")
# session = cnx.session()

# # Data fetch karke list mein convert karna
# my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# # Snowflake dataframe ko list mein convert karein taake multiselect sahi chale
# pd_df = my_dataframe.to_pandas()

# ingredients_list = st.multiselect(
#     'Choose up to 5 ingredients: ',
#     pd_df['FRUIT_NAME'], # Yahan list pass karein
#     max_selections = 5
# )

# if ingredients_list:
#     ingredients_string = ''
  
#     for fruit_chosen in ingredients_list:
#         ingredients_string += fruit_chosen + ' '
        
#         # Har fruit ka apna header
#         st.subheader(fruit_chosen + ' Nutrition Information')
        
#         # API Call: Yahan hum fruit_chosen ka variable use kar rahe hain
#         # Note: API call loop ke andar honi chahiye taake har fruit ka data aaye
#         smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
        
#         # API response ko table mein dikhana
#         if smoothiefroot_response.status_code == 200:
#             st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
#         else:
#             st.error(f"Sorry, {fruit_chosen} is not in our database.")

#     # Insert Statement
#     my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
#             values ('""" + ingredients_string + """', '""" + name_on_order + """')"""
    
#     time_to_insert = st.button('Submit Order')

#     if time_to_insert:
#         session.sql(my_insert_stmt).collect()
#         st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")






# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col

# --- UI Setup ---
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("choose the fruits u want in your custom Smoothie!")

# User Input for Name
name_on_order = st.text_input("Name on Smoothie: ")
st.write("The name on your Smoothie will be: ", name_on_order)

# --- Snowflake Connection ---
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# --- Ingredient Selection ---
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients: ',
    my_dataframe,
    max_selections = 5
)

# --- Display Nutrition & Build Insert String ---
if ingredients_list:
    ingredients_string = ''
  
    for fruit_chosen in ingredients_list:
        # Snowflake Row object se string nikalne ke liye [0] use karein
        fruit_name = fruit_chosen[0]
        ingredients_string += fruit_name + ' '
        
        # Har fruit ka apna header
        st.subheader(fruit_name + ' Nutrition Information')
        
        # API Call (Dynamic URL)
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_name)
        
        # Table display
        # Note: Agar fruit database mein nahi hoga (jaise Ximenia), 
        # toh API khud error message bhejegi jo table mein show ho jayega.
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    # --- Database Insert Logic ---
    # SQL query build karein
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """', '""" + name_on_order + """')"""
    
    # Submit Button
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered! {name_on_order}!', icon="✅")

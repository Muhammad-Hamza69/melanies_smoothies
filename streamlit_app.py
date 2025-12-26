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
import pandas as pd
import requests
from snowflake.snowpark.functions import col

# --- Title ---
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("choose the fruits u want in your custom Smoothie!")

# User Input
name_on_order = st.text_input("Name on Smoothie: ")
st.write("The name on your Smoothie will be: ", name_on_order)

# --- Snowflake Connection ---
cnx = st.connection("snowflake")
session = cnx.session()

# Bina Pandas ke data ko handle karne ka sahi tareeka: 
# Dataframe se values nikaal kar unhe ek list bana lein

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))

st.dataframe(data = my_dataframe, use_container_width = True)
st.stop()

# Convert the Snowpark Dataframe to a Pandas Dataframe so we can use the LOC function 
# pd_df = my_dataframe.to_pandas()
# st.dataframe(pd_df)
# st.stop()

# --- Multiselect ---
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients: ',
    my_dataframe,
    max_selections = 5
)

if ingredients_list:
    ingredients_string = ''
  
    for fruit_chosen in ingredients_list:
        # AGAR AAPKA PICHLA CODE 'T' DIKHA RAHA THA, TOH YAHAN [0] HATADEIN
        # Streamlit ab Row objects ko khud hi string mein convert kar deta hai
        fruit_name = fruit_chosen 
        
        ingredients_string += fruit_name + ' '

        # search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_name, 'SEARCH_ON'].iloc[0]
        # st.write('The search value for ', fruit_name,' is ', search_on, '.')
        
        # Heading: Ab yeh poora naam dikhayega (e.g., Tangerine Nutrition Information)
        st.subheader(fruit_name + ' Nutrition Information')
        
        # API Call: Poore naam ke sath call hogi
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_name)
        
        # Table Display: Jaisa image mein hai
        st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    # --- Order Submission ---
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """', '""" + name_on_order + """')"""
    
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered! {name_on_order}!', icon="✅")

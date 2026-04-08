# Import python packages
import streamlit as st
import requests
import pandas as pd
from snowflake.snowpark.functions import col

# Title
st.title("🥤 Customize Your Smoothie!")
st.write("Choose the fruits you want in your custom Smoothie!")

# Name input
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# Snowflake session
cnx = st.connection("snowflake")
session = cnx.session()

# Load data with SEARCH_ON
my_dataframe = session.table("smoothies.public.fruit_options").select(
    col("FRUIT_NAME"),
    col("SEARCH_ON")
)

# Convert Snowpark DataFrame to Pandas DataFrame
pd_df = my_dataframe.to_pandas()

# Fruit list for multiselect
fruit_list = pd_df["FRUIT_NAME"].tolist()

# Multiselect
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_list,
    max_selections=5
)

# Logic
if ingredients_list:
    ingredients_string = ""

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + " "

        # Get SEARCH_ON value from Pandas DataFrame
        search_on = pd_df.loc[
            pd_df["FRUIT_NAME"] == fruit_chosen, "SEARCH_ON"
        ].iloc[0]

        st.write("The search value for", fruit_chosen, "is", search_on, ".")

        st.subheader(f"{fruit_chosen} Nutrition Information")

        smoothiefroot_response = requests.get(
            f"https://my.smoothiefroot.com/api/fruit/{search_on}"
        )

        data = smoothiefroot_response.json()

        if "error" in data:
            st.warning(data["error"])
        else:
            st.dataframe(pd.DataFrame([data]), use_container_width=True)

    # Build INSERT statement
    my_insert_stmt = f"""
    insert into smoothies.public.orders(ingredients, name_on_order)
    values ('{ingredients_string}', '{name_on_order}')
    """

    # Submit button
    time_to_insert = st.button("Submit Order")

    # Insert only on click
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f"Your Smoothie is ordered, {name_on_order}!", icon="✅")

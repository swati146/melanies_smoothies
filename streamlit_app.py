if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

        # Get SEARCH_ON value
        search_on = pd_df.loc[
            pd_df["FRUIT_NAME"] == fruit_chosen, "SEARCH_ON"
        ].iloc[0]

        # UI heading
        st.subheader(f"{fruit_chosen} Nutrition Information")

        # API call using SEARCH_ON
        smoothiefroot_response = requests.get(
            f"https://my.smoothiefroot.com/api/fruit/{search_on}"
        )

        data = smoothiefroot_response.json()

        # Handle missing fruits
        if "error" in data:
            st.warning(data["error"])
        else:
            st.dataframe(pd.DataFrame([data]), use_container_width=True)

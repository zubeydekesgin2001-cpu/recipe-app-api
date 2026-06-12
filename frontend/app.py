import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title("Recipe Management App")

menu = st.sidebar.selectbox(
    "Menu",
    [
        "Recipe List",
        "Recipe Details",
        "Create Recipe",
        "Add Rating"
    ]
)

if menu == "Recipe List":
    st.header("Recipes")

    try:
        response = requests.get(f"{API_URL}/recipes/")
        recipes = response.json()

        for recipe in recipes:
            st.subheader(recipe["title"])
            st.write(f"Category: {recipe['category']}")
            st.write(f"Difficulty: {recipe['difficulty']}")
            st.write(f"Description: {recipe['description']}")
            st.write("---")

    except:
        st.error("API unavailable")


elif menu == "Recipe Details":
    st.header("Recipe Details")

    recipe_id = st.number_input(
        "Recipe ID",
        min_value=1,
        step=1
    )

    if st.button("Get Recipe"):
        try:
            response = requests.get(
                f"{API_URL}/recipes/{recipe_id}"
            )

            if response.status_code == 200:
                recipe = response.json()

                st.subheader(recipe["title"])
                st.write(recipe["description"])
                st.write("Ingredients:", recipe["ingredients"])
                st.write("Instructions:", recipe["instructions"])
                st.write("Category:", recipe["category"])
                st.write("Difficulty:", recipe["difficulty"])

                if recipe["photo"]:
                    image_url = (
                        f"{API_URL}/{recipe['photo']}"
                    )
                    st.image(image_url)

                ratings_response = requests.get(
                    f"{API_URL}/ratings/"
                )

                ratings = ratings_response.json()

                recipe_ratings = [
                    r["value"]
                    for r in ratings
                    if r["recipe_id"] == recipe_id
                ]

                if recipe_ratings:
                    avg = (
                        sum(recipe_ratings)
                        / len(recipe_ratings)
                    )
                    st.write(
                        f"Average Rating: {avg:.2f}"
                    )

            else:
                st.error("Recipe not found")

        except:
            st.error("API unavailable")


elif menu == "Create Recipe":
    st.header("Create Recipe")

    title = st.text_input("Title")
    description = st.text_area("Description")
    ingredients = st.text_area("Ingredients")
    instructions = st.text_area("Instructions")
    category = st.text_input("Category")
    difficulty = st.selectbox(
        "Difficulty",
        ["Easy", "Medium", "Hard"]
    )
    user_id = st.number_input(
        "User ID",
        min_value=1,
        step=1
    )

    if st.button("Create Recipe"):
        data = {
            "title": title,
            "description": description,
            "ingredients": ingredients,
            "instructions": instructions,
            "category": category,
            "difficulty": difficulty,
            "photo": "",
            "user_id": user_id
        }

        try:
            response = requests.post(
                f"{API_URL}/recipes/",
                json=data
            )

            if response.status_code == 200:
                st.success("Recipe created")
            else:
                st.error(response.text)

        except:
            st.error("API unavailable")


elif menu == "Add Rating":
    st.header("Add Rating")

    recipe_id = st.number_input(
        "Recipe ID",
        min_value=1,
        step=1
    )

    user_id = st.number_input(
        "User ID",
        min_value=1,
        step=1,
        key="user"
    )

    value = st.slider(
        "Rating",
        1,
        5
    )

    comment = st.text_area("Comment")

    if st.button("Add Rating"):
        data = {
            "value": value,
            "comment": comment,
            "user_id": user_id,
            "recipe_id": recipe_id
        }

        try:
            response = requests.post(
                f"{API_URL}/ratings/",
                json=data
            )

            if response.status_code == 200:
                st.success("Rating added")
            else:
                st.error(response.text)

        except:
            st.error("API unavailable")
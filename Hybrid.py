# -*- coding: utf-8 -*-
from streamlit_option_menu import option_menu
import pickle
import streamlit as st
import re
import pandas as pd
import requests
import bz2
from PIL import Image
import pickle
from pathlib import Path
import streamlit_authenticator as stauth


def main():
    """Movie recommendaion App with Streamlit """
    st.title("Movie Recommendaion System")
    names = ["Syeni Oswald", "Arome Emmanuel", "Murtala Umar", "explore"]
    usernames = ["soswald", "emmanuel", "Umar", "explore"]

    # load hashed passwords
    file_path = Path(__file__).parent / "hased_pw.pkl"
    with file_path.open("rb") as file:
        hashed_passwords = pickle.load(file)

    authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
                                        "home screen", "abcdef", cookie_expiry_days=10)

    names, authentication_status, username = authenticator.login(
        "Login", "main")

    if authentication_status == False:
        st.error("Username/password is incorrect")

    if authentication_status == None:
        st.warning("Enter your username and password")

    if authentication_status:

        # Creates a main title and subheader on your page -
        # these are static across all pages
        with st.sidebar:
            selection = option_menu(
                menu_title="Main Menu",
                options=["Recommendation", "About us",
                         "Contact us", "Documentation"],
                icons=["emoji-expressionless",
                       "robot", "people-fill", "phone", "book"],
                menu_icon="cast",
                default_index=0
            )

        if selection == "Recommendation":
            def Poster(title):
                if title:
                    try:
                        url = f"http://www.omdbapi.com/?t={title}&apikey=2818afea"
                        re = requests.get(url)
                        re = re.json()
                        col1, col2 = st.columns([1, 2])
                        with col1:
                            st.image(re["Poster"])
                        with col2:
                            st.subheader(re['Title'])
                            st.caption(
                                f"Genre: {re['Genre']} Year: {re['Year']} ")
                            st.write(re['Plot'])
                            st.text(F"Rating: {re['imdbRating']}")
                            st.progress(float(re['imdbRating']))
                    except:
                        st.error('')

            def clean(title):
                title = re.sub("[^a-zA-Z]", " ", title)
                return title
            movies = pickle.load(open('movie_list.pkl', 'rb'))
            similarity = pickle.load(open('similarity.pkl', 'rb'))
            indices = pd.Series(
                movies.index, index=movies['title']).drop_duplicates()

            def recommend(title, movies, similarity):
                idx = indices[title]
                distances = sorted(
                    list(enumerate(similarity[idx])), reverse=True, key=lambda x: x[1])
                recommended_movie_names = []

                for i in distances[1:10]:
                    recommended_movie_names.append(movies.iloc[i[0]].title)
                return recommended_movie_names

            st.title('Movie Recommender System')
            st.image('Image_header.png', use_column_width=True)

            selected_movie_name = st.selectbox(
                "Which movie are you looking for?", movies['title'].values)
            if st.button('Recommend'):
                st.write("#### You have chosen")
                indices = pd.Series(
                    movies.index, index=movies['title']).drop_duplicates()
                Poster(selected_movie_name)
                recomm = []
                recommended_movies = recommend(
                    selected_movie_name, movies, similarity)
                st.write("#### We recommend these movies for you")
                for i in recommended_movies:
                    Poster(i)
                    recomm.append(i)

        if selection == "About us":
            st.title("NFINATE CONSULTANT")
            st.subheader("Who are we?")
            st.write(
                "NFINATE CONSULTANT is a freelance tech startup specialised in Data Science, Machine Learning, Data Analysis, and Business Intelligence. ")
            st.write("Our team of expert scientists and researchers is dedicated to helping companies derive insightful information from existing data. By doing so Eagle Analytics hardwork is oriented in facilitating decision making as well prediction in business setting.")
            st.write(
                "Our vision is to make the world a better place through hidden insight in data")
            st.subheader("Meet the team")
            # team members
            Oswald = Image.open('img/Oswald.png')
            Mune = Image.open('img/Mune.png')
            Abienwense = Image.open('img/Abienwese.png')
            Jan = Image.open('img/Jan.png')

            # Oswald
            col1, col2 = st.columns(2)
            with col1:
                st.image(Oswald)
            with col2:
                st.subheader("Oswald Cedric Syeni (CEO)")
                st.write("Oswald has his PhD in Business Intellingence and over 15 years of experience running most successful businesses like Google, Microsoft, Oracle and Explore AI")
                st.write(
                    "With this blend of skills and experience the CEO and his team has helped over 250 startups improve their service")

            # Mune
            col1, col2 = st.columns(2)
            with col1:
                st.image(Mune)
            with col2:
                st.subheader("Mune Vani (Co-founder)")
                st.write(
                    "Mune has a master in Project Management from Havard University and has applied his knowlege in numerous fortune Startup")
                st.write("During her 30 years of experience she has managed the development of well known and successfull products like Iphone 6, Iphone X, Iphone 11 Pro, and recently Samsung 22 before he moved to NFINITE CONSULTANTS ")

            # Abienwense
            col1, col2 = st.columns(2)
            with col1:
                st.image(Abienwense)
            with col2:
                st.subheader("Abienwense Head of R&D")
                st.write("Being a Master holder in Machine learning from the University of Michigan, Abienwense developed the machine learning algorithm for Tesla self driving and was the team lead for its implementation")
                st.write("She has also been CTO of numero organizations like Alibaba, Jumia, and Amazone where he has gained practinal knowledge that he put in use for the succcess of the startup")

            # Jan
            col1, col2 = st.columns(2)
            with col1:
                st.image(Jan)
            with col2:
                st.subheader("JAN LEGODI  (COO)")
                st.write(
                    "He has her PhD in Business Administration from Polytechnique University in Canada and is dedicated in successfuly running Business.")
                st.write(
                    "he spent the fifteen years of her successful career at Silicon Valley where he has helped the compamy inscrease its revenue by 80 percent")

        if selection == "Contact us":
            st.title("Contact us")
            col1, col2 = st.columns(2)
            with col1:

                st.subheader("Contact info")
                st.write("Cola Street, Near ATTC,")
                st.write("Adjacent Sociate Generale, Head Office,")
                st.write("Kokomlemle, P.O. Box AN0000, Accra")
                st.write("Telephone:+233 00 111 2222")
                st.write("WhatsApp:+234 210 12344 1390")
                st.write("Email: eagleanalytics@gmail.com")
                st.write("Website: eagleanalytics.com")
            with col2:
                st.subheader("Email Us")
                email = st.text_input("Enter your email")
                message = st.text_area("Enter your message")
                st.button("Send")

        # logout
        authenticator.logout("Logout", "sidebar")


# Required to let Streamlit instantiate our web app.
if __name__ == '__main__':
    main()

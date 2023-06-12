import streamlit as st
import leaderboardLASC
import streamlit as st
from PIL import Image


PAGES = {
    "Lymph Atar Segmentation Challenge": leaderboardLASC
}

image = Image.open('lasc.png')
st.sidebar.image(image)
#st.sidebar.title('Navigation')
#selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES["Lymph Atar Segmentation Challenge"]
page.app()

st.sidebar.title("About")
st.sidebar.info(
    """
    Lymph Atar Segmentation Challenge was developed during 2023 SIIM Hackaton.
    
    Team: Joanna Song, Sabeen Ahmed, Sabrina Khan, Lucas Folio, João Santinha, Les Folio.
    
    This app was developed and is maintained by João Santinha.
"""
)

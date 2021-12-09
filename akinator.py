# akinator.py
import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

def app():
    if 'juste' not in st.session_state:
        st.session_state.juste = 0

    if 'faux' not in st.session_state:
        st.session_state.faux = 0

    if 'tentatives' not in st.session_state:
        st.session_state.tentatives = 0

    def raison():
        st.session_state.juste += 1
        st.session_state.tentatives += 1

    def tort():
        st.session_state.faux += 1
        st.session_state.tentatives += 1

    # st.write(st.session_state)

    st.title("Akinator de chiffre")

    try :
        def justesse():
            justesse = st.session_state.juste/st.session_state.tentatives*100
            return justesse

        st.write("Akinator prédit juste à "+str(justesse())+"%")
    except :
        st.write()

    reconstructed_model = tf.keras.models.load_model("models/model")

    #Importer un csv
    csv_dowloaded = pd.read_csv(r'data/test.csv',delimiter=',', decimal='.')

    # preprocessing des inputs
    def preprocess(input):
        input_preprocess = input / 255
        input_preprocess = np.array(input).reshape((-1, 28, 28, 1))
        return input_preprocess

    # afficher l'image en input

    def see_img(input):
        image = np.array(input).reshape([28,28])
        fig, ax = plt.subplots()
        ax.imshow(image, cmap=plt.get_cmap('gray'))
        st.pyplot(fig)

    def my_prediction():

        # choisir une ligne au hasard dans le dataframe test

        my_input = csv_dowloaded.sample(n=1)

    # afficher l'image en input

        see_img(my_input)

    # afficher la sortie cad le numero predit : print(argmax)
        my_predict = np.argmax(reconstructed_model.predict(preprocess(my_input)), axis=1)
        return str(my_predict)[1]

    st.write("Souhaites-tu me mettre à l'épreuve ? ")

    if st.button('Oui je le veux'):
        st.write("Je vois, je vois ... ")
        st.write("Je vois un "+my_prediction())
        st.button('Tu as raison Akinator',key='raison', on_click=raison)
        st.button('Tu as tort Akinator', key="tort", on_click=tort)
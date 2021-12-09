# dessinemoi.py
import pandas as pd
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import streamlit as st
from streamlit_drawable_canvas import st_canvas
import tensorflow as tf

def app():
    
    if 'juste_d' not in st.session_state:
        st.session_state.juste_d = 0

    if 'faux_d' not in st.session_state:
        st.session_state.faux_d = 0

    if 'tentatives_d' not in st.session_state:
        st.session_state.tentatives_d = 0

    def raison():
        st.session_state.juste_d += 1
        st.session_state.tentatives_d += 1

    def tort():
        st.session_state.faux_d += 1
        st.session_state.tentatives_d += 1

    st.title("Le petit prince ne veut plus de mouton : ")

    st.write("S’il vous plaît… dessine-moi un chiffre !")

    c1, c2 = st.columns(( 3, 1))

    # Create a canvas component
    with c1 :
        canvas_result = st_canvas(
            fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
            stroke_width=30,
            stroke_color="#FFFFFF",
            background_color="#000000",
            update_streamlit=True,
            width=280,
            height=280,
            drawing_mode="freedraw",
            key="canvas",
        )

    #Afficher le score du modele
    try :
        def justesse():
            justesse = st.session_state.juste_d/st.session_state.tentatives_d*100
            return justesse

        st.write("Mon modèle a prédit juste à "+str(justesse())+"%")
    except :
        st.write()

    # Do something interesting with the image data and paths
    if canvas_result.image_data is not None:   

        # with st.sidebar:

        res = Image.fromarray(canvas_result.image_data.astype('uint8'),'RGBA')
        res = res.resize((28, 28))
        res = np.array(res)

            # Affichage de l'image compressée
        fig, ax = plt.subplots()
        plt.axis("off")
        ax.imshow(res, cmap=plt.get_cmap('gray'))
        c2.pyplot(fig)

        #Preprocessing
        img = res[:, :, :-1]
        img = img.mean(axis=2)
        my_input = img / 255
        my_input = np.array(my_input).reshape((-1, 28, 28, 1))

        # afficher la sortie cad le numero predit : print(argmax)
        reconstructed_model = tf.keras.models.load_model("models/model")
        my_predict = np.argmax(reconstructed_model.predict(my_input), axis=1)
        
        st.write("Voici le chiffre identifié : "+str(my_predict)[1])

        st.button('Correct',key='raison', on_click=raison)
        st.button('Faux', key="tort", on_click=tort)
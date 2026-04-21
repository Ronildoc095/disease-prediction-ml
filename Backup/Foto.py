import cv2
from PIL import Image
import streamlit as st

def main():
    st.title("Captura de Foto")

    # Inicializa a câmera
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        st.error("Não foi possível abrir a câmera.")
        return

    # Botão para capturar a foto
    if st.button("Capturar Foto"):
        ret, frame = cap.read()

        if ret:
            # Inverte a imagem
            frame = cv2.flip(frame, 1)

            # Salva a imagem na pasta "BD"
            cv2.imwrite("BD/foto.jpg", frame)

            # Exibe a imagem capturada
            st.image(frame, channels="BGR", caption="Foto Capturada")

            # Fecha a câmera
            cap.release()

if __name__ == "__main__":
    main()
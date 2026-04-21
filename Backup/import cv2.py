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

            # Converte BGR para RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Salva a imagem na pasta "BD"
            cv2.imwrite("BD/foto.jpg", frame_rgb)

            # Exibe a imagem capturada
            st.image(frame_rgb, caption="Foto Capturada")

            # Fecha a câmera
            cap.release()
            

if __name__ == "__main__":
    main()
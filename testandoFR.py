import face_recognition as fr
import cv2

def reconhece_face(url_foto):
    foto = fr.load_image_file(url_foto)
    rostos = fr.face_encodings(foto)
    if(len(rostos) > 0):
        return True, rostos
    
    return False, []

def get_rostos():
    rostos_conhecidos = []
    nomes_dos_rostos = []

    elon = reconhece_face("BD/12345.jpg")
    if(elon[0]):
        rostos_conhecidos.append(elon[1][0])
        nomes_dos_rostos.append("Ronildo")

    tony = reconhece_face("facialRecognition-main/Tony.jpg")
    if(tony[0]):
        rostos_conhecidos.append(tony[1][0])
        nomes_dos_rostos.append("Tony")
    
    return rostos_conhecidos, nomes_dos_rostos

desconhecido = reconhece_face("facialRecognition-main/Tony.jpg")
if(desconhecido[0]):
    rosto_desconhecido = desconhecido[1][0]
    rostos_conhecidos, nomes_dos_rostos = get_rostos()
    resultados = fr.compare_faces(rostos_conhecidos, rosto_desconhecido)
    print(resultados)

    for i in range(len(rostos_conhecidos)):
        resultado = resultados[i]
        if(resultado):
            print("Rosto do", nomes_dos_rostos[i], "foi reconhecido")

else:
    print("Nao foi encontrado nenhum rosto")
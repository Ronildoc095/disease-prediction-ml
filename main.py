#Importando as bibliotecas
import pandas as pd
import streamlit as st
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import os
from pathlib import Path
import json
from PIL import Image
from streamlit_lottie import st_lottie, st_lottie_spinner
import plotly.express as px
from xgboost import XGBClassifier
from catboost import CatBoostClassifier
from sklearn.neighbors import KNeighborsClassifier
import cv2
import face_recognition as fr
from testandoFR import reconhece_face, get_rostos
import time



#Configurando o tamanho da pagina
st.set_page_config(layout="wide", initial_sidebar_state="auto", page_title="TCC UNIP", page_icon=":chart_with_upwards_trend:")

#Funçao para carregar os arquivos com animaçoes do Lottie
#@str.experimental_memo

def load_lottiefile(path: str):
    with open(path, 'r', errors='ignore') as f:
        data = json.load(f)
        
    return data




#Logo na Sidebar

st.sidebar.image((Image.open(r"Layout/logo predizer1.png")).resize((950,350)),use_column_width=True)


#validar login e senha
def authenticate(username, password):
    # Verificação das credenciais
    if username == "abc123" and password == "12345" :
        return True
    else:
        return False


#Senha do admin para cadastrar novos pacientes
def admin(username, password):
    # Verificação das credenciais
    if username == "admin" and password == "12345":
        return True
    else:
        return False


def reconhece_face(url_foto):
    foto = fr.load_image_file(url_foto)
    rostos = fr.face_encodings(foto)
    if(len(rostos) > 0):
        return True, rostos
    
    return False, []

#Função de cadastro
def get_rostos():
    rostos_conhecidos = []
    nomes_dos_rostos = []

    elon = reconhece_face("BD/abc123.jpg")
    if(elon[0]):
        rostos_conhecidos.append(elon[1][0])
        nomes_dos_rostos.append("Ronildo")


    
    return rostos_conhecidos, nomes_dos_rostos


def main():
    
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False  

    if not st.session_state.logged_in:  
        

        

        telainicial = st.sidebar.radio('Painel de sleção', ['Inicio','Login','Cadastrar'], horizontal=True)
        if telainicial == 'Inicio':
            # Carregando animação
            st.markdown("<h1 style='text-align: center; font-size: 40px;'>TRABALHO DE CONCLUSÃO DE CURSO</h1>", unsafe_allow_html=True)
            lottie_file = r"Layout/animaçaõ_medico.json"
            lottie_json = load_lottiefile(lottie_file)
            st_lottie(lottie_json, height=850) 


        elif telainicial == 'Login':
            # Entrada do nome de usuário e senha
            st.sidebar.title("Tela de Login")
            username = st.sidebar.text_input("CRM")
            password = st.sidebar.text_input("Senha", type="password")
            
            


            # Botão de login
            if st.sidebar.button("Face Id"):
                     # Carregando animação
                    lottie_file = r"Layout/facial.json"
                    lottie_json = load_lottiefile(lottie_file)
                    st_lottie(lottie_json, height=550) 
                    
                    # Inicializa a câmera
                    cap = cv2.VideoCapture(0)

                    if not cap.isOpened():
                        st.error("Não foi possível abrir a câmera.")
                        return

                    # Botão para capturar a foto
                    
                    ret, frame = cap.read()

                    if ret:
                            # Inverte a imagem
                            frame = cv2.flip(frame, 1)

                            # Converte BGR para RGB
                            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                            # Salva a imagem na pasta "BD"
                            cv2.imwrite(f"BD/foto_id.jpg", frame)

                            # Exibe a imagem capturada
                            st.image(frame_rgb, width=250)
                            
                            # Fecha a câmera
                            cap.release()
                            st.sidebar.info("Face Id coletado")

            if st.sidebar.button('Login'):
                            
                            # Carregando animação
                            lottie_file = r"Layout/animaçaõ_medico.json"
                            lottie_json = load_lottiefile(lottie_file)
                            st_lottie(lottie_json, height=850) 
                            # Verifica o rosto capturado
                            desconhecido = reconhece_face(f"BD/foto_id.jpg") 
                            if desconhecido[0]:
                                rosto_desconhecido = desconhecido[1][0]
                                
                                # Obtém os rostos conhecidos
                                rostos_conhecidos, nomes_dos_rostos = get_rostos()
                                
                                # Compara o rosto capturado com os rostos conhecidos
                                resultados = fr.compare_faces(rostos_conhecidos, rosto_desconhecido)

                                for i in range(len(rostos_conhecidos)):
                                    resultado = resultados[i]
                                    if resultado:
                                        print("Rosto do", nomes_dos_rostos[i], "foi reconhecido")
                                        if authenticate(username, password):
                                            if nomes_dos_rostos[i] == f'{nomes_dos_rostos[i]}':
                                                st.session_state.logged_in = True
                                                st.sidebar.info("Validando Face Id")
                                                st.sidebar.success("Face ID verificado com sucesso")

                                                
                                                


                                                # Atualizar o espaço vazio com uma mensagem de sucesso
                                                
                                                
                                            
                                            else:
                                            
                                                st.sidebar.error("Face ID ou senha inválido")
                                                if st.button("Sair"):
                                                    st.session_state.logged_in = False
                                        else:
                                            st.sidebar.error("CRM ou senha inválido")
                                            if st.button("Sair"):
                                                    st.session_state.logged_in = False
                                    
                            else:
                                st.sidebar.error("Face ID inválido")
                                if st.button("Sair"):
                                    st.session_state.logged_in = False
                    


        else:
                                # Entrada do nome de usuário e senha
                    st.sidebar.title("Tela de Login")
                    username = st.sidebar.text_input("Admin")
                    password = st.sidebar.text_input("Senha", type="password")
                    st.markdown("<h1 style='text-align: center; font-size: 40px;'>CADASTRO DE MÉDICOS</h1>", unsafe_allow_html=True)
                    #Carregando animação
                    lottie_file = r"Layout/regis.json"
                    lottie_json = load_lottiefile(lottie_file)
                    st_lottie(lottie_json, height=450) 
                    st.sidebar.info('Digite o Login do Administrador')
                    st.sidebar.button('Cadastrar')
                   
                    if admin(username, password):
                        st.markdown(
                            """
                            <style>
                            .stTextInput {
                                margin: 0 left;
                                max-width: 500px;
                            }
                            </style>
                            """,
                            unsafe_allow_html=True
                        )
                        name_input = st.text_input('Digite seu nome')
                        cpf_input = st.text_input('Digite seu CRM')
                        email_input = st.text_input('Digite seu E-mail')
                        cell_input = st.text_input('Digite seu Número de Telefone')
                        endereco_input = st.text_input('Digite seu Endereço')
                        senha_input = st.text_input('Digite sua senha:', type='password')
                        confirme_input = st.text_input('Confirme sua senha:', type='password')
                        
                        

                        # Inicializa a câmera
                        cap = cv2.VideoCapture(0)

                        if not cap.isOpened():
                            st.error("Não foi possível abrir a câmera.")
                            return

                            # Botão para capturar a foto
                        if st.button("Coletar Face ID"):
                            ret, frame = cap.read()

                            if ret:
                                    # Inverte a imagem
                                frame = cv2.flip(frame, 1)

                                # Converte BGR para RGB
                                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                                    # Salva a imagem na pasta "BD"
                                cv2.imwrite(f"BD/{cpf_input}.jpg", frame)

                                    # Exibe a imagem capturada
                                st.image(frame_rgb, caption=f"{name_input}")

                                    # Fecha a câmera
                                cap.release()

                        if st.button("Salvar"):
                            # Verifica se todos os campos foram preenchidos
                            if name_input != '' and cpf_input != '' and email_input != '' and cell_input != '' and endereco_input != '' and senha_input !='' and confirme_input !='':
                                # Lógica para salvar os dados do médico no banco de dados
                                st.write("Dados salvos com sucesso!")
                                 # Lógica para salvar os dados do médico no banco de dados
                            else:
                                st.write("Por favor, preencha todos os campos.")
                    
                   
    else:
        
                                
                                paginasSeleciondas = st.sidebar.selectbox('Menu', ['Doenças Cardiovasculares','Diabete','AVC','Cancer de Pulmão','Contatos'])

                                if paginasSeleciondas == 'Diabete':
                                    # Título com texto maior
                                    st.markdown("<h1 style='text-align: left; font-size: 40px;'>Predição de Diabete</h1>", unsafe_allow_html=True)
                                    
                                    #teste 
                                    df = pd.read_csv('Base/diabetes.csv')
                                    

                                    #cabeçalho
                                    st.subheader('Informações dos dados')




                                    

                                    #Predição de Diabete

                                    previsores_diabete = df.drop(['Outcome'], axis=1)
                                    alvo_diabete = df['Outcome']

                                    previsores_diabete_train, previsores_diabete_test, alvo_diabete_train, alvo_diabete_test = train_test_split(previsores_diabete, alvo_diabete, test_size=0.3, random_state=0)
                                    #Pregnancies,Glucose,BloodPressure,SkinThickness,Insulin,BMI,DiabetesPedigreeFunction,Age,Outcome
                                    def get_user_data_diabete():
                                        pregnancies = st.sidebar.slider('Gravidez', 0, 15, 1)
                                        glucose = st.sidebar.slider('Glicose', 0,200,110)
                                        blood_pressure = st.sidebar.slider('Pressão Sanguinea', 0,122,72)
                                        skin_thickness = st.sidebar.slider('Espesura da pele', 0, 99, 20)
                                        insulin = st.sidebar.slider('Insulina' ,0,900,30)
                                        bmi = st.sidebar.slider('Indice de massa corporal', 0.0, 70.0, 15.0)
                                        dpf = st.sidebar.slider('Historico familiar', 0.0, 3.0, 0.0)
                                        age = st.sidebar.slider('Idade', 15, 100, 21)



                                        user_data_diabete = {'Pregnancies': pregnancies,
                                                    'Glucose':glucose,
                                                    'BloodPressure': blood_pressure,
                                                    'SkinThickness':skin_thickness,
                                                    'Insulin':insulin,
                                                    'BMI':bmi,
                                                    'DiabetesPedigreeFunction':dpf,
                                                    'Age':age,
                                                    
                                                    }
                                        features = pd.DataFrame(user_data_diabete, index=[0])


                                        return features


                                    user_input_variables = get_user_data_diabete()
                                    
                                    
                                    st.write('\n')
                                    import plotly.graph_objects as go
                                    # Gráfico
                                    values = user_input_variables.values.flatten()  # Converte o DataFrame para uma matriz (array) unidimensional
                                    labels = user_input_variables.columns.tolist()  # Obtém os rótulos das colunas como uma lista

                                    fig = go.Figure(data=go.Scatterpolar(
                                        r=values,
                                        theta=labels,
                                        fill='toself'
                                    ))

                                    fig.update_layout(
                                        polar=dict(
                                            radialaxis=dict(
                                                visible=True,
                                                range=[0, max(values)]
                                            )
                                        )
                                    )

                                    st.plotly_chart(fig)

                                    st.write("Valores inseridos pelo usuário:")
                                    st.write(user_input_variables)
                                    
                                    dtc_diabete =  XGBClassifier(max_depth=2, learning_rate=0.05, n_estimators=250, objective='binary:logistic', random_state=3)
                                    dtc_diabete.fit(previsores_diabete_train, alvo_diabete_train)
                                    
                                    
                                    #Acuracia do modelo
                                
                                    st.markdown("<h2 style='text-align: left; font-size: 20px;'>Acurácia do modelo de Diabete:</h2>", unsafe_allow_html=True)
                                    st.markdown("<h3 style='text-align: left; font-size: 20px;'>XGBClassifier</h3>", unsafe_allow_html=True)
                                    st.write("%.2f%%" %(accuracy_score(alvo_diabete_test, dtc_diabete.predict(previsores_diabete_test))*100))
                                    #Previsao
                                    prediction_diabete = dtc_diabete.predict(user_input_variables)
                                    

                                    if prediction_diabete == 0:
                                        st.markdown("<p style='font-size: 30px;'>Não tem tendencia de ter Diabete</p>", unsafe_allow_html=True)
                                    elif prediction_diabete == 1:
                                        st.markdown("<p style='font-size: 30px;'>Tem tendencia de ter Diabete</p>", unsafe_allow_html=True)
                                    else:
                                        st.markdown("<p style='font-size: 30px;'>Resultado invalido</p>", unsafe_allow_html=True)


                                    #Predição de Doenças Cardio


                                
                                elif  paginasSeleciondas == "Doenças Cardiovasculares":

                                    df2 = pd.read_csv('Base/heart_tratado .csv', delimiter=';')
                                
                                    #df2['Sex'].replace({'M':0, 'F': 1}, inplace=True)
                                    df2['Sex'].replace({'M':0, 'F': 1}, inplace=True)
                                    df2['ChestPainType'].replace({'TA':0, 'ATA': 1, 'NAP':2, 'ASY': 3}, inplace=True)
                                    df2['RestingECG'].replace({'Normal':0, 'ST': 1, 'LVH':2}, inplace=True)
                                    df2['ExerciseAngina'].replace({'N':0, 'Y': 1}, inplace=True)
                                    df2['ST_Slope'].replace({'Up':0, 'Flat': 1, 'Down':2}, inplace=True)


                                    previsore_cardio = df2.drop(['HeartDisease'], axis=1)
                                    alvo_cardio = df2['HeartDisease']
                                    
                                    previsore_cardio_train, previsore_cardio_test, alvo_cardio_train, alvo_cardio_test = train_test_split(previsore_cardio, alvo_cardio, test_size=0.3, random_state=0)
                                    #Age;Sex;ChestPainType;RestingBP;Cholesterol;FastingBS;RestingECG;MaxHR;ExerciseAngina;Oldpeak;ST_Slope;HeartDisease
                                    def get_user_data_cardio():
                                        
                                        Age = st.sidebar.slider('Idade', 10, 100, 21)
                                        sex = st.sidebar.radio('Sexo', ['Feminino', 'Masculino'], index=1,horizontal=True)
                                        if sex == 'Feminino':
                                            Sex = 0
                                        else:
                                            Sex = 1

                                        ChestPainType = st.sidebar.radio('Tipo de dor no peito',['TA', 'ATA', 'NAP','ASY'], index=1,horizontal=True)
                                        if ChestPainType == 'TA':
                                            ChestPainType = 0
                                        elif ChestPainType == 'ATA':
                                            ChestPainType = 1
                                        elif ChestPainType == 'NAP':
                                            ChestPainType = 2
                                        else:
                                            ChestPainType = 3
                                            
                                        RestingBP = st.sidebar.slider('Pressão sanguínea em repouso (mmHg)', 0, 200, 30)
                                        Cholesterol = st.sidebar.slider('Colesterol sérico (mg/dl)', 0, 6000, 200)
                                        FastingBS = st.sidebar.radio('Açúcar no sangue em jejum (mg/dl)', ['Fasting BS < 120 mg/dl (não diabético)','Fasting BS >= 120 mg/dl (diabético)'], index=1)
                                        if FastingBS == 'Fasting BS < 120 mg/dl (não diabético)':
                                            FastingBS = 0
                                        else:
                                            FastingBS =1
                                        RestingECG = st.sidebar.radio('Eletrocardiograma em repouso', ['Normal','ST','LVH'], index=1, horizontal=True)
                                        if RestingECG == 'Normal':
                                            RestingECG = 0
                                        elif RestingECG == 'ST':
                                            RestingECG = 1
                                        else:
                                            RestingECG = 2
                                        MaxHR = st.sidebar.slider('Frequência cardíaca máxima', 60, 215, 15)
                                        ExerciseAngina = st.sidebar.radio('Angina induzida por exercício',  ['Sim','Não'], index=1, horizontal=True)
                                        if ExerciseAngina == 'Sim':
                                            ExerciseAngina = 1
                                        else:
                                            ExerciseAngina = 0
                                        Oldpeak = st.sidebar.slider('Depressão de ST induzida por exercício em relação ao repouso', -30, 100, 21)
                                        ST_Slope = st.sidebar.radio('Inclinação do segmento ST', ['UP','Flat','Down'], index=1, horizontal=True)
                                        if ST_Slope == 'UP':
                                            ST_Slope = 0
                                        elif ST_Slope == 'Flat':
                                            ST_Slope = 1
                                        else:
                                            ST_Slope = 2

                                        user_data_cardio = {
                                                    'Age': Age,
                                                    'Sex': Sex,
                                                    'ChestPainType':ChestPainType,
                                                    'RestingBP': RestingBP,
                                                    'Cholesterol': Cholesterol,
                                                    'FastingBS': FastingBS,
                                                    'RestingECG': RestingECG,
                                                    'MaxHR': MaxHR,
                                                    'ExerciseAngina': ExerciseAngina,
                                                    'Oldpeak': Oldpeak,
                                                    'ST_Slope': ST_Slope
                                                    }

                                        features_cardio = pd.DataFrame(user_data_cardio, index=[0])
                                        return features_cardio

                                    user_input_cardio = get_user_data_cardio()
                                    import plotly.graph_objects as go
                                    # Gráfico
                                    values = user_input_cardio.values.flatten()  # Converte o DataFrame para uma matriz (array) unidimensional
                                    labels = user_input_cardio.columns.tolist()  # Obtém os rótulos das colunas como uma lista

                                    fig = go.Figure(data=go.Scatterpolar(
                                        r=values,
                                        theta=labels,
                                        fill='toself'
                                    ))

                                    fig.update_layout(
                                        polar=dict(
                                            radialaxis=dict(
                                                visible=True,
                                                range=[0, max(values)]
                                            )
                                        )
                                    )
                                    st.markdown("<h1 style='text-align: left; font-size: 40px;'>Predição de Diabete:</h1>", unsafe_allow_html=True)
                                    #cabeçalho
                                    st.subheader('Informações dos dados')
                                    st.plotly_chart(fig)

                                    st.write(user_input_cardio)

                                    dtc_cardio = DecisionTreeClassifier(criterion='entropy', max_depth=3)
                                    dtc_cardio.fit(previsore_cardio_train, alvo_cardio_train)

                                    prediction_cardio = dtc_cardio.predict(user_input_cardio)

                                    # Acurácia do modelo de doenças cardíacas
                                
                                    
                                    
                                    
                                    st.markdown("<h2 style='text-align: left; font-size: 20px;'>Acurácia do modelo de Diabete</h2>", unsafe_allow_html=True)
                                    st.markdown("<h3 style='text-align: left; font-size: 20px;'>DecisionTreeClassifier</h3>", unsafe_allow_html=True)
                                    st.write("%.2f%%" %(accuracy_score(alvo_cardio_test, dtc_cardio.predict(previsore_cardio_test)) * 100))

                                    if prediction_cardio == 0:
                                        st.markdown("<p style='font-size: 30px;'>Não tem tendência de ter Diabete</p>", unsafe_allow_html=True)
                                    elif prediction_cardio == 1:
                                        st.markdown("<p style='font-size: 30px;'>Tem tendência de ter Diabete</p>", unsafe_allow_html=True)
                                    else:
                                        st.markdown("<p style='font-size: 30px;'>Resultado inválido</p>", unsafe_allow_html=True)
                        
                                elif paginasSeleciondas == 'AVC':
                                    #predição de AVC
                                    df3 = pd.read_csv('Base/AVCtratado.csv', delimiter=';')
                                
                                    #df2['Sex'].replace({'M':0, 'F': 1}, inplace=True)
                                    df3['gender'].replace({'Male':0, 'Female': 1, 'Other': 2}, inplace=True)
                                    df3['ever_married'].replace({'No':0, 'Yes': 1}, inplace=True)
                                    df3['work_type'].replace({'Private':0, 'Self-employed': 1, 'Govt_job':2, 'children': 3, 'Never_worked': 4}, inplace=True)
                                    df3['Residence_type'].replace({'Urban':0, 'Rural': 1}, inplace=True)
                                    df3['smoking_status'].replace({'formerly smoked':0, 'never smoked': 1, 'smokes':2, 'Unknown': 3}, inplace=True)
                                    df3['age'] = df3['age'].div(100)
                                    df3['avg_glucose_level'] = df3['avg_glucose_level'].div(100)
                                    df3['bmi'] = df3['bmi'].div(100)
                            
                                    previsore_avc = df3.drop(['stroke','id'], axis=1)
                                    alvo_avc = df3['stroke']
                                    
                                    previsore_avc_train, previsore_avc_test, alvo_avc_train, alvo_avc_test = train_test_split(previsore_avc, alvo_avc, test_size=0.3, random_state=0)
                                    #id;gender;age;hypertension;heart_disease;ever_married;work_type;Residence_type;avg_glucose_level;bmi;smoking_status;stroke
                                    
                                    def get_user_data_avc():
                                        
                                        gender = st.sidebar.radio('Sexo', ['Masculino', 'Feminino','Outros'], index=1,horizontal=True)
                                        if gender == 'Masculino':
                                            gender = 0
                                        elif gender == 'Feminino':
                                            gender = 1
                                        else:
                                            gender = 2
                                        age = st.sidebar.slider('Idade',10,100,20)
                                        hypertension = st.sidebar.radio('Hipertensão',['Sim', 'Não'], index=1,horizontal=True)
                                        if hypertension == 'Não':
                                            hypertension = 0
                                        else:
                                            hypertension = 1
                                        heart_disease = st.sidebar.radio('Doença cardíaca',['Sim', 'Não'], index=1,horizontal=True)
                                        if heart_disease == 'Não':
                                            heart_disease = 0
                                        else:
                                            heart_disease = 1 
                                        ever_married = st.sidebar.radio('Casamento',['Sim', 'Não'], index=1,horizontal=True)
                                        if ever_married == 'Não':
                                            ever_married = 0
                                        else:
                                            ever_married = 1   
                                        work_type = st.sidebar.radio('Tipo de Trabalho', ['Criança','Emprego gov','Nunca Trabalhou','Autônomo'], index=1)
                                        if work_type == 'Criança':
                                            work_type = 3
                                        elif work_type == 'Emprego gov':
                                            work_type = 2
                                        elif work_type == 'Nunca Trabalhou':
                                            work_type = 1
                                        else:
                                            work_type =0
                                        Residence_type = st.sidebar.radio('Tipo de Residencia', ['Rural','Urbano'], index=1, horizontal=True)
                                        if Residence_type == 'Rural':
                                            Residence_type = 1
                                        else:
                                            Residence_type = 0
                                        avg_glucose_level = st.sidebar.slider('Nível médio de glicose no sangue mg/dl ', 0, 200, 15)
                                        bmi = st.sidebar.slider('Índice de massa corporal', 0, 60, 10)
                                        smoking_status = st.sidebar.radio('Status de Fumante',  ['Já foi fumante','Nunca fumou','Fuma', 'Desconhecido'], index=1)
                                        if smoking_status == 'Já foi fumante':
                                            smoking_status = 0
                                        elif smoking_status == 'Nunca fumou':
                                            smoking_status = 1
                                        elif smoking_status == 'Fuma':
                                            smoking_status = 2      
                                        else:
                                            smoking_status = 3
                                        
                                        #id;gender;age;hypertension;heart_disease;ever_married;work_type;Residence_type;avg_glucose_level;bmi;smoking_status
                                        user_data_avc = {
                                                    'gender': gender,
                                                    'age': age,
                                                    'hypertension':hypertension,
                                                    'heart_disease': heart_disease,
                                                    'ever_married': ever_married,
                                                    'work_type': work_type,
                                                    'Residence_type': Residence_type,
                                                    'avg_glucose_level':avg_glucose_level,
                                                    'bmi': bmi,
                                                    'smoking_status':smoking_status
                                                    
                                                    }

                                        features_avc = pd.DataFrame(user_data_avc, index=[0])
                                        return features_avc

                                    user_input_avc = get_user_data_avc()
                                    import plotly.graph_objects as go
                                    # Gráfico
                                    values = user_input_avc.values.flatten()  # Converte o DataFrame para uma matriz (array) unidimensional
                                    labels = user_input_avc.columns.tolist()  # Obtém os rótulos das colunas como uma lista

                                    fig = go.Figure(data=go.Scatterpolar(
                                        r=values,
                                        theta=labels,
                                        fill='toself'
                                    ))

                                    fig.update_layout(
                                        polar=dict(
                                            radialaxis=dict(
                                                visible=True,
                                                range=[0, max(values)]
                                            )
                                        )
                                    )
                                    st.markdown("<h1 style='text-align: left; font-size: 40px;'>Predição de AVC:</h1>", unsafe_allow_html=True)
                                    
                                    #cabeçalho
                                    st.subheader('Informações dos dados')

                                    st.plotly_chart(fig)
                                    st.write(user_input_avc)
                                    dtc_avc = KNeighborsClassifier(n_neighbors=5, metric='minkowski', p=2)
                                    dtc_avc.fit(previsore_avc_train, alvo_avc_train)
                                    

                                    prediction_avc = dtc_avc.predict(user_input_avc)

                                    # Acurácia do modelo de doenças cardíacas
                                
                                    
                                    
                                    st.markdown("<h2 style='text-align: left; font-size: 20px;'>Acurácia do modelo de AVC</h2>", unsafe_allow_html=True)
                                    st.markdown("<h3 style='text-align: left; font-size: 20px;'>KNeighborsClassifier (KNN)</h3>", unsafe_allow_html=True)
                                    st.write("%.2f%%" %(accuracy_score(alvo_avc_test, dtc_avc.predict(previsore_avc_test)) * 100))

                                    if prediction_avc == 0:
                                        st.markdown("<p style='font-size: 30px;'>Não tem tendência de ter AVC</p>", unsafe_allow_html=True)
                                    elif prediction_avc == 1:
                                        st.markdown("<p style='font-size: 30px;'>Tem tendência de ter AVC</p>", unsafe_allow_html=True)
                                    else:
                                        st.markdown("<p style='font-size: 30px;'>Resultado inválido</p>", unsafe_allow_html=True)

                                    
                                # Criar espaço vazio no canto superior direito

                                elif paginasSeleciondas == 'Cancer de Pulmão':

                                    #predição de AVC
                                    df4 = pd.read_csv('Base/Cancer_Pulmao_Tratado.csv', delimiter=';')
                                    
                                    
                                    df4['LUNG_CANCER'].replace({'YES':1, 'NO': 0}, inplace=True)
                                    df4['GENDER'].replace({'M':1, 'F': 0}, inplace=True)
                            
                                    previsore_pulmao = df4.drop(['LUNG_CANCER'], axis=1)
                                    alvo_pulmao = df4['LUNG_CANCER']
                                    
                                    previsore_pulmao_train, previsore_pulmao_test, alvo_pulmao_train, alvo_pulmao_test = train_test_split(previsore_pulmao, alvo_pulmao, test_size=0.3, random_state=0)
                                    
                                                    #GENDER;AGE;SMOKING;YELLOW_FINGERS;ANXIETY;PEER_PRESSURE;CHRONIC DISEASE;FATIGUE 
                                    # ;ALLERGY ;WHEEZING;ALCOHOL CONSUMING;COUGHING;SHORTNESS OF BREATH;SWALLOWING DIFFICULTY;CHEST PAIN;LUNG_CANCER
                                    def get_user_data_pulmao():
                                        
                                        GENDER = st.sidebar.radio('Sexo', ['Masculino', 'Feminino'], index=1,horizontal=True)
                                        if GENDER == 'Masculino':
                                            GENDER = 1
                                        else:
                                            GENDER = 2

                                        AGE = st.sidebar.slider('Idade',10,100,15)

                                        SMOKING = st.sidebar.radio('Hábito de consumir produtos de tabaco', ['Sim', 'Não'], index=1,horizontal=True)
                                        if SMOKING == 'Sim':
                                            SMOKING  = 1
                                        else:
                                            SMOKING = 2

                                        YELLOW_FINGERS= st.sidebar.radio('Descoloração dos dedos devido ao tabagismo', ['Sim', 'Não'], index=1,horizontal=True)
                                        if YELLOW_FINGERS == 'Sim':
                                            YELLOW_FINGERS  = 1
                                        else:
                                            YELLOW_FINGERS = 2

                                        ANXIETY= st.sidebar.radio('Sentimentos de preocupação e nervosismo', ['Sim', 'Não'], index=1,horizontal=True)
                                        if ANXIETY == 'Sim':
                                            ANXIETY = 1
                                        else:
                                            ANXIETY = 2
                                        
                                        PEER_PRESSURE= st.sidebar.radio('Influência social para se conformar', ['Sim', 'Não'], index=1,horizontal=True)
                                        if PEER_PRESSURE == 'Sim':
                                            PEER_PRESSURE  = 1
                                        else:
                                            PEER_PRESSURE = 2
                                        
                                        CHRONICDISEASE= st.sidebar.radio('Condição médica de longa duração', ['Sim', 'Não'], index=1,horizontal=True)
                                        if  CHRONICDISEASE== 'Sim':
                                            CHRONICDISEASE  = 1
                                        else:
                                            CHRONICDISEASE = 2
                                        
                                        FATIGUE= st.sidebar.radio('Sensação de cansaço extremo', ['Sim', 'Não'], index=1,horizontal=True)
                                        if FATIGUE == 'Sim':
                                            FATIGUE = 1
                                        else:
                                            FATIGUE = 2
                                        
                                        ALLERGY= st.sidebar.radio('Reação do sistema imunológico a substâncias', ['Sim', 'Não'], index=1,horizontal=True)
                                        if  ALLERGY== 'Sim':
                                            ALLERGY = 1
                                        else:
                                            ALLERGY = 2
                                        
                                        WHEEZING= st.sidebar.radio('Som agudo ao respirar, frequentemente associado a problemas respiratórios.', ['Sim', 'Não'], index=1,horizontal=True)
                                        if WHEEZING == 'Sim':
                                            WHEEZING = 1
                                        else:
                                            WHEEZING = 2
                                        
                                        ALCOHOLCONSUMING= st.sidebar.radio('Ingestão de bebidas alcoólicas', ['Sim', 'Não'], index=1,horizontal=True)
                                        if ALCOHOLCONSUMING == 'Sim':
                                            ALCOHOLCONSUMING = 1
                                        else:
                                            ALCOHOLCONSUMING = 2
                                        
                                        COUGHING= st.sidebar.radio('Expulsão súbita de ar dos pulmões', ['Sim', 'Não'], index=1,horizontal=True)
                                        if COUGHING == 'Sim':
                                            COUGHING  = 1
                                        else:
                                            COUGHING = 2
                                        
                                        SHORTNESSOFBREATH= st.sidebar.radio('Dificuldade em respirar plenamente', ['Sim', 'Não'], index=1,horizontal=True)
                                        if  SHORTNESSOFBREATH== 'Sim':
                                            SHORTNESSOFBREATH= 1
                                        else:
                                            SHORTNESSOFBREATH = 2

                                        SWALLOWINGDIFFICULTY= st.sidebar.radio('Sensação de dificuldade ao engolir alimentos ou líquidos', ['Sim', 'Não'], index=1,horizontal=True)
                                        if SWALLOWINGDIFFICULTY == 'Sim':
                                            SWALLOWINGDIFFICULTY  = 1
                                        else:
                                            SWALLOWINGDIFFICULTY = 2
                                        
                                        CHESTPAIN= st.sidebar.radio('Desconforto ou dor na região torácica', ['Sim', 'Não'], index=1,horizontal=True)
                                        if CHESTPAIN == 'Sim':
                                            CHESTPAIN = 1
                                        else:
                                            CHESTPAIN = 2            


                                        

                                        
                                                    #GENDER;AGE;SMOKING;YELLOW_FINGERS;ANXIETY;PEER_PRESSURE;CHRONIC DISEASE;FATIGUE 
                                    # ;ALLERGY ;WHEEZING;ALCOHOL CONSUMING;COUGHING;SHORTNESS OF BREATH;SWALLOWING DIFFICULTY;CHEST PAIN;LUNG_CANCER
                                        user_data_avc = {
                                                    'GENDER': GENDER,
                                                    'AGE': AGE,
                                                    'SMOKING':SMOKING,
                                                    'YELLOW_FINGERS': YELLOW_FINGERS,
                                                    'ANXIETY': ANXIETY,
                                                    'PEER_PRESSURE': PEER_PRESSURE,
                                                    'CHRONIC DISEASE': CHRONICDISEASE,
                                                    'FATIGUE ':FATIGUE,
                                                    'ALLERGY ':ALLERGY,
                                                    'WHEEZING': WHEEZING,
                                                    'ALCOHOL CONSUMING':ALCOHOLCONSUMING,
                                                    'COUGHING':COUGHING,
                                                    'SHORTNESS OF BREATH':SHORTNESSOFBREATH,
                                                    'SWALLOWING DIFFICULTY':SWALLOWINGDIFFICULTY,
                                                    'CHEST PAIN':CHESTPAIN
                                                    }

                                        features_pulmao = pd.DataFrame(user_data_avc, index=[0])
                                        return features_pulmao

                                    user_input_pulmao = get_user_data_pulmao()
                                    import plotly.graph_objects as go
                                    # Gráfico
                                    values = user_input_pulmao.values.flatten()  # Converte o DataFrame para uma matriz (array) unidimensional
                                    labels = user_input_pulmao.columns.tolist()  # Obtém os rótulos das colunas como uma lista

                                    fig = go.Figure(data=go.Scatterpolar(
                                        r=values,
                                        theta=labels,
                                        fill='toself'
                                    ))

                                    fig.update_layout(
                                        polar=dict(
                                            radialaxis=dict(
                                                visible=True,
                                                range=[0, max(values)]
                                            )
                                        )
                                    )
                                    st.markdown("<h1 style='text-align: left; font-size: 40px;'>Predição de Cancer de Pulmão:</h1>", unsafe_allow_html=True)
                                    
                                    #cabeçalho
                                    st.subheader('Informações dos dados')

                                    st.plotly_chart(fig)
                                    st.write(user_input_pulmao)
                                    dtc_pulmao = CatBoostClassifier(task_type= 'CPU', iterations =120,  learning_rate=0.1, depth= 8, random_state=5, eval_metric ="Accuracy")
                                    dtc_pulmao.fit(previsore_pulmao_train, alvo_pulmao_train)
                                    

                                    prediction_pulmao = dtc_pulmao.predict(user_input_pulmao)

                                    # Acurácia do modelo de doenças cardíacas
                                
                                    
                                    
                                    st.markdown("<h2 style='text-align: left; font-size: 20px;'>Acurácia do modelo de Cancer de Pulmão</h2>", unsafe_allow_html=True)
                                    st.markdown("<h3 style='text-align: left; font-size: 20px;'>CatBoostClassifier</h3>", unsafe_allow_html=True)
                                    st.write("%.2f%%" %(accuracy_score(alvo_pulmao_test, dtc_pulmao.predict(previsore_pulmao_test)) * 100))

                                    if prediction_pulmao == 0:
                                        st.markdown("<p style='font-size: 30px;'>Não tem tendência de ter Cancer de Pulmão</p>", unsafe_allow_html=True)
                                    elif prediction_pulmao == 1:
                                        st.markdown("<p style='font-size: 30px;'>Tem tendência de ter Cancer de Pulmão</p>", unsafe_allow_html=True)
                                    else:
                                        st.markdown("<p style='font-size: 30px;'>Resultado inválido</p>", unsafe_allow_html=True)

                                    
                                elif paginasSeleciondas == 'Contatos':

                                
                                    st.markdown("<h1 style='text-align: left; font-size: 40px;'>Agradecimentos</h1>", unsafe_allow_html=True)
                                    st.markdown('''<h2 style='text-align: left; font-size: 30px;'>Gostaria de expressar minha sincera gratidão a
                                                todos os membros do grupo que trabalharam em conjunto no nosso Trabalho de Conclusão de Curso 
                                                (TCC). Foi uma jornada desafiadora, mas também repleta de aprendizado e conquistas, e isso não 
                                                teria sido possível sem a dedicação e colaboração de cada um de vocês.Por fim, quero agradecer 
                                                a todos os membros do grupo por acreditarem no nosso trabalho e por se empenharem para torná-lo 
                                                um sucesso. Foi uma experiência enriquecedora e estou orgulhoso do trabalho que realizamos juntos. 
                                                Obrigado por fazerem parte desta jornada e por contribuírem para o nosso TCC.</h2>''', unsafe_allow_html=True)
                                    
                                    st.markdown("<h2 style='text-align: left; font-size: 20px;'>Anne Ronildo Rodrigo Thiago Ulisses</h2>", unsafe_allow_html=True)
                                    st.markdown("<h1 style='text-align: left; font-size: 40px;'>Informações e Contato</h1>", unsafe_allow_html=True)
                                    st.markdown("<h2 style='text-align: left; font-size: 20px;'>Eng.comput.2023@gmail.com</h2>", unsafe_allow_html=True)
                                                        # Título com texto maior
                                    lottie_file = r"Layout/agradecimento.json"
                                    lottie_json = load_lottiefile(lottie_file)
                                    st_lottie(lottie_json, height=350) 
                            
                                if st.button("Sair"):
                                    st.session_state.logged_in = False





if __name__ == "__main__":
    main()

#Importando as bibliotecas
import pandas as pd
import streamlit as st
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
import pickle

# Aumentar a largura do site para 1000 pixels
st.set_page_config(layout="wide", initial_sidebar_state="collapsed", page_title="TCC UNIP", page_icon=":chart_with_upwards_trend:")

# Título com texto maior
st.markdown("<h1 style='text-align: center; font-size: 40px;'>TRABALHO DE CONCLUSÃO DE CURSO\n\n\n\n</h1>", unsafe_allow_html=True)



# Adicionando uma imagem
image = 'PREDIZER.jpg'  # Substitua pelo nome do seu arquivo de imagem
st.image(image, caption= 'Aqui pode por uma legenda' , use_column_width=True )
# Título com texto maior
st.markdown("<h1 style='text-align: center; font-size: 40px;'>OQUE SÃO DCNT?\n\n\n\n</h1>", unsafe_allow_html=True)
# Caminho do vídeo
video_path = 'doenças.mp4'  # Substitua pelo caminho do seu vídeo MOV

# Exibindo o vídeo
st.video(video_path)




# Descrição com texto maior
st.markdown("<p style='font-size: 30px;'>PREDIÇÃO DE DOENÇAS CRÔNICAS NÃO TRANSMISSÍVEIS</p>", unsafe_allow_html=True)

# Algo a ser adicionado com texto maior
st.markdown("""<p style='font-size: 20px;'>DCNT é a sigla para 'Doenças Crônicas Não Transmissíveis'. São doenças de longa duração e progressão lenta, 
            que geralmente não são causadas por agentes infecciosos e não são transmitidas de pessoa para pessoa. As DCNTs são responsáveis por uma 
            grande carga de morbidade e mortalidade em todo o mundo.</p>""", unsafe_allow_html=True)


#Dataset
#teste 
df = pd.read_csv("C:/Users/Ronildo/OneDrive/Área de Trabalho/heart_tratado .csv")

#cabeçalho
st.subheader('Informações dos dados')

#Nome do usuario
name_input = st.sidebar.text_input ('Digite seu nome')
cpf_input = st.sidebar.text_input ('Digite seu CPF')
idade_input = st.sidebar.text_input ('Digite sua Idade')
cell_input = st.sidebar.text_input ('Digite seu Numero de Telefone')
endereco_input = st.sidebar.text_input ('Digite seu Endereço')

st.write('Paciente:', name_input)
st.write('CPF:', cpf_input)
st.write('Idade:', idade_input)
st.write('Celular:', cell_input)
st.write('Endereço:', endereco_input)

                 
#Separa dados em treinamento e teste
#X_train, X_teste, Y_train, Y_teste = train_test_split(x, y, teste_size=.2, random_state=42)



def get_user_data():
    Age = st.sidebar.slider('Idade', 0, 130, 1)
    Chest_Pain_Type = st.sidebar.radio('Tipo de dor no peito', ['Angina típica', 'Angina atípica', 'Dor não anginosa','Assintomático'], index=0, horizontal=True)
    Sex = st.sidebar.radio('Sexo', ['Masculino', 'Feminino'], index=0, horizontal=True)
    Resting_BP = st.sidebar.slider('Pressão sanguínea em repouso (mmHg)', 0, 200, 10)
    Cholesterol = st.sidebar.slider('colesterol sérico (mg/dl)', 0, 200, 10)
    Fasting_BS = st.sidebar.radio('Açúcar no sangue em jejum (mg/dl)' ,['Fasting BS < 120 mg/dl (não diabético)','Fasting BS >= 120 mg/dl (diabético)'], index=0, horizontal=True)
    Resting_ECG = st.sidebar.radio('Eletrocardiograma em repouso', ['Normal', 'Anormalidade da onda','Hipertrofia ventricular esquerda'], index=0, horizontal=True)
    Max_HR = st.sidebar.slider('frequência cardíaca máxima', 0, 200, 10)
    Exercise_Angina = st.sidebar.radio('Angina induzida por exercício', ['Sim', 'Não'], index=0, horizontal=True)
    Old_Peak = st.sidebar.slider('Depressão de ST induzida por exercício em relação ao repouso', 0, 200, 10)
    ST_Slope = st.sidebar.radio('Inclinação do segmento ST',['UP', 'Flat','Down'], index=0, horizontal=True)


    user_data = {'Idade': Age,
                 'Tipo de dor no peito': Chest_Pain_Type,
                 'Sexo':Sex,
                 'Pressão sanguínea em repouso (mmHg)':Resting_BP,
                 'colesterol sérico (mg/dl)':Cholesterol,
                 'Açúcar no sangue em jejum (mg/dl)':Fasting_BS,
                 'Eletrocardiograma em repouso':Resting_ECG,
                 'frequência cardíaca máxima':Max_HR,
                 'Angina induzida por exercício':Exercise_Angina,
                 'Depressão de ST induzida por exercício em relação ao repouso':Old_Peak,
                 'Inclinação do segmento ST':ST_Slope
                 }

    

    
    


    features = pd.DataFrame(user_data, index=[0])

    return features

user_input_variables = get_user_data()

#Grafico
graf = st.bar_chart(user_input_variables)

st.subheader('Dados do usuário')
st.write(user_input_variables)

st.subheader("\n\n\n\n\n\n\n\n\n\nPredição se o paciente tem doença crônica não transmissíveis")

# Carregando os modelos treinados
heart_disease_model = pickle.load(open('heart_disease_model.pkl', 'rb'))
diabetes_model = pickle.load(open('diabetes_model.pkl', 'rb'))
stroke_model = pickle.load(open('stroke_model.pkl', 'rb'))
lung_cancer_model = pickle.load(open('lung_cancer_model.pkl', 'rb'))

# Fazendo previsões para as quatro doenças com base nos dados do usuário
heart_disease_prediction = heart_disease_model.predict(user_input_variables)
diabetes_prediction = diabetes_model.predict(user_input_variables)
stroke_prediction = stroke_model.predict(user_input_variables)
lung_cancer_prediction = lung_cancer_model.predict(user_input_variables)

# Exibindo as previsões
st.subheader('Previsões')
st.write('Doença Cardiovascular:', heart_disease_prediction)
st.write('Diabetes:', diabetes_prediction)
st.write('AVC:', stroke_prediction)
st.write('Câncer de Pulmão:', lung_cancer_prediction)
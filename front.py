import streamlit as st
import requests


st.title('Предсказывают выживание Титаника')

api_url = "http://127.0.0.1:8001/predict"


pclass = st.selectbox("Класс пассажира", [1, 2, 3])
sex = st.selectbox("Пол", ["male", "female"])
age = st.number_input("Возраст", min_value=0, max_value=100, value=30)
fare = st.number_input("Стоимость билета", min_value=0.0, value=50.0)
family = st.number_input("Размер семьи", min_value=0, value=1)
embarked = st.selectbox("Порт посадки", ["C", "Q", "S"])


titanic_data = {
        "Pclass": pclass,
        "Sex": sex,
        "Age": age,
        "Fare": fare,
        "FamilySize": family,
        "Embarked": embarked
    }


if st.button("Проверить выживание"):
    try:
        answer = requests.post(api_url, json=titanic_data, timeout=10)

        if answer.status_code == 200:
            result = answer.json()
            st.json(result)

        else:
            st.error(f"Ошибка: {answer.status_code}")

    except requests.exceptions.RequestException:
        st.error("Не удалось подключиться к API")
import io
from typing import Optional
import pandas as pd
import pickle
import requests
import streamlit as st
from app.api.conversations import Conversations
#from app.services.summary_service import continue_conversation, set_openai_api_key
from app.api.conversations import Message as chat_message




def main():
    model=pickle.load(open("D:/COLLEGE/documents/output.pickle",'rb'))
    st.title("Legal Summarizer")

    API_KEY = st.text_input("Type your OPENAI_API_KEY here",type="password", key="api_key",help="You can get api_key at https://platform.openai.com/account/api-keys")
    #set_openai_api_key(API_KEY)


    if "conversations" not in st.session_state:
        st.session_state.conversations = Conversations()

    if "uploaded" not in st.session_state:
        st.session_state.uploaded = False

    pdf_file = st.file_uploader("Upload a PDF file", type="pdf")

    if pdf_file is not None and st.session_state.uploaded is False:
        print("handle_pdf_upload")
        conversations = handle_pdf_upload(pdf_file)
        st.session_state.uploaded = True
        st.session_state.conversations = conversations
    with st.form(key='form_parameters'):
        sepal_length = st.slider('Sepal Length', 4.0, 8.0, 4.0)
        sepal_width = st.slider('Sepal Width', 2.0, 4.5, 2.0)
        petal_length = st.slider('Petal Length', 1.0, 7.0, 1.0)
        petal_width = st.slider('Petal Width', 0.1, 2.5, 0.1)
        st.markdown('---')
        submitted = st.form_submit_button('Predict')
    # Data Inference
    data_inf = {
        'sepal.length': sepal_length,
        'sepal.width': sepal_width,
        'petal.length': petal_length,
        'petal.width': petal_width
    }
    data_inf = pd.DataFrame([data_inf])

        # Predict using Logistic Regression
    y_pred_inf = model.predict(data_inf)
    st.write("pdf summarization" + str(y_pred_inf))

    question = st.text_input("Type your question here")

    if st.button("Ask", key="ask_button"):
        if question:
            print("continue_conversation")
            st.session_state.conversations = continue_conversation(st.session_state.conversations, question)

    if st.button("Clear All cache", key="clear_cache"):
        st.cache_resource.clear()
        st.session_state.conversations = Conversations()


    if "conversations" in st.session_state:
        for i, message in enumerate(reversed(st.session_state.conversations.get_messages())):
            if message.role == "assistant":
                chat_message(message.content, key=str(i))
            else:
                chat_message(message.content, key=str(i)+"_user", is_user=True)

if __name__ == "__main__":
    main()

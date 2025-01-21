import streamlit as st

import config
import utils
import chat
import vectorstore


def run():
    st.title("RAG 0800")

    expander = st.expander("O que é?")
    expander.write('''
        Chatbot simples baeado em LLM/RAG, implementado com LangChain e outras tecnologias Open Source / gratuitas.
        Adicione seus documentos em PDF no diretório `./data/input/`, click em processar e faça perguntas relacionadas.
    ''')


    if "process_success" not in st.session_state:
        st.session_state.process_success = False

    if st.sidebar.button("Processar documentos de entrada") or st.session_state.process_success:
        with st.spinner("Processando documentos de entrada..."):
            vectorstore.run(config.input_folder_path, config.output_folder_path)

            st.session_state.process_success = True

            chat_ins = chat.Chat(
                store_folder_path=config.output_folder_path,
                db_path=config.db_path,
                chat_template=config.chat_template,
            )

        if "messages" not in st.session_state:
            st.session_state.messages = []

        # transfer message history from database to streamlit session
        for row in chat_ins.get_history():
            st.session_state.messages.append({"role": "user", "content": row[1]})
            st.session_state.messages.append({"role": "assistant", "content": row[2]})

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Faça uma pergunta?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Gerando resposta..."):
                    qa_instance = chat_ins.ask(st.session_state.messages[-1]["content"])
                    response = st.write(qa_instance.answer)

                    chat_ins.log(qa_instance)

if __name__ == "__main__":    
    run()

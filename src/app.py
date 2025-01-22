import os

import streamlit as st

import config
import utils
import chat
import vectorstore


def run():
    st.title("RAG 0800")

    expander1 = st.expander("O que é?")
    expander1.write(
        """
        Chatbot simples baeado em LLM/RAG, implementado com LangChain e outras tecnologias Open Source / gratuitas.
        Faça upload de documentos no menu ao lado, click em processar e, em seguida, pergunte o que quiser sobre os documentos.

        https://github.com/fernandojunior/rag0800
        """
    )

    expander1 = st.expander("Prompt Template")
    expander1.markdown(f"```{config.chat_template}```")

    if "process_success" not in st.session_state:
        st.session_state.process_success = False

    if "chat_ins" not in st.session_state:
        st.session_state.chat_ins = None

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "input_pdfs" not in st.session_state:
        st.session_state.input_pdfs = []

    uploaded_pdf = st.sidebar.file_uploader(
        "Upload PDF", type="pdf", label_visibility="hidden"
    )

    if uploaded_pdf is not None:
        with open(os.path.join(config.input_folder_path, uploaded_pdf.name), "wb") as f:
            f.write(uploaded_pdf.getbuffer())

    st.session_state.input_pdfs = {
        f: st.sidebar.checkbox(f.split("/")[-1])
        for f in utils.list_pdfs(config.input_folder_path)
    }

    if st.sidebar.button(
        "❌ Remover documentos", disabled=not any(st.session_state.input_pdfs.values())
    ):
        for file_path, check in st.session_state.input_pdfs.items():
            if check:
                os.remove(file_path)

        removed_files = [f for f, c in st.session_state.input_pdfs.items() if c]

        st.session_state.input_pdfs = {
            f: c
            for f, c in st.session_state.input_pdfs.items()
            if f not in removed_files
        }

        st.write("<script>location.reload()</script>", unsafe_allow_html=True)
        st.rerun()

    if st.sidebar.button(
        "🔄 Processar documentos", disabled=not any(st.session_state.input_pdfs.values())
    ):
        with st.spinner("Processando documentos de entrada..."):
            _input_files = [f for f, c in st.session_state.input_pdfs.items() if c]

            vectorstore.run(_input_files, config.output_folder_path)

            st.session_state.chat_ins = chat.Chat(
                store_folder_path=config.output_folder_path,
                db_path=config.db_path,
                chat_template=config.chat_template,
            )

            st.session_state.process_success = True

    if st.session_state.process_success:
        # transfer message history from database to streamlit session
        for row in st.session_state.chat_ins.get_history():
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
                    qa_instance = st.session_state.chat_ins.ask(
                        st.session_state.messages[-1]["content"]
                    )
                    st.write(qa_instance.answer)

                    st.session_state.chat_ins.log(qa_instance)


if __name__ == "__main__":
    run()

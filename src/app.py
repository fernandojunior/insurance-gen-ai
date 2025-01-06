import streamlit as st

import config
import utils
import chat
import vectorstore


def run():
    chat_ins = None

    if "user_question" not in st.session_state:
        st.session_state.user_question = ""
    
    if "feedback" not in st.session_state:
        st.session_state.feedback = ""

    if "answer_sucess" not in st.session_state:
        st.session_state.answer_sucess = False

    if "qa_instance" not in st.session_state:
        st.session_state.qa_instance = None

    with st.spinner("Loading and processing documents / embeddings..."):
        index_files = utils.list_files_by_datetime(config.index_folder_path)
        # st.write(index_files)

        if len(index_files) == 1:
            vectorstore.run()

        chat_ins = chat.Chat(
            index_folder_path=config.index_folder_path,
            chat_template=config.chat_template,
        )

        st.success("Documents loaded and chain initialized!")

    st.subheader("Q&A History")
    qa_history = chat_ins.get_history()

    for row in qa_history:
        st.write(row)

    st.subheader("Global: Feedback")
    st.write(chat_ins.analyze_feedback())

    if st.session_state.user_question == "" and st.session_state.feedback == "":
        # st.session_state.user_question = st.text_input("Sua perguta:", key="user_question")
        st.session_state.user_question = st.text_input("Sua perguta", st.session_state.user_question)

        if st.button("Enviar Pergunta") and st.session_state.user_question:
            with st.spinner("Generating answer..."):
                st.session_state.qa_instance = chat_ins.ask(st.session_state.user_question)

                st.session_state.answer_sucess = True

                if st.button("OK"):
                    st.write("Button clicked!")

    if st.session_state.answer_sucess:
        st.success(st.session_state.qa_instance.answer)

    if st.session_state.user_question != "" and st.session_state.feedback == "" and st.session_state.answer_sucess:
        st.session_state.feedback = st.text_input("Feedback (sim/não/outro):", st.session_state.feedback)

        if st.button("Enviar Feedback") and st.session_state.feedback:
            chat_ins.set_feedback(st.session_state.qa_instance, st.session_state.feedback)
            chat_ins.log(st.session_state.qa_instance)

            st.session_state.qa_instance = None
            st.session_state.user_question = ""
            st.session_state.feedback = ""
            st.session_state.answer_sucess = False

            if st.button("OK"):
                st.write("Button clicked!")


if __name__ == "__main__":
    
    run()

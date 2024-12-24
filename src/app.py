import streamlit as st

import config
import utils
import chat
import vectorstore


def run():
    chat_ins = None

    if "user_question" not in st.session_state:
        st.session_state.user_question = ""
    
    if "feedback_input" not in st.session_state:
        st.session_state.feedback_input = ""

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

    # Chat Interface
    user_question = st.text_input("Sua perguta:", key="user_question")

    if st.button("Enviar Pergunta") and user_question:
        with st.spinner("Generating answer..."):
            qa_instance = chat_ins.ask(user_question)

            st.success(qa_instance.answer)

            feedback_input = st.text_input("Feedback (sim/não/outro):", key="feedback_input")

            if st.button("Enviar Feedback") and feedback_input:
                chat_ins.set_feedback(qa_instance, feedback_input)
                chat_ins.log(qa_instance)

if __name__ == "__main__":
    
    run()

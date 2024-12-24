import streamlit as st

import config
import utils
import chat
import vectorstore


def run():
    with st.spinner("Loading and processing documents / embeddings..."):

        index_files = utils.list_files_by_datetime(config.index_folder_path)
        st.write("vai")
        st.write(index_files)

        if len(index_files) == 1:
            vectorstore.run()

        st.session_state["chat"] = chat.Chat(
            index_folder_path=config.index_folder_path,
            chat_template=config.chat_template,
        )

        st.success("Documents loaded and chain initialized!")

    # Chat Interface
    user_input = st.text_input("Sua perguta:")

    if st.button("Enviar Pergunta") and user_input:
        with st.spinner("Generating answer..."):
            try:
                qa_instance = st.session_state["chat"].ask(user_input)

                # Display the answer
                st.success(qa_instance.answer)

                feedback_input = st.text_input("Feedback (sim/não/outro):")

                if st.button("Enviar Feedback") and feedback_input:
                    st.session_state["chat"].set_feedback(qa_instance, feedback_input)
                    st.session_state["chat"].log(qa_instance)
            except Exception as e:
                st.error(f"An error occurred: {e}")

    # Display Q&A history
    st.subheader("Q&A History")
    qa_history = st.session_state["chat"].get_history()

    for row in qa_history:
        question, answer, feedback = row
        st.write(f"**Q:** {question}")
        st.write(f"**A:** {answer}")
        st.write(f"**F:** {feedback}")

    st.subheader("Global: Feedback")
    st.write(st.session_state["chat"].analyze_feedback())


if __name__ == "__main__":
    run()

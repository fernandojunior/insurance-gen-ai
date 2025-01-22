input_folder_path = "./data/input"

output_folder_path = "./data/output"

db_path = "./data/database/chatbot_history.db"

chat_template = """
Com base nos dados fornecidos: chat history(delimitado por <hs></hs>)
e context (delimitado por <ctx></ctx>).
Responda à seguinte pergunta da melhor forma: {question}.
-----------
<ctx>
{context}
</ctx>
-----------
<hs>
{chat_history}
</hs>
-----------
"""

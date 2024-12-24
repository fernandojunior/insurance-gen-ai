input_folder_path = "./data/input"

index_folder_path = "./data/output"

chat_template = """
Você é um assistente especializado em seguros.
Com base nos dados fornecidos: chat history(delimitado por <hs></hs>) e context (delimitado por <ctx></ctx>).
Responda à seguinte pergunta de maneira clara e completa: {question}.
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

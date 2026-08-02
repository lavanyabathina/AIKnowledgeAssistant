from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


chat_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are an AI Knowledge Assistant.

            Answer only using the provided context.

            Context:
            {context}
            """
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}")
    ]
)
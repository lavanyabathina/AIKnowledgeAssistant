from langchain_core.messages import HumanMessage, AIMessage
from typing import List
from chat.query_rewrite_prompt import query_rewrite_prompt


def format_chat_history_for_rewrite(chat_history: List) -> str:
    """
    Convert chat history messages to readable text format for LLM
    
    Args:
        chat_history: List of HumanMessage and AIMessage objects
        
    Returns:
        Formatted string representation of chat history
    """
    if not chat_history:
        return "No previous chat history."
    
    formatted = []
    for i, message in enumerate(chat_history):
        if isinstance(message, HumanMessage):
            formatted.append(f"User: {message.content}")
        elif isinstance(message, AIMessage):
            formatted.append(f"Assistant: {message.content}")
    
    return "\n".join(formatted)


def rewrite_query(current_query: str, chat_history: List, llm) -> str:
    """
    Rewrite the user's query using chat history context and the provided LLM
    
    Uses the same LLM instance to enrich the query with:
    - Resolution of pronouns (it, they, this, that)
    - Expansion of abbreviated terms
    - Addition of context from previous exchanges
    
    Args:
        current_query: The current user question
        chat_history: List of previous HumanMessage and AIMessage objects
        llm: The LLM instance to use for rewriting (same as RAG chain)
        
    Returns:
        Rewritten query string enriched with context
    """
    
    try:
        # If no chat history, return original query
        if not chat_history:
            return current_query
        
        # Format chat history for the prompt template
        formatted_history = format_chat_history_for_rewrite(chat_history)
        
        # Use the query_rewrite_prompt template
        # Create the rewrite chain: prompt -> llm
        rewrite_chain = query_rewrite_prompt | llm
        
        # Invoke the chain with formatted inputs
        response = rewrite_chain.invoke({
            "chat_history": formatted_history,
            "current_query": current_query
        })
        
        # Extract the rewritten query from response
        # Handle both string and AIMessage responses
        if isinstance(response, AIMessage):
            rewritten_query = response.content.strip()
        else:
            rewritten_query = str(response).strip()
        
        # Handle edge cases where LLM might add extra text
        # Clean up common extra text patterns
        lines = rewritten_query.split('\n')
        rewritten_query = lines[0].strip()  # Take first line
        
        # Remove common prefixes if present
        prefixes_to_remove = ["rewritten query:", "rewritten:", "query:", "refined query:"]
        query_lower = rewritten_query.lower()
        for prefix in prefixes_to_remove:
            if query_lower.startswith(prefix):
                rewritten_query = rewritten_query[len(prefix):].strip()
        
        if rewritten_query and len(rewritten_query) > 5:
            return rewritten_query
        else:
            return current_query
            
    except Exception as e:
        print(f"Error during query rewriting: {str(e)}. Using original query.")
        return current_query

# AI Knowledge Assistant

A Retrieval-Augmented Generation (RAG) chatbot that leverages LLMs to answer questions based on knowledge bases from web sources and local documentation. The system supports multiple LLM providers and integrates with DeepEval for comprehensive evaluation metrics.

## Features

- **Multi-Source Data Loading**: Fetch documentation from web sources (using web crawlers) and load local documents
- **Document Processing**: Chunk documents with configurable size and overlap
- **Vector Embeddings**: Generate embeddings using HuggingFace models
- **Vector Database**: Store and retrieve embeddings using ChromaDB
- **RAG Pipeline**: Retrieval-Augmented Generation for contextual question answering
- **Query Rewriting**: Intelligently rewrite queries based on conversation history and context (e.g., resolving pronouns like "it" to previous topics)
- **Multi-LLM Support**: Claude, Gemini, OpenAI, and Groq
- **DeepEval Integration**: Comprehensive evaluation metrics including:
  - Answer Relevancy
  - Contextual Precision & Recall
  - Conversation Completeness
  - Faithfulness
  - Goal Accuracy
  - Knowledge Retention
  - Role Adherence
  - Topic Adherence
  - Turn Faithfulness
  - Turn Relevancy
- **Chat Session Management**: Maintain conversation history across multiple turns

## Prerequisites

### System Requirements
- Python 3.8+
- Windows, macOS, or Linux
- 8GB+ RAM (recommended for LLM operations)

### Required Software
- Python package manager (pip)
- Git (optional)

### Required API Keys
Set up these environment variables in a `.env` file:
```
# LLM Providers (choose at least one based on your config)
ANTHROPIC_API_KEY=your_anthropic_api_key
GOOGLE_API_KEY=your_google_api_key
OPENAI_API_KEY=your_openai_api_key
GROQ_API_KEY=your_groq_api_key
```

## Installation

### Step 1: Clone or Download the Project
```bash
cd c:\Users\Admin\Desktop\Lavanya\AILearning\AIKnowledgeAssistant
```

### Step 2: Create a Virtual Environment (Recommended)
```bash
python -m venv venv
```

Activate the virtual environment:
- **Windows**: `venv\Scripts\activate`
- **macOS/Linux**: `source venv/bin/activate`

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

**Critical Dependencies** (required for core functionality):
- **python-dotenv**: Loads environment variables from `.env` file (used in main.py and all evaluation scripts)
- **PyYAML**: Parses YAML configuration files (used by loaders/load_config.py)

These two are essential - without them, the application will fail to start.

### Step 4: Set Up Environment Variables
Create a `.env` file in the project root directory:
```
ANTHROPIC_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
GROQ_API_KEY=your_key_here
```

**Optional**: For DeepEval's cache functionality on Windows, ensure pywin32 is installed:
```bash
python -m pip install --upgrade pywin32
python Scripts/pywin32_postinstall.py -install
```

## Configuration

The project uses YAML configuration files located in the `config/` directory:

### `application_config.yaml`
Controls the application pipeline:
```yaml
application:
  dataset_generation:
    enabled: false  # Set to true to generate dataset
  rebuild_vector_db:
    enabled: false  # Set to true to delete existing vector DB
  vector_indexing:
    enabled: false  # Set to true to build vector index
  chat:
    enabled: true   # Set to true to enable chat

# Chunking settings for document processing
chunking:
  chunk_size: 1000
  chunk_overlap: 200

# Embedding model configuration
embedding:
  provider: huggingface
  model: sentence-transformers/all-MiniLM-L6-v2
  batch_size: 32

# Vector database settings
vector_db:
  type: chroma
  path: ./vectorstore/chroma_db
  collection: knowledge_base

# Retrieval settings
retrieval:
  top_k: 3  # Number of documents to retrieve

# Main LLM configuration for chat
llm:
  provider: claude  # Options: claude, gemini, openai, groq
  model: claude-sonnet-4-6
  temperature: 0

# DeepEval judge LLM configuration (for evaluation metrics)
deepeval_judgellm:
  provider: claude  # Options: claude, gemini, groq
  model: claude-sonnet-4-6
  temperature: 0
```

### `dataset_config.yaml`
Configures data sources:
```yaml
datasets:
  - name: java
    type: web
    path: https://docs.oracle.com/en/java/javase/25/docs/api/
  
  - name: selenium
    type: web
    path: https://www.selenium.dev/documentation/

  - name: playwright
    type: web
    path: https://playwright.dev/docs/intro
  
  - name: python
    type: local
    path: ./localData/pythondocs

source_directory: ./sources
web_source_directory: ./sources/web
local_source_directory: ./sources/local

max_depth: 3
max_pages: 300
output: markdown
```

## Quick Start Guide

### Step 1: Generate Dataset

Enable dataset generation in `config/application_config.yaml`:
```yaml
application:
  dataset_generation:
    enabled: true
```

Run the dataset pipeline:
```bash
python main.py
```

This will:
- Crawl web sources (Java docs, Selenium documentation, Playwright docs)
- Load local documents from `localData/`
- Save documents as markdown files in `sources/` directory

**Duration**: 5-30 minutes depending on data source size and `max_pages` setting

### Step 2: Build Vector Index

After dataset generation, enable vector indexing in `config/application_config.yaml`:
```yaml
application:
  dataset_generation:
    enabled: false
  rebuild_vector_db:
    enabled: true  # Enable to clear existing DB (optional)
  vector_indexing:
    enabled: true
  chat:
    enabled: false
```

Run the vector pipeline:
```bash
python main.py
```

This will:
1. Load markdown documents from `sources/` directory
2. Split documents into chunks (size: 1000, overlap: 200)
3. Generate embeddings using HuggingFace's `all-MiniLM-L6-v2` model
4. Store embeddings in ChromaDB at `vectorstore/chroma_db`

**Output**: ChromaDB collection named `knowledge_base`

### Step 3: Start Chat

#### Option A: Using `main.py` (Simple Chat Interface)

Enable chat in `config/application_config.yaml`:
```yaml
application:
  dataset_generation:
    enabled: false
  rebuild_vector_db:
    enabled: false
  vector_indexing:
    enabled: false
  chat:
    enabled: true
```

Run:
```bash
python main.py
```

This launches an interactive chat interface where you can:
- Ask questions about the indexed knowledge base
- Receive RAG-enhanced responses from the configured LLM
- Maintain **multi-turn conversations** with full chat history
- Leverage query rewriting based on conversation context

Example usage:
```
You: What is Class in Java?
Answer: A class is a blueprint or template for creating objects. It defines properties (fields) and behaviors (methods)...

You: How can I create object from it?
Answer: To create an object from a class, use the 'new' keyword followed by the class name and constructor. For example: MyClass obj = new MyClass();

You: What is a test fixture in Playwright?
Answer: A test fixture in Playwright is a reusable component that sets up test preconditions before tests run...

You: exit
```

**Note**: The second question "How can I create object from it?" demonstrates query rewriting - the system recognizes "it" refers to Class from the first question and rewrites the query for better context-aware retrieval.

**Features of main.py chat mode**:
- Maintains conversation history across multiple turns
- Rewrites queries based on previous context for better retrieval
- Continuous interactive loop until user types 'exit'
- Perfect for exploring topics with follow-up questions

#### Option B: Using `chat_session.py` (Programmatic Chat with History)

For programmatic multi-turn conversations with chat history management (instead of interactive CLI), use the ChatSession class:

Create a Python script `my_chat.py`:
```python
import asyncio
from loaders.load_config import load_config
from services.chat_session import ChatSession
from dotenv import load_dotenv

async def main():
    load_dotenv()
    
    # Load configuration
    app_config = load_config('config/application_config.yaml')
    
    # Initialize chat session
    session = ChatSession(app_config)
    
    # Multi-turn conversation
    question1 = "What is a Class in Java?"
    print(f"Q1: {question1}")
    answer1 = session.ask(question1)
    print(f"A1: {answer1}\n")
    
    question2 = "How do I create an object from it?"
    print(f"Q2: {question2}")
    answer2 = session.ask(question2)
    print(f"A2: {answer2}\n")
    
    question3 = "What is the difference between StringBuffer and String?"
    print(f"Q3: {question3}")
    answer3 = session.ask(question3)
    print(f"A3: {answer3}\n")

if __name__ == "__main__":
    asyncio.run(main())
```

Run:
```bash
python my_chat.py
```

**Advantages over main.py**:
- Programmatic control over conversation flow
- Better for automation and batch processing
- Easier to integrate with other systems
- Same chat history and query rewriting features as main.py
- Better for testing and evaluation with pre-defined questions

#### Option C: Using `chat_session_without_rewrite_query_logic.py` (Backup - Development Only)

**⚠️ This is a backup version kept for development/testing purposes. Use `chat_session.py` (Option B) for production.**

For development or testing without query rewriting logic:
```python
from services.chat_session_without_rewrite_query_logic import ChatSession
# ... same usage as Option B
```

**Recommended**: Use this only if you need to debug or test RAG functionality without query rewriting. For production use, query rewriting is highly recommended for better multi-turn conversation quality.

### Comparison: Chat Modes

| Feature | main.py | chat_session.py | chat_session_without_rewrite* |
|---------|---------|-----------------|------------------------------|
| **Interface** | Interactive CLI | Programmatic API | Programmatic API |
| **Multi-turn** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Chat History** | ✅ Maintained | ✅ Maintained | ✅ Maintained |
| **Query Rewriting** | ✅ Enabled | ✅ Enabled | ❌ Disabled |
| **Best Use Case** | Interactive exploration | Automation/Testing | Development/Testing only |
| **User Input** | `input()` prompt loop | Pre-defined questions | Pre-defined questions |

\* `chat_session_without_rewrite_query_logic.py` is a backup version for development/testing purposes only. Use `chat_session.py` for production.

**Choose main.py if**: You want to interactively explore the knowledge base with follow-up questions and leverage query rewriting for better context-aware retrieval

**Choose chat_session.py if**: You need to automate conversations or integrate with other systems while maintaining query rewriting capabilities

**Note on query rewriting**: Both `main.py` and `chat_session.py` enable query rewriting by default. This is the recommended approach for multi-turn conversations. A backup version `chat_session_without_rewrite_query_logic.py` exists (query rewriting disabled) but is primarily for development/testing purposes and not recommended for production use.

### Understanding Query Rewriting

**With Query Rewriting (main.py & chat_session.py - RECOMMENDED)**:
```
User: "What is a Class in Java?"
Original Query: "What is a Class in Java?"
Retrieved: Relevant Java Class documentation ✅

User: "How can I create object from it?"
Original Query: "How can I create object from it?"
Rewritten Query: "How to create an object from a Java class?" ← LLM adds context
Retrieved: More precise object instantiation documentation ✅
```

**Without Query Rewriting (chat_session_without_rewrite_query_logic.py - BACKUP ONLY)**:
```
User: "What is a Class in Java?"
Query: "What is a Class in Java?"
Retrieved: Relevant Java Class documentation ✅

User: "How can I create object from it?"
Query: "How can I create object from it?" ← Pronoun "it" is ambiguous
Retrieved: Generic results about object creation (may miss context) ⚠️
```

**Why Query Rewriting Matters**: The `llm` parameter in `ask_question()` enables/disables query rewriting based on conversation history. Query rewriting significantly improves retrieval quality in multi-turn conversations by resolving context and pronouns.

## DeepEval Integration

### Running Evaluation Tests

DeepEval provides comprehensive metrics to evaluate the quality of answers. The project includes pre-configured test cases in the `evaluation/` directory.

#### Available Metrics

1. **Answer Relevancy**: Measures if the answer addresses the question
2. **Contextual Precision & Recall**: Evaluates retrieval quality
3. **Conversation Completeness**: Assesses multi-turn conversation quality
4. **Faithfulness**: Checks if answer is grounded in retrieved context
5. **Goal Accuracy**: Measures achievement of conversation goals
6. **Knowledge Retention**: Evaluates information preservation
7. **Role Adherence**: Checks if bot maintains assigned role
8. **Topic Adherence**: Ensures answer stays on topic
9. **Turn Faithfulness**: Evaluates single-turn answer fidelity
10. **Turn Relevancy**: Measures turn-level relevancy

#### Running a Specific Metric Test

Example - Run Answer Relevancy metric:
```bash
python -m evaluation.answerRelevancyMetric_test
```

**Note**: Use `python -m` (module execution) instead of direct file execution. This ensures Python correctly resolves imports to the `services`, `loaders`, and other project packages.

#### Running All Evaluations

Your evaluation scripts are standalone Python scripts, not pytest tests. Run them individually using module execution:

```bash
# Run individual metric tests (use 'python -m' for proper module imports)
python -m evaluation.answerRelevancyMetric_test
python -m evaluation.faithfulnessMetric_test
python -m evaluation.conversationCompletenessMetric_test
python -m evaluation.contextualPrecisionAndRecallMetrics_test
python -m evaluation.goalAccuracyMetric_test
python -m evaluation.knowledgeRetentionMetric_test
python -m evaluation.roleAdherenceMetric_test
python -m evaluation.topicAdherenceMetric_test
python -m evaluation.turnFailthfulnessMetric_test
python -m evaluation.turnRelevancyMetric_test
```

Or run all at once with a bash loop:

**Windows (PowerShell)**:
```powershell
Get-ChildItem evaluation/*_test.py | ForEach-Object { python $_.FullName }
```

**macOS/Linux**:
```bash
for file in evaluation/*_test.py; do python "$file"; done
```

#### Creating a Multi-Turn Evaluation Test

Use the existing `evaluation/turnRelevancyMetric_test.py` as a reference for multi-turn conversational evaluation:

```python
from deepeval import evaluate
from deepeval.test_case import Turn, ConversationalTestCase
from deepeval.metrics import TurnRelevancyMetric
from services.chat_session import ChatSession
from loaders.load_config import load_config
from dotenv import load_dotenv
from deepeval.models import AnthropicModel

# Load configuration and initialize judge model
load_dotenv()
application_config = load_config('config/application_config.yaml')
session = ChatSession(application_config)

judge_model_provider = application_config["deepeval_judgellm"]["provider"]
judge_model = application_config["deepeval_judgellm"]["model"]

# Create judge model based on configuration
if judge_model_provider == "claude":
    modelObj = AnthropicModel(model=judge_model, temperature=0)
else:
    print(f"{judge_model_provider} is not yet supported as judge model")

# Get multi-turn responses
question1 = "What is Class in java?"
actual_output1 = session.ask(question1)
print("Actual output1:", actual_output1)

question2 = "How do I create an object from it?"
actual_output2 = session.ask(question2)
print("Actual output2:", actual_output2)

question3 = "What is the difference between StringBuffer and String?"
actual_output3 = session.ask(question3)
print("Actual output3:", actual_output3)

# Create conversational test with all turns
conversational_test = ConversationalTestCase(
    turns=[
        Turn(role="user", content=question1),
        Turn(role="assistant", content=actual_output1),
        Turn(role="user", content=question2),
        Turn(role="assistant", content=actual_output2),
        Turn(role="user", content=question3),
        Turn(role="assistant", content=actual_output3)
    ]
)

# Evaluate using TurnRelevancyMetric
metric = TurnRelevancyMetric(threshold=0.5, model=modelObj)
evaluate(test_cases=[conversational_test], metrics=[metric])
```

Run:
```bash
python -m evaluation.turnRelevancyMetric_test
```

**What this test does**:
- Evaluates 3 sequential turns (user question + assistant answer)
- Question 1: "What is Class in java?" - Initial question
- Question 2: "How do I create an object from it?" - Follow-up using pronoun "it" to test query rewriting
- Question 3: "What is the difference between StringBuffer and String?" - Context-aware question
- Creates a `ConversationalTestCase` with all turns in sequence
- Evaluates relevancy of each turn using TurnRelevancyMetric
- Maintains full chat history across turns

#### Creating a Custom Evaluation Test

For single-turn evaluation, use the existing `evaluation/answerRelevancyMetric_test.py` as a reference:
```python
from deepeval import evaluate
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric
from services.chat_session import ChatSession
from loaders.load_config import load_config
from dotenv import load_dotenv
from deepeval.models import AnthropicModel

# Load configuration and initialize judge model
load_dotenv()
application_config = load_config('config/application_config.yaml')
judge_model_provider = application_config["deepeval_judgellm"]["provider"]
judge_model = application_config["deepeval_judgellm"]["model"]

# Create judge model based on configuration
if judge_model_provider == "claude":
    model = AnthropicModel(model=judge_model, temperature=0)
else:
    print(f"{judge_model_provider} is not yet supported")

# Initialize chat session
session = ChatSession(application_config)

# Create metric
metric = AnswerRelevancyMetric(threshold=0.6, model=model, include_reason=True)

# Test with multiple questions
question1 = "What is class in Java?"
actual_output1 = session.ask(question1)

question2 = "What is the difference between String and String Buffer in Java?"
actual_output2 = session.ask(question2)

question3 = "Which are different loops available in Python?"
actual_output3 = session.ask(question3)

# Create test cases and evaluate
test_case1 = LLMTestCase(input=question1, actual_output=actual_output1)
test_case2 = LLMTestCase(input=question2, actual_output=actual_output2)
test_case3 = LLMTestCase(input=question3, actual_output=actual_output3)

evaluate(test_cases=[test_case1, test_case2, test_case3], metrics=[metric])
```

Run:
```bash
python -m evaluation.answerRelevancyMetric_test
```

### Configuring DeepEval LLM

The DeepEval judge LLM is used to evaluate answer quality in evaluation metrics. Configure it in `config/application_config.yaml`:

```yaml
deepeval_judgellm:
  provider: claude  # Options: claude, gemini, groq
  model: claude-sonnet-4-6
  temperature: 0
```

**Note**: You can use a different LLM for evaluation than your chat LLM. For example:
- Use Claude for chat responses
- Use Gemini for evaluation metrics (to reduce costs or compare results)
- Just ensure the corresponding API key is in your `.env` file

## Project Structure

```
AIKnowledgeAssistant/
├── main.py                          # Main entry point for CLI
├── requirements.txt                 # Python dependencies
├── .env                            # Environment variables (create this)
│
├── config/
│   ├── application_config.yaml      # Pipeline & LLM settings
│   └── dataset_config.yaml          # Data source configuration
│
├── sources/                         # Generated documents
│   ├── web/                         # Web-crawled documentation
│   ├── local/                       # Local source files
│
├── localData/
│   └── pythondocs/                 # Local Python documentation
│
├── loaders/                        # Data loading modules
│   ├── document_loader.py          # Load markdown documents
│   ├── webdocument_loader.py       # Web crawling
│   ├── localdocument_loader.py     # Local file loading
│   └── load_config.py              # Config file parser
│
├── processors/                     # Document processing
│   ├── document_chunker.py         # Split documents into chunks
│   ├── embedding_generator.py      # Generate embeddings
│   └── query_rewriter.py           # Rewrite user queries
│
├── llm/                            # LLM integrations
│   ├── claude_llm.py              # Anthropic Claude
│   ├── gemini_llm.py              # Google Gemini
│   ├── openai_llm.py              # OpenAI GPT
│   └── groq_llm.py                # Groq LLama
│
├── retrieval/                      # Vector retrieval
│   ├── retriever.py               # Retriever interface
│   └── chroma_retriever.py         # ChromaDB retriever
│
├── vectorstore/                    # Vector database
│   ├── chroma_store.py            # ChromaDB operations
│   └── chroma_db/                 # Vector database storage
│
├── pipelines/                      # Data processing pipelines
│   ├── dataset_pipeline.py        # Generate dataset
│   ├── vector_pipeline.py         # Build vector index
│   ├── chat_pipeline.py           # Chat pipeline logic
│   └── chat_pipeline_without_rewrite_query_logic.py
│
├── services/                       # High-level services
│   ├── chat_session.py            # ChatSession class
│   └── chat_session_without_rewrite_query_logic.py
│
├── chat/                          # Chat modules
│   ├── chat_prompt.py             # Chat prompt template
│   └── query_rewrite_prompt.py    # Query rewriting prompt
│
├── evaluation/                    # DeepEval test metrics
│   ├── answerRelevancyMetric_test.py
│   ├── contextualPrecisionAndRecallMetrics_test.py
│   ├── conversationCompletenessMetric_test.py
│   ├── faithfulnessMetric_test.py
│   ├── goalAccuracyMetric_test.py
│   ├── knowledgeRetentionMetric_test.py
│   ├── roleAdherenceMetric_test.py
│   ├── topicAdherenceMetric_test.py
│   ├── turnFailthfulnessMetric_test.py
│   ├── turnRelevancyMetric_test.py
│   ├── golden_dataset.json         # Test cases
│   └── groq_judge.py              # Groq-based judge
│
└── models/                         # Data models
    └── embedded_chunk.py          # Embedding data structure
```

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'services'" when running evaluation scripts
**Cause**: Running evaluation scripts with direct file execution (`python evaluation/script.py`) doesn't properly resolve imports to parent packages. Also, using `/` instead of `.` in module paths.
**Solution**: Always use module execution format with dots: `python -m evaluation.script_name` (use `.` not `/`, and no `.py`)
```bash
# ✗ Wrong - will fail with ModuleNotFoundError
python evaluation/answerRelevancyMetric_test.py
python -m evaluation/answerRelevancyMetric_test  # Uses / instead of .

# ✓ Correct - proper module imports with dot notation
python -m evaluation.answerRelevancyMetric_test
```

### Issue: "Module not found" errors
**Solution**: Ensure you're running from the project root directory and the virtual environment is activated.

### Issue: API key errors
**Solution**: Verify `.env` file exists and contains correct API keys. Reload terminal after creating `.env`.

### Issue: ChromaDB initialization fails
**Solution**: Delete `vectorstore/chroma_db/` directory and rebuild vector index.

### Issue: Slow document loading
**Solution**: Reduce `max_pages` in `dataset_config.yaml` or increase `max_depth` as needed.

### Issue: DeepEval cache errors (Windows)
**Solution**: Install pywin32 as described in the Installation section.

## Common Workflows

### Workflow 1: Set Up New Knowledge Base
```bash
# 1. Update dataset_config.yaml with new data sources
# 2. Enable dataset generation in application_config.yaml
python main.py

# 3. Enable vector indexing, disable dataset generation
# 4. Run vector pipeline
python main.py

# 5. Enable chat, disable vector indexing
# 6. Test with chat
python main.py
```

### Workflow 2: Evaluate Multi-Turn RAG Quality
```bash
# 1. Run the multi-turn evaluation test
python -m evaluation.turnRelevancyMetric_test

# This tests 3 sequential questions:
# - "What is Class in java?" - Base knowledge
# - "How do I create an object from it?" - Tests query rewriting with pronoun reference
# - "What is the difference between StringBuffer and String?" - Context-aware follow-up

# 2. Review results for each turn
# 3. Check chat history maintenance
# 4. Verify query rewriting effectiveness (especially Turn 2 pronoun resolution)
# 5. Adjust retrieval settings (top_k, chunk_size) based on results
```

### Workflow 3: Full RAG Quality Evaluation
```bash
# 1. Ensure chat works
python -m services.chat_session

# 2. Run multi-turn evaluation
python -m evaluation.turnRelevancyMetric_test

# 3. Run all evaluation metrics (run each individually or use loop)
python -m evaluation.answerRelevancyMetric_test
python -m evaluation.faithfulnessMetric_test
# ... run other evaluation scripts

# 4. Check `golden_dataset.json` for test cases
# 5. Adjust retrieval/LLM settings based on results
```

### Workflow 4: Switch LLM Provider
```bash
# 1. Edit config/application_config.yaml
# 2. Change llm.provider and llm.model
# 3. Ensure API key is in .env
# 4. Restart chat: python main.py
```

## Advanced Usage

### Customizing Chunking Strategy
Edit `config/application_config.yaml`:
```yaml
chunking:
  chunk_size: 1500    # Increase for larger context
  chunk_overlap: 300  # Increase for more overlap
```

### Adjusting Retrieval Settings
```yaml
retrieval:
  top_k: 5  # Retrieve more documents (increases context)
```

### Custom RAG Chain
Edit or extend `chat/chat_prompt.py` and `pipelines/chat_pipeline.py` to customize:
- System prompts
- Retrieval logic
- Post-processing of answers

## Performance Tips

1. **Faster Indexing**: Use smaller `chunk_size` and `chunk_overlap`
2. **Better Answers**: Increase `top_k` in retrieval settings (slower but more context)
3. **Faster Responses**: Reduce chunk size to decrease embedding generation time
4. **Better Embeddings**: Use larger HuggingFace models (more accurate but slower)

## Development

### Adding a New LLM Provider
1. Create `llm/new_provider_llm.py`
2. Implement LLM interface
3. Update `llm/llm_factory.py` to include new provider
4. Update `config/application_config.yaml` with provider name

### Adding a New Evaluation Metric
1. Create `evaluation/new_metric_test.py`
2. Import DeepEval metric class
3. Create test cases using `LLMTestCase`
4. Run using module execution: `python -m evaluation.new_metric_test`

## License

[Add your license information here]

## Support

For issues or questions:
1. Check the Troubleshooting section
2. Review configuration files for typos
3. Ensure all dependencies are installed
4. Verify API keys are correct

## References

- [DeepEval Documentation](https://deepeval.com/docs/introduction)
- [LangChain Documentation](https://python.langchain.com/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [HuggingFace Models](https://huggingface.co/models)

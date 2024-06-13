# RAG-Powered Chatbot for Auto Insurance Queries

## Overview

This project aims to create a Retrieval-Augmented Generation (RAG) powered chatbot designed to answer questions related to auto insurance policies. By leveraging advanced AI technologies and a carefully constructed dataset, this chatbot can provide accurate and relevant responses to user inquiries, making it a valuable tool for both customers and businesses in the insurance sector.

## Dataset Construction

1. **Combination Method**: 
   - **AI Assistance**: Utilized ChatGPT (Model 4) with specific guidelines to generate a portion of the dataset.
   - **Manual Search**: Manually searched for top auto insurance questions and found corresponding answers in the policy handbook.
2. **Diverse Queries**: Ensured that the questions cover different types, document sections, and pages to avoid concentration in one area.
3. **Relevance and Challenge**: Designed questions to reflect real-world scenarios, making them relevant and challenging.

### Thought Process

- **AI and Manual Integration**: Combining AI-generated content with manual searches ensures both breadth and depth in the dataset.
- **Real-world Relevance**: Focused on real-world insurance questions to make the chatbot responses practical and useful.
- **Quality Assurance**: The dataset's diversity helps gauge the chatbot's performance in various scenarios, ensuring comprehensive evaluation.

## RAG System Creation

### Tech Stack

- OpenAI embeddings
- FAISS vector database
- LangChain
- OpenAI chat model

### Development Steps

1. **Dataset Preprocessing**: Determined the ideal chunk size using the LlamaIndex framework.
2. **Initial Setup**: 
   - Built a basic local RAG using Chroma DB, Nomic-embed-text embeddings from Ollama, and the Mistral chat model.
   - Switched to Pinecone DB due to inefficiencies.
3. **Optimized Setup**: Achieved better results with OpenAI embeddings, FAISS vector database, and LangChain.
4. **Evaluation Methods**: 
   - Used the Mistral chat model.
   - Employed Sentence Transformer.
5. **Accuracy Improvements**:
   - PDF cleanup.
   - Used Multiquery retriever.
   - Few-shot prompting (added 10 initial dataset entries along with the PDF).
   - Added metadata like chunk numbers and page numbers (later removed due to issues).

### Improvements

1. **PDF Cleanup**: Ensured the input documents were clean and well-structured.
2. **Multiquery Retriever**: Improved retrieval accuracy by using multiple queries.
3. **Few-shot Prompting**: Enhanced model training by including a small set of initial dataset entries.
4. **Metadata Addition**: Added chunk numbers and page numbers to improve context relevance (removed due to issues).


## Evaluation Metrics

### Thought Process

- **Faithfulness**: Measures factual consistency of generated answers against the given context. Chosen to ensure the chatbot's responses are accurate and reliable.
- **Relevancy**: Assesses the pertinence of the generated answer to the given prompt. Chosen to ensure the chatbot provides useful and relevant information.
- **Context Recall**: Measures alignment of retrieved context with the annotated answer. Chosen to evaluate the effectiveness of context retrieval.
- **Answer Correctness**: Evaluates the accuracy of the generated answer compared to the ground truth. Chosen to ensure the chatbot's answers are correct.
- **Context Precision**: Evaluates whether all relevant items in the contexts are ranked higher. Chosen to ensure relevant information is prioritized.



## Conclusion

This RAG-powered chatbot project demonstrates the potential of combining AI technologies with manual data curation to create an effective tool for answering complex auto insurance queries. The iterative development and rigorous evaluation ensure that the chatbot meets high standards of accuracy, relevance, and reliability.
# RAG-Powered Chatbot for Auto Insurance Queries

## Overview

This project aims to create a Retrieval-Augmented Generation (RAG) powered chatbot designed to answer questions related to auto insurance policies. By leveraging advanced AI technologies and a carefully constructed dataset, this chatbot can provide accurate and relevant responses to user inquiries, making it a valuable tool for both customers and businesses in the insurance sector.

## Dataset Construction

1. **Combination Method**: The dataset was created using a combination of AI-assisted and manual approaches.
2. **AI Assistance**: Utilized ChatGPT (Model 4) with specific guidelines to generate a portion of the dataset.
3. **Manual Search**: Manually searched for top auto insurance questions and found corresponding answers in the policy handbook.
4. **Coverage**: The dataset includes various sections from the policy handbook, covering queries related to tables, text, and more.
5. **Performance Gauging**: This dataset allows businesses to assess the accuracy and relevance of RAG system responses, ensuring high-quality outputs for real-world applications.
6. **Relevance and Challenge**: The questions are designed to be relevant and challenging, reflecting real-world scenarios.

## RAG System Creation

1. **Tech Stack**: OpenAI embeddings, FAISS vector database, LangChain, and OpenAI chat model.
2. **Dataset Preprocessing**: Determined the ideal chunk size using the LlamaIndex framework.
3. **Initial Setup**:
   - Built a basic local RAG using Chroma DB, Nomic-embed-text embeddings from Ollama, and the Mistral chat model.
   - Observed inefficiencies and switched to Pinecone DB, which also did not meet expectations.
4. **Optimized Setup**: Achieved better results with OpenAI embeddings, FAISS vector database, and LangChain.
5. **Evaluation Methods**:
   - Utilized the Mistral chat model.
   - Employed Sentence Transformer.
6. **Accuracy Improvements**:
   - PDF cleanup.
   - Used Multiquery retriever.
   - Few-shot prompting (added 10 initial dataset entries along with the PDF).
   - Added metadata like chunk numbers and page numbers (later removed due to issues).
7. **Re-evaluation**:
   - Accuracy assessment with the Mistral chat model.
   - Precision, recall, and relevancy evaluation with Sentence Transformer.
   - RAGAs metrics: Faithfulness, relevancy, context recall, answer correctness, context precision.

## Metrics Focus

1. **Faithfulness**: Measures the factual consistency of the generated answer against the given context. RAGAs faithfulness is computed using an LLM-as-a-judge approach.
2. **Relevancy**: Assesses how pertinent the generated answer is to the given prompt. Higher scores indicate better relevancy.
3. **Context Recall**: Measures the extent to which the retrieved context aligns with the annotated answer.
4. **Answer Correctness**: Evaluates the accuracy of the generated answer compared to the ground truth.
5. **Context Precision**: Evaluates whether all relevant items in the contexts are ranked higher. Ideally, all relevant chunks must appear at the top ranks.

## Conclusion

This RAG-powered chatbot project demonstrates the potential of combining AI technologies with manual data curation to create an effective tool for answering complex auto insurance queries. The iterative development and rigorous evaluation ensure that the chatbot meets high standards of accuracy, relevance, and reliability.
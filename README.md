# QSharp Chat

An AI-powered chat interface that allows users to query QSharp documents using RAG (Retrieval-Augmented Generation) technology. The application combines the power of Claude 3 Sonnet with vector search capabilities to provide accurate, sourced responses from official Qsharp documents.

## 🌐 Live Demo
Visit the live application: [qsharp.streamlit.app](https://qsharp.streamlit.app)

## 🚀 Features
- Real-time chat interface with AI responses
- Source citations from QSharp documents
- Vector-based semantic search using Pinecone
- Detailed source viewing with expandable sections

## 🛠️ Technology Stack
- **Frontend**: Streamlit
- **AI Models**: 
  - Claude 3 Sonnet (Anthropic) for response generation
  - OpenAI text-embedding-3-small for vector embeddings
- **Vector Database**: Pinecone
- **Language**: Python 3.9+

## 🔧 Local Development
1. Clone the repository
git clone https://github.com/MersivMedia/qsharp-chat.git

2. Install dependencies
pip install -r requirements.txt

3. Create a `.env` file with the following variables:
ANTHROPIC_API_KEY=your_key
ANTHROPIC_MODEL=claude-3-sonnet-20240229
PINECONE_API_KEY=your_key
PINECONE_ENVIRONMENT=aws
PINECONE_INDEX_NAME=your_index_name
OPENAI_API_KEY=your_key
OPENAI_EMBEDDING_MODEL=text-embedding-3-small

4. Run the application
streamlit run app.py

## 📚 Project Structure
- `app.py`: Main application file with chat interface
- `requirements.txt`: Project dependencies

## 🔐 Security Note
This application uses publicly available declassified documents from the CIA website. It is designed for research and entertainment purposes only.

## 🤝 Contributing
Feel free to open issues or submit pull requests for improvements.

## 📝 License
[MIT License](LICENSE)

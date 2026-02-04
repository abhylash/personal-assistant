# Personal AI Assistant (Jarvis)

An end-to-end personal AI assistant powered by self-hosted LLMs and vector database knowledge storage.

## Features

- 🤖 Self-hosted LLM integration (LLaMA compatible)
- 📚 Vector database knowledge storage with Pinecone
- 💬 Conversational chatbot interface
- 🔍 Knowledge management (add/delete documents)
- 🚀 FastAPI backend with React frontend
- 🐳 Docker deployment support

## Architecture

```
├── backend/          # FastAPI server
│   ├── app/
│   │   ├── api/      # API routes (chat, knowledge)
│   │   ├── core/     # Configuration
│   │   ├── models/   # Data models
│   │   └── services/ # Business logic (Pinecone, LLM)
│   ├── requirements.txt
│   ├── Dockerfile
│   └── main.py
├── frontend/         # React chatbot UI
│   ├── src/
│   │   ├── components/ # ChatInterface, KnowledgeManager
│   │   ├── pages/     # ChatPage, KnowledgePage
│   │   └── services/  # API client
│   ├── package.json
│   ├── Dockerfile
│   └── public/
├── docker-compose.yml
└── README.md
```

## Quick Start

### Option 1: Docker (Recommended)

1. Clone the repository and navigate to the project directory
2. Copy `.env.example` to `.env` and configure your environment variables
3. Run with Docker Compose:
   ```bash
   docker-compose up
   ```
4. Access the application at `http://localhost:3000`

### Option 2: Manual Setup

#### Backend Setup

1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. Start the backend server:
   ```bash
   python main.py
   ```

#### Frontend Setup

1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

## Configuration

### Environment Variables

Create a `.env` file in the backend directory with the following variables:

```bash
# Pinecone Configuration (Required)
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_ENVIRONMENT=your_pinecone_environment_here
PINECONE_INDEX_NAME=personal-assistant

# LLM Configuration (Choose one)
# Option 1: Self-hosted LLM (e.g., LLaMA)
LLM_API_URL=http://localhost:8080/v1
LLM_API_KEY=your_llm_api_key_here

# Option 2: OpenAI
OPENAI_API_KEY=your_openai_api_key_here

# Embedding Model
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

### Pinecone Setup

1. Create a Pinecone account at [pinecone.io](https://pinecone.io)
2. Create an index with:
   - Dimension: 384 (for all-MiniLM-L6-v2)
   - Metric: cosine
3. Copy your API key and environment to the `.env` file

### Self-Hosted LLM Setup

To use a self-hosted LLM like LLaMA:

1. Set up an LLM server (e.g., using [text-generation-webui](https://github.com/oobabooga/text-generation-webui))
2. Configure it to accept API requests
3. Set `LLM_API_URL` to your server endpoint
4. Optionally set `LLM_API_KEY` if authentication is required

## Usage

### Chat Interface

1. Navigate to `http://localhost:3000`
2. Start chatting with your AI assistant
3. The assistant will use your knowledge base to provide contextually relevant answers

### Knowledge Management

1. Click the "Knowledge" button or navigate to `/knowledge`
2. Add documents to build your knowledge base
3. Search and manage existing documents
4. Documents are automatically indexed for semantic search

## API Endpoints

### Chat
- `POST /api/chat` - Send a message and get AI response
- `GET /api/chat/sessions/{session_id}` - Get chat session history

### Knowledge
- `POST /api/knowledge` - Add a document to knowledge base
- `DELETE /api/knowledge/{document_id}` - Delete a document
- `GET /api/knowledge/search` - Search knowledge base
- `GET /api/knowledge/stats` - Get knowledge base statistics

## Development

### Backend Development

The backend uses FastAPI with the following structure:
- `app/api/` - API route handlers
- `app/services/` - Business logic (Pinecone, LLM integration)
- `app/models/` - Pydantic data models
- `app/core/` - Configuration management

### Frontend Development

The frontend uses React with:
- TailwindCSS for styling
- Axios for API communication
- React Router for navigation
- Lucide React for icons

## Production Deployment

1. Configure all environment variables
2. Use HTTPS in production
3. Set up proper CORS origins
4. Consider using a reverse proxy (nginx)
5. Monitor Pinecone usage and costs

## Troubleshooting

### Common Issues

1. **Pinecone Connection Error**: Verify API key and environment
2. **LLM Not Responding**: Check LLM server URL and API key
3. **Frontend Not Connecting**: Ensure backend is running and CORS is configured
4. **TailwindCSS Not Working**: Run `npm install` in frontend directory

### Logs

- Backend logs: Check terminal output or Docker logs
- Frontend logs: Check browser developer console

## License

This project is open source and available under the [MIT License](LICENSE).

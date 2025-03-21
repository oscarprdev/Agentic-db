# Agentic DB Backend

A simple API for interacting with databases using natural language. This backend leverages a multi-agent system to interpret user queries, connect to databases, and execute SQL operations.

## Features

- Connect to any SQL database using a connection URL
- Execute read queries (SELECT statements)
- Perform write operations (INSERT, UPDATE, DELETE)
- Get help generating SQL queries
- Natural language processing for database interactions

## Architecture

The backend is organized into the following components:

- **Agents**: Specialized modules that handle different aspects of database interaction
  - `ConnectionAgent`: Manages database connections
  - `ReadAgent`: Handles read operations
  - `WriteAgent`: Manages write operations
  - `QueryAgent`: Helps generate SQL queries
  - `Orchestrator`: Routes messages to the appropriate agent

- **Routes**: API endpoints for interacting with the system
  - `/api/chat`: Main endpoint for sending messages
  - `/api/reset/{session_id}`: Reset a user session

- **Utils**: Utility functions and classes
  - `DatabaseConnection`: Handles low-level database operations

## Getting Started

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the server:
   ```
   python main.py
   ```

3. The API will be available at http://localhost:8000

## API Usage

### Send a message

```
POST /api/chat
{
  "message": "Connect to postgresql://user:password@localhost:5432/database",
  "session_id": "user-123"
}
```

Example queries:
- "Connect to postgresql://user:password@localhost:5432/database"
- "Show me all users in the users table"
- "Add a new product with name 'Widget' and price 19.99"
- "How do I write a query to join two tables?"

### Reset a session

```
GET /api/reset/user-123
```

## License

MIT 
# Anonymous Chat Application

This project is a simple real-time chat application that allows users to send anonymous messages. The application is built with FastAPI for the backend and React for the frontend. Users can join the chat, send messages, and see messages from other users in real time.

## Features

- Anonymous messaging: Send and receive messages without registering.
- Real-time updates: Messages are updated automatically using WebSocket, without the need to refresh the page.
- Message count endpoint: A dedicated endpoint to get the total number of messages in the chat.

## Technologies Used

- **Backend:** FastAPI, Python
- **Frontend:** React, JavaScript
- **WebSocket:** For real-time messaging
- **Deployment:** Instructions for local setup

## Getting Started

### Prerequisites

- [Python 3.9+](https://www.python.org/downloads/)
- [Node.js](https://nodejs.org/) (includes npm)

### Project Structure

```plaintext
project-root/
├── back-end/
│   ├── main.py
│   ├── venv/               # Virtual environment for backend dependencies
│   └── requirements.txt    # Backend dependencies
│   └── tests/              # tests
├── front-end/
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── node_modules/
└── .gitignore


# Clone the repository and navigate to the project folder
git clone https://github.com/your-username/chat-project.git
cd chat-project

# --- BACKEND SETUP ---

# Navigate to the backend folder
cd back-end

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install backend dependencies
pip install -r requirements.txt

# Run the FastAPI server (it will run on http://127.0.0.1:8000)
python main.py &

# --- FRONTEND SETUP ---

# Open a new terminal window or tab, or keep running in the same one if backend is running in the background
cd ../front-end

# Install frontend dependencies
npm install

# Run the React frontend (it will run on http://localhost:3000)
npm start

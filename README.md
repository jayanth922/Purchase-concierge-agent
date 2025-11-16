# Purchasing Concierge Agent

A sophisticated multi-agent system built with Google ADK (Agent Development Kit) that demonstrates Agent-to-Agent (A2A) communication. The system features a purchasing concierge that coordinates with specialized seller agents for pizza and burgers, enabling seamless food ordering through intelligent agent orchestration.

## 🏗️ Architecture

The system consists of three main components:

### Concierge Agent
- **Location**: `concierge/agent.py`
- **Role**: Central orchestrator that handles user requests
- **Technology**: Google ADK LlmAgent with sub-agent coordination
- **Port**: Served via ADK Web UI

### Seller Agents
- **Pizza Seller** (`sellers/pizza_server/agent.py`)
  - Manages pizza menu and orders
  - Port: 11000
- **Burger Seller** (`sellers/burger_server/agent.py`)
  - Manages burger menu and orders
  - Port: 11001

### Communication
- **Protocol**: Agent-to-Agent (A2A) using HTTP-based agent cards
- **Discovery**: Automatic agent card resolution at `/.well-known/agent-card.json`
- **Orchestration**: Concierge uses remote A2A agents as sub-agents

## ✨ Features

- **Multi-Agent Coordination**: Seamless communication between concierge and seller agents
- **Menu Management**: Dynamic menu retrieval and comparison
- **Order Processing**: Intelligent order placement with validation
- **Status Tracking**: Real-time order status checking
- **Web Interface**: ADK-powered web UI for interaction
- **RESTful APIs**: A2A endpoints for programmatic access

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- uv (Python package manager)
- Google Cloud API key with Gemini access

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/jayanth922/Purchase-concierge-agent.git
   cd Purchase-concierge-agent
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Set up environment**
   ```bash
   cp .env.example .env
   # Edit .env with your GOOGLE_API_KEY
   ```

### Running the System

1. **Start Seller Agents**
   ```bash
   # Terminal 1: Pizza Seller
   uv run uvicorn sellers.pizza_server.agent:a2a_app --host 127.0.0.1 --port 11000

   # Terminal 2: Burger Seller
   uv run uvicorn sellers.burger_server.agent:a2a_app --host 127.0.0.1 --port 11001
   ```

2. **Start Concierge Web UI**
   ```bash
   # Terminal 3: Concierge
   uv run adk web .
   ```

3. **Access the Interface**
   - Open your browser to the ADK Web UI URL (typically http://localhost:8000)
   - Interact with the concierge agent

## 📋 API Endpoints

### Seller Agents
Each seller exposes A2A endpoints:

- `GET /.well-known/agent-card.json` - Agent card discovery
- `POST /message` - Send messages to the agent

### Concierge Agent
- Served through ADK Web UI
- Supports natural language food ordering

## 🛠️ Development

### Project Structure
```
03-purchasing-concierge-local/
├── concierge/
│   ├── __init__.py
│   └── agent.py          # Main concierge agent
├── sellers/
│   ├── pizza_server/
│   │   ├── __init__.py
│   │   └── agent.py      # Pizza seller A2A server
│   └── burger_server/
│       ├── __init__.py
│       └── agent.py      # Burger seller A2A server
├── .env.example
├── .gitignore
├── pyproject.toml
├── requirements.txt
├── README.md
└── uv.lock
```

### Adding New Sellers
1. Create new seller directory under `sellers/`
2. Implement agent with menu and order tools
3. Expose via A2A with `to_a2a()`
4. Update concierge to include as sub-agent

### Environment Variables
- `GOOGLE_API_KEY`: Your Google Gemini API key
- `PIZZA_PORT`: Port for pizza seller (default: 11000)
- `BURGER_PORT`: Port for burger seller (default: 11001)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Google ADK](https://github.com/google/adk)
- Agent-to-Agent protocol implementation
- Inspired by multi-agent system architectures

## 📞 Support

For questions or issues:
- Open an issue on GitHub
- Check the ADK documentation
- Review the agent logs for debugging information
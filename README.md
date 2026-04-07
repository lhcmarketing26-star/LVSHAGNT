# LVSHAGNT
# LVSH AI Chatbot Agents

This repository contains the workflow and code related to the LVSH AI Chatbot Agents system. 

## Description

The LVSH AI Chatbot Agents aim to streamline user interactions and provide automated responses based on specified workflows.

## Installation

Instructions on how to install and set up the system will be added soon.

## Usage

Instructions on how to use the chatbot agents will be added soon.

## Contributing

If you would like to contribute to this project, feel free to fork the repository and submit a pull request. 

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

# LVSH AI Chatbot Agents Workflow System

A comprehensive, multi-agent AI chatbot system designed to accelerate business growth and automation through intelligent, specialized conversational agents.

## 🎯 Overview

LVSH AI Chatbot Agents is an enterprise-grade system featuring 5 specialized AI agents, each engineered to provide high-level information at rapid rates with reliable sources and data. Each agent specializes in a specific domain to help businesses from scratch to scale.

## 🤖 Core Agents

### 1. **LVSH AGENT CHATBOT 1 (lvshopagent)**
Intelligent modern web and app development specialist
- Self-generating problem-solving capabilities
- Free software and development consultation
- High-performance automated systems
- Quality-assured products and services
- Built-in efficiency optimization

### 2. **LVSH AGENT CHATBOT 2 (lvshplanagent)**
Professional deep-search analytics and business planning bot
- Step-by-step brand builder
- Design and creative ideation
- Business strategy management
- Financial planning and accounting
- 3-example generation for all concepts
- Theory to advanced implementation (free to premium)

### 3. **LVSH AGENT CHATBOT 3 (lvshgenagent)**
High-speed communication and monetization automation bot
- Email management and automation
- AI image generation
- AI video generation
- Content enhancement and editing
- Web-sourced intelligence integration
- Affiliate revenue optimization

### 4. **LVSH AGENT CHATBOT 4 (enchantedagent)**
Advanced integrated systems and automation specialist
- Custom code generation and components
- Full app/website/system building
- Pre-built premium stores and solutions
- Advanced analytics and dashboard integration
- Customer service automation
- AI-powered business model optimization
- Daily business idea generation
- Cloud services and deployment

### 5. **LVSH AGENT CHATBOT 5 (database_agent)**
Real-time data management and system optimization
- Continuous database updates (hourly)
- Performance monitoring and enhancement
- User experience improvement
- Feature and functionality expansion
- System-wide automation orchestration

## ✨ Key Features

- ✅ **Multi-Agent Architecture** - Specialized agents for different domains
- ✅ **Authenticated User Login** - Secure authentication system
- ✅ **Payment Processing** - Integrated Stripe/PayPal support
- ✅ **SMS Messaging** - Twilio integration for notifications
- ✅ **AI Assistant Integration** - OpenAI/Claude API connectivity
- ✅ **Comprehensive Database** - PostgreSQL with real-time updates
- ✅ **Admin Dashboard** - Full administrative control and analytics
- ✅ **Subscription Management** - Multiple tier support
- ✅ **Push Notifications** - Real-time user alerts
- ✅ **Pre-built Stores** - Ready-to-deploy business solutions
- ✅ **Bug Detection & Fixing** - Automated testing and validation

## 🏗️ Architecture

The system follows a microservices architecture with:

```
User Interface (Web/Mobile)
        ↓
Orchestrator (Router/Dispatcher)
        ↓
┌───────┬───────┬──────────┬──────────┬────────────┐
│       │       │          │          │            │
Agent1  Agent2  Agent3     Agent4     Agent5       Admin
│       │       │          │          │            │
└───────┴───────┴──────────┴──────────┴────────────┘
        ↓
Shared Context & Knowledge Store
        ↓
Database / External APIs / File Storage
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- PostgreSQL 14+
- Docker & Docker Compose
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/lhcmarketing26-star/ai-chatbot-agents-workflow.git
cd ai-chatbot-agents-workflow

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp config/environment.example .env
# Edit .env with your API keys and database credentials

# Run database migrations
python -m alembic upgrade head

# Start the application
python src/lvsh_agent_chatbots.py
```

### Docker Setup

```bash
docker-compose up -d
```

## 📋 Configuration

All configuration is managed through environment variables. See `.env.example`:

```
# API Keys
OPENAI_API_KEY=your_key_here
STRIPE_API_KEY=your_key_here
TWILIO_ACCOUNT_SID=your_sid_here
TWILIO_AUTH_TOKEN=your_token_here

# Database
DATABASE_URL=postgresql://user:password@localhost/lvsh_agents

# Application
DEBUG=False
SECRET_KEY=your_secret_key_here
```

## 📚 Documentation

- [Project Architecture](docs/project-architecture.md) - System design and components
- [Agent Specifications](docs/LVSH-AGENT-SPECIFICATIONS.md) - Detailed agent documentation
- [API Documentation](docs/API-DOCUMENTATION.md) - REST API endpoints
- [Deployment Guide](docs/DEPLOYMENT-GUIDE.md) - Production deployment instructions

## 🔄 Workflow

The system uses GitHub Actions for:
- **CI/CD Pipeline** - Automated testing and deployment
- **Security Scanning** - Vulnerability detection
- **Agent Deployment** - Containerized agent updates
- **Chatbot Testing** - Comprehensive test suite execution

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run specific test
pytest tests/test_agents.py

# Coverage report
pytest --cov=src tests/
```

## 📊 Admin Dashboard

Access the admin dashboard at `http://localhost:8000/admin`

Features include:
- User management
- Agent performance monitoring
- Revenue analytics
- Business idea management
- Pre-built store creation
- Subscription tier management
- System health monitoring

## 💳 Payment Processing

Integrated payment processors:
- Stripe (credit cards, subscriptions)
- PayPal (alternative payments)
- Custom subscription tiers
- Automated billing

## 🔐 Security

- JWT authentication
- AES-256 encryption for sensitive data
- SQL injection prevention
- CORS protection
- Rate limiting
- PII data masking
- GDPR/CCPA compliance

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 📧 Support

For support, email support@lvshagent.com or open an issue on GitHub.

## 🔗 Links

- [Website](https://lvshagent.com)
- [Documentation](https://docs.lvshagent.com)
- [GitHub Repository](https://github.com/lhcmarketing26-star/ai-chatbot-agents-workflow)

---

**Last Updated:** 2026-04-07  
**Version:** 1.0.0

# Joke Generator Module

A comprehensive, multi-source joke generator for the LVSH AI Chatbot Agents system.

## Features

- **Multiple API Sources**: Integrates with 4+ joke APIs for maximum reliability
- **Automatic Fallback**: If one source fails, automatically tries another
- **Caching**: Built-in TTL-based caching to reduce API calls
- **Type Safety**: Full TypeScript-like type hints with Pydantic models
- **Async Support**: Fully asynchronous operations for high performance
- **Category Filtering**: Multiple joke categories (programming, dark, dad, etc.)
- **Search Functionality**: Search jokes by keywords
- **Batch Fetching**: Get multiple jokes at once

## Supported Joke APIs

### 1. JokeAPI (Sv443)
- **URL**: https://v2.jokeapi.dev
- **Categories**: Any, General, Programming, Dark, Pun, Knock-knock
- **Features**: Advanced filtering, multiple languages, no auth required

### 2. Official Joke API
- **URL**: https://official-joke-api.appspot.com
- **Categories**: Random, Programming, General, Knock-knock
- **Features**: Simple, reliable, no auth required

### 3. Dad Jokes API
- **URL**: https://icanhazdadjoke.com
- **Categories**: Dad jokes, searchable
- **Features**: Search functionality, simple format

### 4. API Ninjas Jokes
- **URL**: https://api.api-ninjas.com/v1/jokes
- **Categories**: Multiple categories available
- **Features**: Requires API key (free tier available)

## Installation

The module is included in the LVSH AI Chatbot Agents. No additional installation needed.

## Quick Start

### Using the Joke Generator Directly

```python
import asyncio
from src.integrations.joke_generator import JokeGenerator

async def main():
    generator = JokeGenerator()
    
    # Get a random joke
    joke = await generator.get_random_joke()
    print(joke)
    
    # Get a programming joke
    prog_joke = await generator.get_programming_joke()
    print(prog_joke)
    
    # Get multiple jokes
    jokes = await generator.get_multiple_jokes(count=5)
    for joke in jokes:
        print(joke)

asyncio.run(main())
```

### Using the Joke Agent

```python
from src.agents.joke_agent import JokeAgent

async def main():
    agent = JokeAgent()
    
    # Tell a random joke
    result = await agent.tell_random_joke()
    print(result["message"])
    
    # Tell a programming joke
    result = await agent.tell_programming_joke()
    print(result["message"])

asyncio.run(main())
```

### Via REST API

```bash
# Get a random joke
curl http://localhost:8000/api/v1/jokes/random

# Get a programming joke
curl http://localhost:8000/api/v1/jokes/programming

# Get a dad joke
curl http://localhost:8000/api/v1/jokes/dad

# Search for a joke
curl "http://localhost:8000/api/v1/jokes/search?q=dog"

# Get multiple jokes
curl "http://localhost:8000/api/v1/jokes/multiple?count=5"

# Get joke of the day
curl http://localhost:8000/api/v1/jokes/daily
```

## API Endpoints

### GET /api/v1/jokes/random
Get a random joke from any available source.

**Response:**
```json
{
  "success": true,
  "joke": {
    "id": "123",
    "content": "Why did the chicken cross the road?",
    "type": "general",
    "category": "Any",
    "source": "JokeAPI",
    "safe": true
  },
  "message": "**Why did the chicken cross the road?**"
}
```

### GET /api/v1/jokes/programming
Get a programming-related joke.

### GET /api/v1/jokes/dad
Get a dad joke.

### GET /api/v1/jokes/dark
Get a dark/edgy joke (mature content warning).

### GET /api/v1/jokes/search?q={search_term}
Search for jokes by keyword.

**Parameters:**
- `q` (required): Search term

### GET /api/v1/jokes/multiple?count={n}
Get multiple jokes at once.

**Parameters:**
- `count` (optional, default=5): Number of jokes to fetch (1-20)

### GET /api/v1/jokes/daily
Get the joke of the day.

### POST /api/v1/jokes/invoke
Invoke a specific joke action.

**Request Body:**
```json
{
  "action": "tell_programming_joke",
  "parameters": {}
}
```

## Configuration

Add these to your `.env` file:

```bash
# Optional: API Ninjas key for additional joke sources
API_NINJAS_KEY=your_api_key_here

# Joke caching settings
JOKE_CACHE_TTL=3600  # 1 hour
JOKE_REQUEST_TIMEOUT=10  # seconds
```

## Data Models

### Joke Object

```python
@dataclass
class Joke:
    id: str                          # Unique joke ID
    content: str                     # Full joke text
    setup: Optional[str]             # Setup (for two-part jokes)
    punchline: Optional[str]         # Punchline (for two-part jokes)
    joke_type: str                   # Type: single, twopart, etc.
    category: str                    # Category: General, Programming, Dark, etc.
    source: str                      # Source API: JokeAPI, OfficialJokeAPI, etc.
    language: str                    # Language code (default: "en")
    safe: bool                       # Whether joke is safe-for-work
    rating: Optional[float]          # Rating (0-10, if available)
    fetched_at: datetime             # When the joke was fetched
```

## Performance

- **Caching**: Reduces redundant API calls (default 1 hour TTL)
- **Async**: All operations are non-blocking
- **Fallback**: Automatic failover to alternate sources
- **Timeout**: 10-second default timeout per request

## Error Handling

The module gracefully handles:
- API timeouts
- Network errors
- Malformed responses
- Rate limiting

If one API source fails, it automatically tries the next available source.

## Humor Categories

| Category | Best For |
|----------|----------|
| General | Lighthearted, family-friendly jokes |
| Programming | Jokes for developers and tech enthusiasts |
| Dad | Classic dad jokes and puns |
| Dark | Edgy, mature humor |
| Pun | Wordplay and puns |
| Knock-knock | Classic knock-knock jokes |

## Examples

### Example 1: Random Joke

```bash
$ curl http://localhost:8000/api/v1/jokes/random

{
  "success": true,
  "joke": {
    "id": "456",
    "content": "A SQL query goes into a bar, walks up to two tables and asks... 'Can I join you?'",
    "type": "single",
    "category": "Programming",
    "source": "JokeAPI",
    "safe": true
  },
  "message": "**A SQL query goes into a bar...**"
}
```

### Example 2: Multiple Jokes

```bash
$ curl http://localhost:8000/api/v1/jokes/multiple?count=2

{
  "success": true,
  "count": 2,
  "jokes": [...],
  "message": "**5 Random Jokes:**\n\n1. Joke 1...\n\n2. Joke 2..."
}
```

### Example 3: Search

```bash
$ curl "http://localhost:8000/api/v1/jokes/search?q=dog"

{
  "success": true,
  "search_term": "dog",
  "joke": {...},
  "message": "Found: **Why do dogs run in circles?**..."
}
```

## Testing

```bash
# Run joke generator tests
pytest tests/test_joke_generator.py -v

# Run with coverage
pytest tests/test_joke_generator.py --cov=src/integrations/joke_generator
```

## Troubleshooting

### All APIs are returning `null`

Check:
- Internet connection
- Firewall/proxy settings
- API service status (check their status pages)
- Request timeout (increase if needed)

### Rate limiting errors

The APIs typically allow 100+ requests per hour. If you hit rate limits:
- Enable caching (default enabled)
- Increase cache TTL
- Space out requests

### `API_NINJAS_KEY` not working

- Verify key is correct
- Check key hasn't expired
- Visit https://api-ninjas.com to manage your key

## Contributing

To add a new joke API:

1. Create a new adapter class inheriting from `BaseJokeAPI`
2. Implement the `fetch()` method
3. Add to the adapters list in `JokeGenerator.__init__()`

## License

MIT License - See LICENSE file

## Support

For issues or questions:
- GitHub Issues: https://github.com/lhcmarketing26-star/ai-chatbot-agents-workflow/issues
- Email: support@lvshagent.com

---

**Last Updated:** 2026-04-07  
**Version:** 1.0.0

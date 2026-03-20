# Installation

## Prerequisites

- Python 3.11+
- Poetry (package manager)

## Steps

1. Clone the repository:
```bash
git clone https://github.com/cktt/ai-agent-platform.git
cd ai-agent-platform
```

2. Install dependencies:
```bash
poetry install
```

3. Configure environment:
```bash
cp .env.example .env
# Edit .env with your settings
```

4. Start services:
```bash
docker-compose up -d
```

## Verification

Run the development server:
```bash
poetry run uvicorn apps.agent_api.src.agent_api.main:app --reload
```

Visit http://localhost:8000 to verify the installation.

# Configuration

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| DEBUG | Enable debug mode | false |
| ENVIRONMENT | Environment name | development |
| API_HOST | API host | 0.0.0.0 |
| API_PORT | API port | 8000 |
| DATABASE_HOST | PostgreSQL host | localhost |
| DATABASE_PORT | PostgreSQL port | 5432 |
| REDIS_HOST | Redis host | localhost |
| REDIS_PORT | Redis port | 6379 |
| LLM_PROVIDER | LLM provider | openai |
| LLM_API_KEY | API key | - |

## Configuration Files

- `config/base.yaml` - Base configuration
- `config/development.yaml` - Development overrides
- `config/staging.yaml` - Staging overrides
- `config/production.yaml` - Production overrides

# Docker Deployment Guide

Complete guide for running Ludicé with Docker and Docker Compose.

## 🐳 Quick Start

### Prerequisites

- Docker 20.10+
- Docker Compose 2.0+
- 2GB RAM minimum
- 10GB disk space

### One-Command Deploy

```bash
docker-compose up -d
```

That's it! All services will start automatically.

## 📋 Services Overview

The stack includes 5 services:

### 1. **Redis** (redis:7-alpine)
- **Port**: 6379
- **Purpose**: Data storage for balance service
- **Health check**: Automatic ping check every 10s

### 2. **Redis Service** (Go)
- **Port**: 8000
- **Purpose**: Balance management microservice
- **Dependencies**: Redis

### 3. **Backend** (Python/FastAPI)
- **Port**: 8080
- **Purpose**: Main API server
- **Dependencies**: Redis, Redis Service

### 4. **Bot** (Python/Aiogram)
- **Purpose**: Telegram bot
- **Dependencies**: Backend
- **Environment**: Requires TOKEN in frontend/.env

### 5. **Web** (Nginx)
- **Ports**: 80, 443
- **Purpose**: Serves Mini App and proxies API
- **Dependencies**: Backend

## 🚀 Deployment Steps

### 1. Configure Environment

Create `frontend/.env`:
```bash
TOKEN=your_telegram_bot_token_here
ADMIN_PASSWORD=your_admin_password
ADMIN_KEY=your_admin_key
```

Create `backend/secrets.json`:
```json
{
  "api_key": "your_api_key",
  "secret_key": "our_secret_key"
}
```

### 2. Build Images

```bash
# Build all images
./docker-build.sh

# Or manually
docker-compose build
```

### 3. Start Services

```bash
# Start all services
docker-compose up -d

# Start specific service
docker-compose up -d backend

# With logs
docker-compose up
```

### 4. Verify Deployment

```bash
# Check service status
docker-compose ps

# View logs
docker-compose logs -f

# Check specific service
docker-compose logs -f bot
```

## 🔧 Configuration

### Environment Variables

**Backend:**
```yaml
environment:
  - REDIS_HOST=redis
  - REDIS_PORT=6379
  - DEBUG=false
```

**Bot:**
```yaml
environment:
  - BACKEND_URL=http://backend:8080
  - REDIS_SERVICE_URL=http://redis-service:8000
env_file:
  - frontend/.env
```

### Volumes

**Persistent Data:**
```yaml
volumes:
  - ./data:/app/data          # Application data
  - redis-data:/data          # Redis persistence
```

**Development Mode:**
```yaml
volumes:
  - ./frontend:/app           # Live code updates
  - ./backend:/app
```

### Ports

| Service | Internal | External | Purpose |
|---------|----------|----------|---------|
| Redis | 6379 | 6379 | Redis server |
| Redis Service | 8000 | 8000 | Balance API |
| Backend | 8080 | 8080 | Main API |
| Web | 80, 443 | 80, 443 | Mini App |

## 📊 Monitoring

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend

# Last 100 lines
docker-compose logs --tail=100 bot

# Since specific time
docker-compose logs --since 2024-01-01
```

### Check Resource Usage

```bash
# Container stats
docker stats

# Specific container
docker stats ludice-backend

# Format output
docker stats --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"
```

### Health Checks

```bash
# Check all services
docker-compose ps

# Detailed inspect
docker inspect ludice-backend

# Health status
docker inspect --format='{{.State.Health.Status}}' ludice-redis
```

## 🔄 Updates & Maintenance

### Update Application

```bash
# Pull latest code
git pull

# Rebuild images
docker-compose build

# Restart with new images
docker-compose up -d

# Remove old images
docker image prune -f
```

### Update Dependencies

```bash
# Update Python dependencies
docker-compose exec backend pip install --upgrade -r requirements.txt

# Update Go dependencies
docker-compose exec redis-service go get -u ./...
```

### Database Backup

```bash
# Backup Redis data
docker-compose exec redis redis-cli SAVE
docker cp ludice-redis:/data/dump.rdb ./backups/

# Backup JSON data
tar -czf data-backup-$(date +%Y%m%d).tar.gz data/
```

### Restore from Backup

```bash
# Stop services
docker-compose down

# Restore Redis
docker cp ./backups/dump.rdb ludice-redis:/data/

# Restore JSON data
tar -xzf data-backup-20240101.tar.gz

# Start services
docker-compose up -d
```

## 🐛 Troubleshooting

### Service Won't Start

```bash
# Check logs
docker-compose logs [service-name]

# Check container details
docker inspect ludice-[service-name]

# Try rebuilding
docker-compose build --no-cache [service-name]
docker-compose up -d [service-name]
```

### Connection Issues

```bash
# Test network connectivity
docker-compose exec backend ping redis
docker-compose exec bot curl http://backend:8080

# Check network
docker network inspect ludice-network

# Recreate network
docker-compose down
docker network rm ludice-network
docker-compose up -d
```

### Out of Memory

```bash
# Check memory usage
docker stats

# Add memory limits to docker-compose.yml:
services:
  backend:
    mem_limit: 512m
    mem_reservation: 256m
```

### Disk Space Issues

```bash
# Check disk usage
docker system df

# Clean up
docker system prune -a
docker volume prune

# Clean specific items
docker image prune -a
docker container prune
```

## 🔒 Security

### Production Settings

```yaml
# docker-compose.prod.yml
services:
  backend:
    environment:
      - DEBUG=false
    restart: always
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### Network Isolation

```yaml
networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true
```

### Secrets Management

Use Docker secrets instead of environment variables:

```yaml
secrets:
  bot_token:
    file: ./secrets/bot_token.txt

services:
  bot:
    secrets:
      - bot_token
```

## 📈 Scaling

### Horizontal Scaling

```bash
# Scale bot instances
docker-compose up -d --scale bot=3

# Scale backend
docker-compose up -d --scale backend=2
```

### Load Balancing

Add nginx load balancer:

```yaml
services:
  loadbalancer:
    image: nginx:alpine
    ports:
      - "8080:80"
    volumes:
      - ./lb.conf:/etc/nginx/nginx.conf
    depends_on:
      - backend
```

## 🚦 CI/CD Integration

### GitHub Actions

```yaml
- name: Build and push images
  run: |
    docker-compose build
    docker-compose push

- name: Deploy to server
  run: |
    ssh user@server "cd /opt/ludice && docker-compose pull && docker-compose up -d"
```

### Auto-restart on Failure

```yaml
services:
  backend:
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

## 📚 Advanced Topics

### Multi-Stage Builds

Already implemented in Dockerfiles for optimized images.

### Custom Networks

```yaml
networks:
  frontend:
  backend:
    internal: true

services:
  web:
    networks:
      - frontend
  backend:
    networks:
      - frontend
      - backend
  redis:
    networks:
      - backend
```

### Volume Management

```bash
# List volumes
docker volume ls

# Inspect volume
docker volume inspect ludice_redis-data

# Backup volume
docker run --rm -v ludice_redis-data:/data -v $(pwd):/backup alpine tar czf /backup/redis-backup.tar.gz /data

# Restore volume
docker run --rm -v ludice_redis-data:/data -v $(pwd):/backup alpine tar xzf /backup/redis-backup.tar.gz -C /
```

## 🎯 Best Practices

1. **Always use specific versions** in Dockerfiles
2. **Multi-stage builds** for smaller images
3. **Health checks** for all services
4. **Resource limits** to prevent OOM
5. **Proper logging** configuration
6. **Regular backups** of data volumes
7. **Security scanning** of images
8. **Network isolation** between services

## 📞 Support

Issues with Docker deployment? Check:
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/)
- [GitHub Issues](https://github.com/yourusername/Ludice/issues)

---

**Ready to deploy!** 🚀

# Redis Setup and Configuration Guide

## Installation

### Ubuntu/Debian
```bash
# Update package list
sudo apt update

# Install Redis
sudo apt install redis-server

# Start Redis service
sudo systemctl start redis-server

# Enable Redis to start on boot
sudo systemctl enable redis-server

# Verify installation
redis-cli ping
# Should return: PONG
```

### macOS
```bash
# Using Homebrew
brew install redis

# Start Redis service
brew services start redis

# Verify installation
redis-cli ping
```

### Windows
1. Download Redis for Windows from https://github.com/microsoftarchive/redis/releases
2. Run the installer
3. Add Redis to PATH environment variable
4. Start Redis server:
   ```bash
   redis-server
   ```

## Configuration

### Basic Configuration
1. Locate redis.conf file:
   - Linux: /etc/redis/redis.conf
   - macOS: /usr/local/etc/redis.conf
   - Windows: C:\Program Files\Redis\redis.windows.conf

2. Essential Settings:
```conf
# Memory Management
maxmemory 128mb
maxmemory-policy allkeys-lru

# Connection
bind 127.0.0.1
port 6379
timeout 300

# Security
requirepass your_password_here

# Persistence
save 900 1
save 300 10
save 60 10000
```

## Integration with Flask

1. Update .env file:
```
REDIS_URL=redis://localhost:6379
REDIS_PASSWORD=your_password_here
```

2. Test connection:
```python
import redis

r = redis.Redis(
    host='localhost',
    port=6379,
    password='your_password_here',
    decode_responses=True
)

try:
    r.ping()
    print("Connected to Redis")
except redis.ConnectionError:
    print("Redis connection failed")
```

## Monitoring

```bash
# Monitor all commands
redis-cli monitor

# Get server info
redis-cli info

# Memory stats
redis-cli info memory
```

## Troubleshooting

1. Connection Refused
```bash
# Check if Redis is running
sudo systemctl status redis

# Restart Redis
sudo systemctl restart redis
```

2. Memory Issues
```bash
# Check memory usage
redis-cli info memory
```
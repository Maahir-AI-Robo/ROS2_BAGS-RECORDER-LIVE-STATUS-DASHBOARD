# Universal ROS2 Live Recording Status Dashboard

A complete implementation of an offline-first, enterprise-grade ROS2 recording and monitoring system.

## Overview

This system provides:
- Automatic ROS2 topic discovery and configuration
- Robust recording and incremental session handling
- Real-time live recording status dashboard
- Transactional, resumable uploads between edge and cloud

## Features

- **Offline-First**: Recording and local storage work without network
- **Zero Data Loss**: Atomic writes, checksumming, and transactional commit/rollback
- **Universal ROS2 Compatibility**: Works with any ROS2 distro and DDS implementation
- **Real-Time Dashboard**: Live metrics, progress bars, alerts, and logs
- **Resumable Uploads**: Chunked uploads with precise resume capability
- **Security**: Encryption at rest and in transit
- **Observability**: Rich metrics and audit trails

## Requirements

- Docker & Docker Compose
- ROS2 (Foxy/Galactic/Humble/Iron)
- 100GB+ disk space
- Python 3.8+
- Node.js 16+

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/Maahir-AI-Robo/ROS2_BAGS-RECORDER-LIVE-STATUS-DASHBOARD.git
cd ROS2_BAGS-RECORDER-LIVE-STATUS-DASHBOARD
```

2. Copy and configure environment variables:
```bash
cp .env.example .env
# Edit .env with your settings
```

3. Start services:
```bash
docker-compose up -d
```

4. Access dashboard:
```
http://localhost:3000
```

## Documentation

See [docs/](docs/) directory for detailed documentation:
- [Installation Guide](docs/installation.md)
- [Configuration Reference](docs/configuration.md)
- [API Documentation](docs/api.md)
- [Developer Guide](docs/development.md)

## License

[MIT License](LICENSE)
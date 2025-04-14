# QGIS Server with Flask Management

This repository provides a Docker Compose setup for running a QGIS Server alongside a Flask application to create, manage, and serve QGIS projects. The stack includes QGIS Server for rendering maps, a Flask API for project management, and Nginx as a reverse proxy to handle requests.

## Features

- **QGIS Server**: Serves WMS/WFS maps using QGIS project files (`.qgs`).
- **Flask API**: Allows creating and listing QGIS projects programmatically.
- **Nginx Proxy**: Routes requests to QGIS Server for map rendering or to Flask API
- **Docker Compose**: Simplifies deployment with isolated services and shared data volumes.

## Project Structure

```
qgis-flask-docker/
├── data/              # Directory for QGIS project files and shapefiles
├── flaskgis/          # Directory for the Flask service
│   ├── Dockerfile     # Docker image definition for Flask
│   ├── app.py         # Flask application for project management
│   └── requirements.txt  # Python dependencies
├── fonts/             # Directory for custom fonts
├── plugins/           # Directory for QGIS plugins
├── nginx.conf         # Nginx configuration for proxying requests
├── docker-compose.yml # Docker Compose configuration
└── README.md          # This file
```

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) installed.
- A shapefile (e.g., `world.shp`) in the `data/` directory for QGIS projects.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/voirinprof/qgis_docker.git
   cd qgis_docker
   ```

2. **Prepare data**:
   - Place your shapefile (e.g., `world.shp`) in the `data/` directory.
   - Optionally, add QGIS plugins to `plugins/` or custom fonts to `fonts/`.

3. **Start the services**:
   ```bash
   docker-compose up --build -d
   ```
   - The `--build` flag rebuilds the Flask image if needed.
   - `-d` runs containers in detached mode.


### Stop the services

```bash
docker-compose down
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request with improvements.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

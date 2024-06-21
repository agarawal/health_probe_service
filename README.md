# Health Probe Service

Health Probe Service is a Django application designed for monitoring the health status of various endpoints (probes). It periodically checks the specified URLs and logs their responses using threads for concurrency.

## Features

- **Probe Management**: CRUD operations for probes (URLs to monitor).
- **Threaded Monitoring**: Uses Python threads for concurrent health check operations.
- **Django Signals**: Utilizes signals (`post_save` and `post_delete`) to start and stop probe monitoring dynamically.

## Supported Endpoints

Health Probe Service supports monitoring the following types of endpoints:

1. **HTTP/HTTPS Endpoints**: Monitors standard web URLs using HTTP or HTTPS protocols.
2. **Custom Protocols**: Extensible for monitoring endpoints with custom protocols, provided a compatible fetch method is implemented.
3. **API Endpoints**:
   - **Get Probes**: Endpoint to retrieve specific probe.
     - URL: `/probe/`
     - Method: `GET`
     - - Query Parameters:
       - `url`: URL of the probe to query.
   - **Create Probe**: Endpoint to create a new probe.
     - URL: `/probe/create/`
     - Method: `POST`
     - Payload:
       ```json
       {
           "url": "http://example.com",
           "duration": 60
       }
       ```
     - Description: Creates a new probe with the specified URL and monitoring duration in seconds.
   - **Delete Probe**: Endpoint to delete an existing probe.
     - URL: `/probe/delete/`
     - Method: `DELETE`
     - Query Parameters:
       - `url`: URL of the probe to delete.
     - Description: Deletes the probe with the specified URL.

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.11 (or compatible version)
- Docker (optional, for containerization)

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/health_probe_service.git
   cd health_probe_service
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   
3. Database Setup:
   ```bash
   python manage.py migrate
   ```

### Running the Development Server
  ```bash
  python manage.py runserver
  ```
  The application will be accessible at http://localhost:8000.


## Docker

### To run the application in Docker containers:

**Building the Docker Image**
1. Build the Docker image:

  ```bash
  docker build -t health-probe-service .
  ```

2. Running the Docker Container

  ```bash
  docker run -p 8000:8000 health-probe-service
  ```




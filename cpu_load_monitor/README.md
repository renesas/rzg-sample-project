# CPU Monitor Web Server

A lightweight Flask-based web server for visualizing real-time CPU usage monitoring. This project includes support for Docker-based deployment and displays the overall CPU usage along with core 0 and core 1 statistics.

---

## Folder Structure

```
.
├── cpu_load_monitor/       # Root folder
    ├── app.py              # Flask server and Python backend
    ├── Dockerfile          # Docker build instructions
    ├── requirements.txt    # Python dependencies
    ├── static/
    │   ├── script.js       # Frontend logic and chart rendering
    │   └── styles.css      # CSS styles
    ├── templates/
    │   └── index.html      # Web interface
```

---

## How to Run the Web Server

### Prerequisites

- Docker installed
- Static IP configured for your Ethernet connection (for server access)

### How to assign Static IP

- Please refer to "docs/Setting_Up_Static_IP_address_in_G2L_Board.pdf"
- Follow the steps mentioned in the pdf

### Build & Run

1. Copy the complete project folder to your device.
2. Navigate into the root folder:
   ```bash
   cd cpu_load_monitor
   ```
3. Build the Docker image:
   ```bash
   docker build -t cpu-monitor .
   ```
4. Run a container using the image:
   ```bash
   docker run -d -p 5000:5000 -v /etc/issue:/etc/issue:ro --name cpu-monitor-container cpu-monitor
   ```
5. Start the container manually:
   ```bash
   docker start -i <container-id>
   ```
6. Start the container automatically with board bootup:
   Please refer to "docs/Autoboot_docker_service_in_G2L_Board.pdf"
---

## Accessing the Web Server

Once running, open a browser and go to:

```
http://<device-ip>:5000/
```

You should see the live CPU monitor dashboard, showing:
- Aggregate CPU usage
- CPU core 0 usage
- CPU core 1 usage

---

## Tech Stack

- **Flask** (Python backend)
- **Chart.js** (frontend graph rendering)
- **Docker** (containerized deployment)
- **HTML/CSS/JS** (UI)

---

## Notes

- Toggle between CPU charts using the sidebar.
- Dark/light mode toggle available via checkbox.
- Ensure network visibility of the device IP to access the dashboard remotely.

---

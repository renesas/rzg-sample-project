# CPU Monitor Web Server

A lightweight Flask-based web server for visualizing real-time CPU usage monitoring. This project includes support for Docker-based deployment and displays the overall CPU usage along with core 0 and core 1 statistics.

Basic overview of the project:

1. Fetches and plots the CPU usage from proc/stat file in the device every second.
2. Last 60 seconds (60 datapoints) of the cpu usage data is plotted on the graph.
3. Once the plot is changed the data in it will be discarded and the new plot will start plotting again from that instant in time.

---

## `/proc/stat` Format
The first line of `/proc/stat` shows cumulative CPU time counters (in **jiffies**, typically 1/100s of a second):

```
cpu  3357 0 4313 1362393 238 0 127 0 0 0
```

These fields represent:
1. **user** – Time spent in user mode.
2. **nice** – Time spent in user mode with low priority.
3. **system** – Time spent in kernel mode.
4. **idle** – Time spent idle.
5. **iowait** – Time spent waiting for I/O.
6. **irq** – Time servicing interrupts.
7. **softirq** – Time servicing softirqs.
8. **steal** – Time stolen by other operating systems (in VMs).
9. **guest** – Time running guest VMs.
10. **guest_nice** – Time running niced guest VMs.

---

## CPU Usage Calculation
CPU usage is not an absolute value; it’s calculated **between two readings** of `/proc/stat`.

### Steps:
1. Read values of all CPU fields at time **T1**.
2. After a small delay (e.g., 1 second), read values again at **T2**.
3. Calculate the **difference (Δ)** for each field:  
   ```
   Δuser   = user2   - user1
   Δsystem = system2 - system1
   Δidle   = idle2   - idle1
   ...
   ```
4. Compute **total time** during the interval:  
   ```
   Δtotal = Δuser + Δnice + Δsystem + Δidle + Δiowait + Δirq + Δsoftirq + Δsteal
   ```
5. Compute CPU usage percentage:  
   ```
   CPU Usage % = (Δtotal - Δidle - Δiowait) / Δtotal * 100
   ```
   - Busy time = total time - idle time  
   - Usage % = busy time / total time  

---

## Folder Structure

```
.
├── cpu_load_monitor/                                          # Root folder
    ├── docs/
    │   ├── Autoboot_docker_service_in_G2L_Board.pdf           # Guide to auto-start docker continer on boot-up
    │   └── Setting_Up_Static_IP_address_in_G2L_Board.pdf      # Guide to set-up static IP for the device
    ├── app.py                                                 # Flask server and Python backend
    ├── Dockerfile                                             # Docker build instructions
    ├── requirements.txt                                       # Python dependencies
    ├── static/
    │   ├── script.js                                          # Frontend logic and chart rendering
    │   └── styles.css                                         # CSS styles
    ├── templates/
    │   └── index.html                                         # Web interface
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
6. (Optional) Start the container automatically with board bootup:
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

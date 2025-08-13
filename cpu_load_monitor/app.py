from flask import Flask, render_template
from flask_socketio import SocketIO
import time

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Function to read CPU stats from /proc/stat for cpu, cpu0, and cpu1
def get_cpu_load():
    with open('/proc/stat', 'r') as f:
        lines = f.readlines()

    # Read the first line which is the aggregate CPU stats (total for all cores)
    aggregate_cpu = lines[0].split()

    # Parse the aggregate stats
    aggregate_stats = {
        'total': sum(map(int, aggregate_cpu[1:])),
        'idle': int(aggregate_cpu[4]) + int(aggregate_cpu[5])  # idle + iowait
    }

    # Read the CPU stats for cpu0 and cpu1 (assuming at least 2 CPUs are available)
    cpu_cores = {}
    for line in lines[1:3]:  # Only read lines for cpu0 and cpu1 (index 1 and 2)
        cpu_info = line.split()
        core_id = cpu_info[0]
        core_stats = {
            'total': sum(map(int, cpu_info[1:])),
            'idle': int(cpu_info[4]) + int(cpu_info[5])  # idle + iowait
        }
        cpu_cores[core_id] = core_stats

    return aggregate_stats, cpu_cores

# Function to calculate CPU usage for aggregate CPU and cpu0, cpu1
def calculate_cpu_usage(prev_stats, prev_cores_stats):
    # Get the current stats
    aggregate_stats, cpu_cores_stats = get_cpu_load()

    # Calculate usage for all cores and the aggregate CPU
    cpu_usage = {}

    # For aggregate CPU
    total_diff = aggregate_stats['total'] - prev_stats['total']
    idle_diff = aggregate_stats['idle'] - prev_stats['idle']
    cpu_usage['cpu'] = (total_diff - idle_diff)* 100 / total_diff

    # For cpu0 and cpu1
    for core_id in ['cpu0', 'cpu1']:
        stats = cpu_cores_stats.get(core_id, {'total': 0, 'idle': 0})
        total_diff = stats['total'] - prev_cores_stats.get(core_id, {'total': 0, 'idle': 0})['total']
        idle_diff = stats['idle'] - prev_cores_stats.get(core_id, {'total': 0, 'idle': 0})['idle']
        cpu_usage[core_id] = (total_diff - idle_diff) * 100 / total_diff

    # Return the updated stats
    return cpu_usage, aggregate_stats, cpu_cores_stats

def get_vlp_ver():
    with open('/etc/issue', 'r') as f:
        lines = f.readlines()
    issue_file = ''.join(lines).strip()
    vlp_ver = issue_file.split("Version: ")[1]
    return vlp_ver


@app.route("/")
def index():
    return render_template("index.html")

@socketio.on('connect')
def connect():
    socketio.start_background_task(send_data)

def send_data():
    # Initial values for previous total stats
    prev_stats, prev_cores_stats = get_cpu_load()
    
    vlp_ver = get_vlp_ver()
    socketio.emit('vlp_ver', {'ver': vlp_ver})

    while True:
        
        socketio.sleep(1)
        # Calculate the current CPU usage for aggregate CPU and cpu0, cpu1
        cpu_usage, prev_stats, prev_cores_stats = calculate_cpu_usage(prev_stats, prev_cores_stats)

        # Emit the CPU usage to the client
        socketio.emit('system_data', cpu_usage)

        # Sleep for 1 second before sending the next update
        # socketio.sleep(1)

# if __name__ == '__main__':
#     socketio.run(app, host='0.0.0.0', port=5000, debug=True)


🚦 Smart Traffic Monitoring Dashboard
Overview

The Smart Traffic Monitoring Dashboard is a web-based application built with Streamlit and OpenCV that allows users to upload traffic videos and automatically detect:

Vehicles and buses

Traffic light status (RED/GREEN)

Traffic violations (vehicles moving during RED light)

Traffic density (LOW, MEDIUM, HIGH)

Live graphs of counts over time

No IoT or hardware is required — everything runs directly in the browser.

🧩 Features

Upload any traffic video in MP4, AVI, or MOV format

Automatic detection of vehicles and buses using OpenCV

Traffic violation detection for cars and buses moving during red lights

Traffic density analysis based on total vehicle count

Live updating graphs for vehicles, buses, and violations

Stop button to interrupt video processing anytime

📦 Installation
1. Clone the repository
git clone <your-repo-url>
cd SmartTrafficDashboard

2. Install dependencies
pip install -r requirements.txt


(or manually install: opencv-python, streamlit, matplotlib, numpy)

3. Run the application
streamlit run traffic_dashboard.py


Open the browser at http://localhost:8501 to access the dashboard.

🖥️ Usage

Click Upload a Traffic Video and select your video file.

Use the sidebar sliders to adjust:

Detection Sensitivity: Determines minimum contour size for detection

Red Light Duration: Number of frames the light stays red

Press the Stop Video Processing button to interrupt at any time.

Monitor live video detection and see the graph updating over time

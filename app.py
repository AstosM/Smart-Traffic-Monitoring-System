import cv2
import numpy as np
import streamlit as st
import tempfile
import matplotlib.pyplot as plt
import time

# ===== Streamlit Page Setup =====
st.set_page_config(page_title="Smart Traffic Dashboard", layout="wide")
st.title("🚦 Smart Traffic Monitoring System")
st.write("Upload a traffic video to detect vehicles, buses, violations, and traffic density.")

# ===== Upload Video =====
uploaded_file = st.file_uploader("📤 Upload a Traffic Video", type=["mp4", "avi", "mov"])

if uploaded_file is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    video_path = tfile.name

    # Sidebar for settings
    st.sidebar.header("⚙️ Settings")
    detection_sensitivity = st.sidebar.slider("Detection Sensitivity", 500, 3000, 900)
    red_light_duration = st.sidebar.slider("Red Light Duration (frames)", 100, 400, 200)

    # Add a stop button
    stop_video = st.sidebar.button("🛑 Stop Video Processing")

    # Initialize variables
    cap = cv2.VideoCapture(video_path)
    fgbg = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=50)
    vehicle_count, bus_count, violation_count, frame_count = 0, 0, 0, 0
    light_color = "GREEN"
    density = "LOW"

    vehicle_list, bus_list, violation_list, time_list = [], [], [], []

    # Streamlit video frame placeholder
    stframe = st.empty()

    # Graph placeholder
    graph = st.empty()

    def get_density(total):
        if total < 10:
            return "LOW"
        elif total < 30:
            return "MEDIUM"
        else:
            return "HIGH"

    # ===== Process Video =====
    st.write("🎬 Processing video...")

    while cap.isOpened():
        if stop_video:
            st.warning("⏹ Video processing stopped by user")
            break

        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (640, 360))
        mask = fgbg.apply(frame)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        frame_count += 1
        light_color = "GREEN" if frame_count % (red_light_duration * 2) < red_light_duration else "RED"

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > detection_sensitivity:
                x, y, w, h = cv2.boundingRect(cnt)
                cx, cy = x + w // 2, y + h // 2
                color = (0, 255, 0)

                # Size-based detection
                if area < 3000:
                    vehicle_count += 1
                else:
                    bus_count += 1
                    color = (255, 0, 0)

                if light_color == "RED":
                    violation_count += 1

                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

        total = vehicle_count + bus_count
        density = get_density(total)

        # ===== Display Info =====
        cv2.putText(frame, f"Light: {light_color}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                    (0, 0, 255) if light_color == "RED" else (0, 255, 0), 2)
        cv2.putText(frame, f"Vehicles: {vehicle_count}", (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, f"Buses: {bus_count}", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 200, 255), 2)
        cv2.putText(frame, f"Violations: {violation_count}", (20, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        cv2.putText(frame, f"Density: {density}", (20, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 200, 0), 2)

        # Convert BGR → RGB for Streamlit display
        stframe.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # ===== Update Graph =====
        if frame_count % 60 == 0:
            current_time = time.strftime("%H:%M:%S")
            time_list.append(current_time)
            vehicle_list.append(vehicle_count)
            bus_list.append(bus_count)
            violation_list.append(violation_count)

            fig, ax = plt.subplots()
            ax.plot(time_list, vehicle_list, label="Vehicles", color='green')
            ax.plot(time_list, bus_list, label="Buses", color='blue')
            ax.plot(time_list, violation_list, label="Violations", color='orange')
            ax.set_title("Traffic Statistics Over Time")
            ax.set_xlabel("Time")
            ax.set_ylabel("Count")
            ax.legend()
            graph.pyplot(fig)

    cap.release()
    st.success("✅ Video analysis complete!")

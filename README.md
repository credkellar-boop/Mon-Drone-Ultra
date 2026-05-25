# Mon-Drone-Ultra 🚁🤖

[![CI Pipeline](https://github.com/credkellar-boop/Mon-Drone-Ultra/actions/workflows/ci.yml/badge.svg)](https://github.com/credkellar-boop/Mon-Drone-Ultra/actions)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![MAVSDK](https://img.shields.io/badge/MAVSDK-Python-brightgreen)](https://mavsdk.mavlink.io/main/en/python/)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Mon-Drone-Ultra** is an autonomous, AI-powered smart-drone featuring a dual-tier PX4 and ROS 2 navigation stack for Waymo-like autopilot capability. It integrates the Gemini Vision-Language Model (VLM) for intelligent audio/vision processing, localized facial recognition for security tracking, a Google Maps mobile dashboard, and a stabilized 10–60" cinematic pico-projector.

---

## 🚀 Features

* **Autonomous Navigation (PX4/MAVSDK):** Waypoint mapping, offboard velocity tracking, and return-to-home fail-safes.
* **VLM Tactical Brain (Gemini 2.5 Flash):** Processes flight telemetry and spatial situations to output structured (Pydantic) offboard flight vectors in real-time.
* **Facial Recognition Tracking:** OpenCV-based intruder detection and facial mapping.
* **Cinematic Pico-Projector Payload:** Hardware node integration for projecting visuals/audio to the ground dynamically.
* **Live Mission Control (Streamlit):** Web dashboard featuring real-time telemetry, manual payload overrides, and live Google Maps tracking.
* **Environmental Intelligence:** Integrates OpenWeatherMap APIs to inform the Gemini brain of current flight conditions.

---

## 📂 Project Structure

```text
Mon-Drone-Ultra/
├── .github/
│   └── workflows/
│       └── ci.yml               # GitHub Actions CI/CD Pipeline
├── ai_brain/
│   ├── agent.py                 # Gemini VLM decision engine & structured outputs
│   └── face_tracker.py          # OpenCV facial recognition and dynamic tracking
├── hardware_nodes/
│   └── payload.py               # GPIO controls for Pico-projector & Audio Amp
├── services/
│   └── logger.py                # Telemetry and decision logging for post-flight analysis
├── tests/
│   └── test_placeholder.py      # Pytest unit testing suite
├── ui_dashboard/
│   └── app.py                   # Streamlit Mission Control Web UI
├── utils/
│   └── env_service.py           # External API handlers (OpenWeatherMap, etc.)
├── preflight_check.py           # Automated systems/battery checks before arming
├──

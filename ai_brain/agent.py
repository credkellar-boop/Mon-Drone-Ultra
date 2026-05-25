import asyncio
import os
from google import genai
from google.genai import types
from mavsdk import System
from mavsdk.offboard import OffboardError, VelocityBodyYawspeed

# Ensure API key is configured
if not os.environ.get("GEMINI_API_KEY"):
    raise ValueError("CRITICAL: GEMINI_API_KEY environment variable is not set.")

async def analyze_scene_with_gemini(client, situation_brief: str):
    """
    Sends the current spatial/security situation to Gemini to determine 
    tactical movement vectors for Mon-Drone-Ultra.
    """
    print("[AI-BRAIN] Consulting Gemini VLM...")
    
    prompt = f"""
    You are the central brain of Mon-Drone-Ultra, an autonomous drone equipped with a 60-inch projector and face recognition.
    Current Situation: {situation_brief}
    
    Respond strictly in the following raw format so our parsing layer can ingest it:
    FORWARD_VELOCITY: <float between -2.0 and 2.0 m/s>
    RIGHT_VELOCITY: <float between -2.0 and 2.0 m/s>
    YAW_SPEED: <float between -45.0 and 45.0 deg/s>
    ACTION_LOG: <brief phrase explaining why you chose this action>
    """

    # Using the standard gemini-2.5-flash model for ultra-low latency edge decisions
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text

async def run_ai_drone_loop():
    # Initialize the Gemini Client
    ai_client = genai.Client()
    
    # Initialize Mon-Drone-Ultra Flight Stack Connection
    drone = System()
    print("[FLIGHT] Connecting to Mon-Drone-Ultra via MAVLINK...")
    await drone.connect(system_address="udp://:14540")

    async for state in drone.core.connection_state():
        if state.is_connected:
            print("[FLIGHT] Core Telemetry Link Established.")
            break

    # Mock Scenario: Local Face Recognition has triggered an unknown entity target
    # In a production environment, this text block would be fed via OpenCV/Mediapipe metadata bounding boxes
    mock_sensor_input = "Face recognition flagged an unknown person standing 4 meters away, offset slightly to the right. The projector is currently OFF."

    # Send the sensor profile to Gemini
    gemini_decision = await analyze_scene_with_gemini(ai_client, mock_sensor_input)
    print("\n--- GEMINI RAW STRATEGY ---")
    print(gemini_decision)
    print("---------------------------\n")

    # Simple regex parsing engine for extracting the flight velocities from Gemini's response
    try:
        lines = gemini_decision.strip().split('\n')
        forward = float([l for l in lines if "FORWARD_VELOCITY" in l][0].split(":")[1].strip())
        right = float([l for l in lines if "RIGHT_VELOCITY" in l][0].split(":")[1].strip())
        yaw = float([l for l in lines if "YAW_SPEED" in l][0].split(":")[1].strip())
        log = [l for l in lines if "ACTION_LOG" in l][0].split(":")[1].strip()
        
        print(f"[DECISION LOG]: {log}")
    except Exception as e:
        print(f"[ERROR] Failed to parse Gemini output, falling back to safe hover layout. Error: {e}")
        forward, right, yaw = 0.0, 0.0, 0.0

    # Execute Flight Command via MAVSDK Offboard mode
    print("[FLIGHT] Initializing Offboard Mode Protocols...")
    # Offboard mode requires sending a baseline setpoint before starting
    await drone.offboard.set_velocity_body_yawspeed(VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0))

    try:
        await drone.offboard.start()
    except OffboardError as error:
        print(f"[CRITICAL] Offboard mode failed to start: {error._result.result}. Aborting loop.")
        return

    print(f"[EXECUTION] Mon-Drone-Ultra moving: Forward={forward}m/s, Right={right}m/s, Yaw={yaw}deg/s")
    # Feed Gemini's translated parameters directly into the physical flight dynamics
    await drone.offboard.set_velocity_body_yawspeed(VelocityBodyYawspeed(forward, right, 0.0, yaw))
    
    # Run the tactic for 5 seconds, then safely stabilize
    await asyncio.sleep(5)
    
    print("[FLIGHT] Tactic complete. Disengaging offboard controls and entering stable hover.")
    await drone.offboard.set_velocity_body_yawspeed(VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0))
    await asyncio.sleep(2)
    await drone.offboard.stop()

if __name__ == "__main__":
    asyncio.run(run_ai_drone_loop())
# Simplified Logic Example
async def monitor_power(drone):
    # Retrieve battery and solar input stats via MAVLink
    battery_level = await drone.telemetry.battery()
    solar_input = get_solar_voltage() # Custom sensor readout
    
    if battery_level < 20 and solar_input < threshold:
        # Gemini forced to prioritize energy saving
        await set_projector_state(OFF)
        await fly_to_home()
        

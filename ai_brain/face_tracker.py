import asyncio
import cv2
import face_recognition
from google import genai
from google.genai import types
from mavsdk import System
from mavsdk.offboard import VelocityBodyYawspeed, OffboardError

class MonDroneTracker:
    def __init__(self):
        # 1. Initialize Gemini Client for high-level tactical updates
        self.ai_client = genai.Client()
        self.drone = System()
        
        # 2. Mock database of authorized faces
        self.known_face_encodings = []
        self.known_face_names = ["Master Operator"]
        
        # Target resolution metrics
        self.FRAME_WIDTH = 640
        self.FRAME_HEIGHT = 480
        self.CENTER_X = self.FRAME_WIDTH // 2
        
    async def connect_drone(self):
        print("[FLIGHT] Pairing face tracker node with PX4...")
        await self.drone.connect(system_address="udp://:14540")
        async for state in self.drone.core.connection_state():
            if state.is_connected:
                print("[FLIGHT] Telemetry stream verified.")
                break

    async def trigger_gemini_alert(self, unknown_frame):
        """Dispatches an alert image to Gemini if an intruder is detected."""
        print("[AI-BRAIN] Intruder detected! Dispatching frames to Gemini...")
        
        _, buffer = cv2.imencode('.jpg', unknown_frame)
        image_bytes = buffer.tobytes()
        
        prompt = "Security Alert: Mon-Drone-Ultra face-tracking caught an unauthorized entity. Analyze expression and posture for threat level."
        
        response = self.ai_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
                prompt
            ]
        )
        print(f"\n--- [GEMINI SECURITY VERDICT] ---\n{response.text}\n---------------------------------\n")

    async def tracking_loop(self):
        video_capture = cv2.VideoCapture(0)
        video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.FRAME_WIDTH)
        video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.FRAME_HEIGHT)

        print("[TRACKER] Active. Initializing target acquisition sequence...")
        
        await self.drone.offboard.set_velocity_body_yawspeed(VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0))
        try:
            await self.drone.offboard.start()
        except OffboardError as e:
            print(f"[ERROR] Offboard start failed: {e}")
            return

        try:
            while True:
                ret, frame = video_capture.read()
                if not ret:
                    await asyncio.sleep(0.01)
                    continue

                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                face_locations = face_recognition.face_locations(rgb_frame)
                face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

                yaw_speed = 0.0
                forward_velocity = 0.0

                for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                    # Tracking Logic: P-Controller
                    face_center_x = (left + right) // 2
                    pixel_error_x = face_center_x - self.CENTER_X
                    yaw_speed = float(pixel_error_x * 0.15)
                    yaw_speed = max(min(yaw_speed, 30.0), -30.0)
                    
                    # Depth approximation
                    face_height = bottom - top
                    if face_height < 100:
                        forward_velocity = 0.5 
                    elif face_height > 180:
                        forward_velocity = -0.5
                    
                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                    name = "UNKNOWN INTRUDER"

                    if True in matches:
                        first_match_index = matches.index(True)
                        name = self.known_face_names[first_match_index]
                    else:
                        asyncio.create_task(self.trigger_gemini_alert(frame.copy()))

                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                    cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)

                await self.drone.offboard.set_velocity_body_yawspeed(
                    VelocityBodyYawspeed(forward_velocity, 0.0, 0.0, yaw_speed)
                )

                cv2.imshow('Mon-Drone-Ultra HUD', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

                await asyncio.sleep(0.03)

        finally:
            video_capture.release()
            cv2.destroyAllWindows()
            await self.drone.offboard.stop()

async def main():
    tracker = MonDroneTracker()
    await tracker.connect_drone()
    await tracker.tracking_loop()

if __name__ == "__main__":
    asyncio.run(main())

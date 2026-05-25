import asyncio
import os
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from mavsdk import System
from mavsdk.offboard import OffboardError, VelocityBodyYawspeed

# Define the exact structure you want the drone to return
class DroneCommand(BaseModel):
    FORWARD_VELOCITY: float = Field(description="Velocity forward/backward between -2.0 and 2.0 m/s")
    RIGHT_VELOCITY: float = Field(description="Velocity right/left between -2.0 and 2.0 m/s")
    YAW_SPEED: float = Field(description="Yaw speed between -45.0 and 45.0 deg/s")
    ACTION_LOG: str = Field(description="Brief phrase explaining the tactical choice")

async def analyze_scene_with_gemini(client: genai.Client, situation_brief: str) -> DroneCommand:
    """
    Sends the flight telemetry to Gemini to determine autonomous 
    tactical movement vectors for Mon-Drone-Ultra.
    """
    print("[AI-BRAIN] Consulting Gemini VLM...")
    
    prompt = f"""
    You are the central brain of Mon-Drone-Ultra, an autonomous drone 
    equipped with a 60-inch projector and face recognition. 
    Current Situation: {situation_brief}
    """

    # Request Gemini to return data strictly matching our Pydantic class
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=DroneCommand,
            temperature=0.1 # Low temperature ensures tighter adherence to limits
        )
    )
    
    # The SDK automatically parses the JSON text back into your Python object
    return response.parsed

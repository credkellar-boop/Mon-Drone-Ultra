import RPi.GPIO as GPIO # Or jetson.gpio
import asyncio

# Setup pins
PROJECTOR_PIN = 17
AMP_PIN = 27

def setup_hardware():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PROJECTOR_PIN, GPIO.OUT)
    GPIO.setup(AMP_PIN, GPIO.OUT)

def set_payload(device: str, state: bool):
    pin = PROJECTOR_PIN if device == "projector" else AMP_PIN
    GPIO.output(pin, GPIO.HIGH if state else GPIO.LOW)
    print(f"[HARDWARE] {device} set to {'ON' if state else 'OFF'}")

# Example logic to integrate with your dashboard:
# You would use a lightweight Message Broker like MQTT to pass 
# toggle signals from your Streamlit app to this script.

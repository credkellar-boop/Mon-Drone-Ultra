import asyncio
from mavsdk import System

# Configuration for your specific power setup
MIN_BATTERY_VOLTAGE = 14.2  # Set this to your safe minimum (e.g., 3.6V per cell)
MAX_VOLTAGE_FLUX = 0.5      # Max allowed fluctuation in Volts

async def run_safety_gate():
    drone = System()
    print("[SYSTEM] Initializing Mon-Drone-Ultra Safety Gate...")
    await drone.connect(system_address="udp://:14540")

    print("[SYSTEM] Waiting for MAVLink connection...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("[SYSTEM] MAVLink Link Established.")
            break

    # Safety Check: Telemetry Health
    print("[CHECK] Validating sensors and GPS...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("[PASS] GPS and Navigation sensors are healthy.")
            break
        else:
            print("[FAIL] Navigation sensors NOT ready. Check GPS/Compass.")
            return

    # Safety Check: Power Bus Stability
    print("[CHECK] Monitoring Power Bus stability...")
    battery_samples = []
    
    # Take 5 readings to ensure the voltage is stable
    for i in range(5):
        async for battery in drone.telemetry.battery():
            battery_samples.append(battery.voltage_v)
            break
        await asyncio.sleep(0.5)
    
    avg_voltage = sum(battery_samples) / len(battery_samples)
    voltage_diff = max(battery_samples) - min(battery_samples)

    if avg_voltage < MIN_BATTERY_VOLTAGE:
        print(f"[CRITICAL] Voltage low: {avg_voltage:.2f}V. Aborting.")
        return
    elif voltage_diff > MAX_VOLTAGE_FLUX:
        print(f"[CRITICAL] Power instability detected (Fluctuation: {voltage_diff:.2f}V). Check your BEC/PDB.")
        return
    else:
        print(f"[PASS] Power Bus Stable at {avg_voltage:.2f}V.")

    print("[SUCCESS] Mon-Drone-Ultra is safe to operate.")
    print(">>> STANDBY FOR MISSION COMMANDS <<<")

if __name__ == "__main__":
    asyncio.run(run_safety_gate())

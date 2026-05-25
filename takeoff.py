import asyncio
from mavsdk import System

async def run():
    # Initialize the Mon-Drone-Ultra system
    drone = System()
    
    print("Connecting to Mon-Drone-Ultra SITL...")
    # udp://:14540 is the default connection port for PX4 SITL
    await drone.connect(system_address="udp://:14540")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("-- Connected to drone!")
            break

    print("Waiting for drone to establish GPS lock...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("-- GPS lock acquired!")
            break

    print("-- Arming Motors")
    await drone.action.arm()

    print("-- Taking Off")
    await drone.action.takeoff()

    # Hover in the air for 10 seconds
    print("Hovering for 10 seconds...")
    await asyncio.sleep(10)

    print("-- Landing")
    await drone.action.land()

if __name__ == "__main__":
    # Execute the asynchronous event loop
    asyncio.run(run())

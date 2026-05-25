import json
import time
import csv

def log_flight_data(data_packet):
    """
    Archives state to local disk for post-flight analysis.
    """
    timestamp = time.strftime("%Y-%m-%d-%H-%M-%S")
    filename = f"flight_logs/log_{timestamp}.json"
    
    with open(filename, 'a') as f:
        json.dump(data_packet, f)
        f.write('\n')

# Example payload to log during your flight loop:
# log_flight_data({
#     "timestamp": context['timestamp'],
#     "weather": context['weather'],
#     "ai_decision": gemini_decision,
#     "battery": battery.voltage_v,
#     "location": [lat, lon]
# })

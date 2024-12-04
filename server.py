# 10.39.95.178

import socket
import pymongo
import datetime

# Helper function to get the device UID
def get_device_uid(device_name):
    DEVICE_UIDS = {
        "Smart TV": "735-48k-8fh-3mm",
        "Dishwasher": "4y3-p18-5zm-l53",
        "Refrigerator": "9k1-wi7-m6z-f0x"
    }
    return DEVICE_UIDS.get(device_name)

# Query 1: Average Moisture in Fridges
def query_one(meta, virtual):
    fridge1_uid = get_device_uid("Refrigerator")

    if not fridge1_uid:
        return "Error: Metadata for refrigerator is missing. Cannot process query."

    current_time = datetime.datetime.now(datetime.timezone.utc)
    three_hours_ago = current_time - datetime.timedelta(hours=3)

    fridge1_query = {
        "payload.parent_asset_uid": fridge1_uid,
        "time": {"$gte": three_hours_ago, "$lte": current_time}
    }

    fridge1_docs = virtual.find(fridge1_query)

    total_docs = 0
    total_moisture = 0

    for doc in fridge1_docs:
        moisture = doc.get("payload", {}).get("Moisture Meter - Moisture-ref")
        if moisture:
            total_docs += 1
            total_moisture += float(moisture)

    if total_docs == 0:
        return "No moisture data found for the past three hours."

    avg_moisture = total_moisture / total_docs
    return f"The average relative humidity (RH%) inside the kitchen fridge in the past three hours is {avg_moisture:.2f}%."

# Query 2: Average Water Usage in Dishwasher
def query_two(meta, virtual):
    # Use the confirmed assetUid for Smart Dishwasher
    dishwasher_uid = "4y3-p18-5zm-l53"

    current_time = datetime.datetime.now(datetime.timezone.utc)
    three_hours_ago = current_time - datetime.timedelta(hours=3)

    # Query dishwasher documents in the last 3 hours
    dishwasher_query = {
        "payload.parent_asset_uid": dishwasher_uid,
        "time": {"$gte": three_hours_ago, "$lte": current_time}
    }

    dishwasher_docs = virtual.find(dishwasher_query)

    total_cycles = 0
    total_water = 0

    for doc in dishwasher_docs:
        # Access the Water Flow Sensor field
        water_usage = doc.get("payload", {}).get("Water Flow Sensor")
        if water_usage:
            total_cycles += 1
            total_water += float(water_usage)

    if total_cycles == 0:
        return "No water usage data found for the past three hours."

    avg_water = total_water / total_cycles
    return f"The average water consumption per cycle in the smart dishwasher is {avg_water:.2f} gallons."

# Query 3: Highest Electricity Consumption
def query_three(meta, virtual):
    devices = ["Smart TV", "Dishwasher", "Refrigerator"]
    max_consumption = 0
    max_device = ""

    current_time = datetime.datetime.now(datetime.timezone.utc)
    three_hours_ago = current_time - datetime.timedelta(hours=3)

    for device in devices:
        device_uid = get_device_uid(device)
        if not device_uid:
            continue

        query = {
            "payload.parent_asset_uid": device_uid,
            "time": {"$gte": three_hours_ago, "$lte": current_time}
        }

        docs = virtual.find(query)

        # Use correct field names for electricity data
        electricity_field = {
            "Smart TV": "Ammeter-tv",
            "Dishwasher": "Ammeter-dish",
            "Refrigerator": "Ammeter-ref"
        }[device]

        total_consumption = sum(float(doc.get("payload", {}).get(electricity_field, 0)) for doc in docs)
        if total_consumption > max_consumption:
            max_consumption = total_consumption
            max_device = device

    if max_device == "":
        return "No electricity usage data found for the past three hours."

    return f"The device that consumed the most electricity is {max_device} with {max_consumption:.2f} kWh."

# Main server logic
if __name__ == "__main__":
    cluster = pymongo.MongoClient("mongodb+srv://smitlila7:Smit7339@cluster0.6qrps.mongodb.net/")
    database = cluster["test"]
    metadata = database["DataBase_metadata"]
    virtual = database["DataBase_virtual"]

    print("Initializing Server")
    server_ip = input("Enter the IP address to bind the server: ")
    server_port = int(input("Enter the port to bind the server: "))
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))
    server_socket.listen(1)
    print(f"Server is listening on {server_ip}:{server_port}")

    incoming_socket, incoming_address = server_socket.accept()
    max_bytes = 1024

    while True:
        incoming = incoming_socket.recv(max_bytes)
        client_message = incoming.decode()
        print(f"Client message: {client_message}")
        result = ''

        if client_message == '1':
            result = query_one(metadata, virtual)
        elif client_message == '2':
            result = query_two(metadata, virtual)
        elif client_message == '3':
            result = query_three(metadata, virtual)
        else:
            result = "Invalid query. Please try one of the valid queries."

        incoming_socket.send(bytearray(str(result), encoding='utf-8'))

    incoming_socket.close()
    print("Connection with the client is now closed")

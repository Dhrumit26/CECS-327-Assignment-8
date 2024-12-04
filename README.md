
# IoT System: End-to-End Implementation

This README explains how to set up and run the client-server IoT system to process user queries related to IoT devices, leveraging TCP communication and MongoDB.

## Prerequisites

Ensure you have the following installed on your system:
1. **Python 3.8+** (for running the client and server scripts)
2. **pip** (Python package manager)
3. **MongoDB** (or access to the MongoDB Atlas cluster)
4. **Required Python Libraries**:
   - `socket`
   - `pymongo`
   - `ipaddress`
   - `datetime`

## Files in this Repository

1. **`client.py`**: The TCP client script for sending user queries to the server.
2. **`server.py`**: The TCP server script for processing queries and retrieving data from MongoDB.
3. **IoT Database Configuration**: The MongoDB cluster stores IoT metadata and device data.

---

## Setup Instructions

### 1. MongoDB Configuration

1. Access your MongoDB Atlas cluster (or your local MongoDB instance).
2. Create the following collections in a database named `test`:
   - `DataBase_metadata`: Stores metadata for IoT devices.
   - `DataBase_virtual`: Stores IoT sensor data, including moisture, water usage, and electricity consumption.
3. Populate the collections with the required data. Ensure that:
   - `DataBase_virtual` includes fields such as `Moisture Meter - Moisture-ref`, `Water Flow Sensor`, and `Ammeter-*`.
   - Each record has a `payload.parent_asset_uid` field linking it to the device's UID.

---

### 2. Install Python Dependencies

Run the following command to install the required Python libraries:

```bash
pip install pymongo
```

---

### 3. Start the Server

1. Navigate to the directory containing `server.py`.
2. Run the server script:

```bash
python server.py
```

3. Enter the server's IP address and port when prompted. For example:

   ```
   Enter the IP address to bind the server: 127.0.0.1
   Enter the port to bind the server: 12345
   ```

   The server will initialize and listen for incoming client connections.

---

### 4. Run the Client

1. Open a new terminal and navigate to the directory containing `client.py`.
2. Run the client script:

```bash
python client.py
```

3. Enter the server's IP address and port to establish a connection. These must match the server's configuration.
4. Follow the on-screen prompts to submit one of the following queries:
   - **Query 1**: Average moisture in the kitchen fridge in the past three hours.
   - **Query 2**: Average water consumption per cycle in the smart dishwasher.
   - **Query 3**: Device with the highest electricity consumption in the past three hours.

---

### 5. Query Output

The server processes the query using MongoDB and sends the results back to the client. Results are displayed in the client terminal. For example:

- **Query 1 Result**: "The average relative humidity (RH%) inside the kitchen fridge in the past three hours is 45.67%."
- **Query 2 Result**: "The average water consumption per cycle in the smart dishwasher is 3.12 gallons."
- **Query 3 Result**: "The device that consumed the most electricity is Refrigerator with 5.67 kWh."

---

## Notes and Assumptions

1. Ensure that the MongoDB cluster contains realistic data that matches the expected query structure.
2. Queries that cannot be processed will return an error message and prompt the user to try again.
3. The system is configured to work in PST and provide results in imperial units.

---

## Troubleshooting

- **Connection Issues**:
  - Verify the server's IP address and port match those provided in the client.
  - Ensure MongoDB is accessible and properly configured.

- **Data Not Found**:
  - Populate MongoDB collections with test data for realistic responses.

---

Feel free to contact the development team if you encounter any issues or need further assistance. Happy coding!

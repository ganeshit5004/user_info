from flask import Flask, jsonify
import win32com.client
import platform
import uuid
import socket
import os
import pythoncom

app = Flask(__name__)

def get_device_id():
    """
    Function to get the device ID using Windows Management Instrumentation (WMI).
    It uses the 'WbemScripting.SWbemLocator' to access system information.
    """
    try:
        # Initialize COM for the current thread
        pythoncom.CoInitialize()
        
        # Create WMI locator object
        obj = win32com.client.Dispatch("WbemScripting.SWbemLocator")
        service = obj.ConnectServer(".", "root\\cimv2")
        
        # Query the WMI service for computer system product information
        for item in service.ExecQuery("Select * from Win32_ComputerSystemProduct"):
            return item.UUID  # Return the Device ID (UUID)
    
    except Exception as e:
        return f"Error retrieving Device ID: {e}"

def get_device_info():
    """
    Collects various device information including OS, hardware UUID, device name, user details, etc.
    """
    try:
        device_info = {
            "Device ID": get_device_id(),  # Device ID using Win32 API
            "Hardware UUID": uuid.getnode(),  # Unique hardware address (MAC address)
            "Device Name": platform.node(),  # Hostname of the device
            "Operating System": platform.system(),  # OS name (e.g., Windows, Linux, Darwin)
            "OS Version": platform.version(),  # Detailed OS version
            "OS Release": platform.release(),  # Release version (e.g., 10, 20.04)
            "User Name": os.getlogin(),  # Current logged in user
            "Machine IP Address": socket.gethostbyname(socket.gethostname())  # IP address of the machine
        }
        return device_info
    
    except Exception as e:
        return {"Error": str(e)}

@app.route("/")
def home():
    """
    Home route for the API, provides a welcome message.
    """
    return "Welcome to the Device Info API!"

@app.route("/device-info", methods=["GET"])
def device_info():
    """
    API endpoint to get detailed device information, including Device ID, Hardware UUID, etc.
    """
    info = get_device_info()
    return jsonify(info)

if __name__ == "__main__":
    # Run the Flask application
    app.run(debug=True, host="0.0.0.0", port=5000)


# 🐾 Smart Pet Health and Vaccination Monitoring System

A web-based platform for managing pet healthcare records, vaccination information, QR-code-based identification, and IoT-enabled activity monitoring.

## 📌 Project Overview

The Smart Pet Health and Vaccination Monitoring System aims to simplify pet healthcare management by bringing essential pet information into one centralised digital platform.

Pet healthcare information is often scattered across vaccination cards, paper documents, messages, and separate records. This makes it difficult for owners to organise medical histories, track vaccination schedules, and access updated information when required.

This project addresses these challenges through a web application that enables pet registration, digital health record management, QR-based identification, and motion-related activity monitoring using an IoT wearable prototype.

## 🎯 Objectives

- Provide digital registration and unique identification for pets.
- Maintain centralised digital health records.
- Manage vaccination, medication, and treatment information.
- Enable quick pet profile access through QR codes.
- Support vaccination schedules and healthcare follow-ups.
- Integrate an ESP32-based wearable for activity monitoring.
- Store and display activity readings through a cloud-connected platform.

## ✨ Key Features

### 1. Digital Pet Registration
- Register pets with their essential details.
- Generate a unique identification number for each pet.
- Maintain individual digital pet profiles.

### 2. QR Code-Based Identification
- Generate a QR code linked to a pet's unique ID.
- Scan the QR code using a smartphone.
- Access the corresponding digital pet profile.

### 3. Digital Health Records
- Maintain centralised healthcare information.
- Record vaccination details.
- Maintain medication and treatment records.
- Store relevant health history.

### 4. Vaccination and Healthcare Management
- Maintain vaccination schedules and records.
- Organise healthcare information.
- Support tracking of important healthcare follow-ups and reminders.

### 5. IoT-Based Activity Monitoring
- Integrate an ESP32 development board with an MPU6050 motion sensor.
- Capture motion-related readings using the accelerometer and gyroscope.
- Transmit sensor readings through Wi-Fi.
- Store readings in the PostgreSQL database.
- Display the latest activity information on the web dashboard.

**Note:** The current prototype captures motion-related readings. It is not a medical diagnostic device and does not independently measure heart rate, body temperature, or other clinical parameters.

### 6. Cloud-Based Access
- Host the web application using Render.
- Store application data using Neon PostgreSQL.
- Access the application through a public web address.

## 🛠️ Technology Stack

| Category | Technology |
|---|---|
| Programming Language | Python |
| Backend Framework | Flask |
| Frontend | HTML, CSS, JavaScript |
| Database | PostgreSQL |
| Database Hosting | Neon |
| Database Adapter | Psycopg2 |
| Application Hosting | Render |
| Microcontroller | ESP32 |
| Motion Sensor | MPU6050 |
| Communication | HTTP API |
| Sensor Interface | I²C |
| Version Control | Git and GitHub |

## 🏗️ System Architecture

The system consists of three main layers:

**Frontend Layer**
- Provides the user interface for pet registration and healthcare management.
- Displays pet profiles, health records, and activity readings.
- Allows users to access pet information through QR-code links.

**Backend and Database Layer**
- Flask handles application requests and API communication.
- The backend processes incoming sensor data.
- Psycopg2 connects Python to PostgreSQL.
- Neon PostgreSQL stores pet information, healthcare records, and activity readings.

**IoT Hardware Layer**
- MPU6050 captures acceleration and angular velocity.
- ESP32 reads sensor data through the I²C interface.
- ESP32 uses Wi-Fi to transmit readings to the Flask API.
- The backend stores the received readings in PostgreSQL.

### Activity Data Flow

```text
MPU6050 Motion Sensor
         |
         | I²C
         v
    ESP32 Board
         |
         | Wi-Fi / HTTP POST
         v
    Flask Backend
         |
         v
 PostgreSQL Database
         |
         v
    Web Dashboard
```

## 🔄 Application Workflow

1. **Register:** The pet owner registers a pet through the web application.
2. **Identify:** The system assigns a unique identification number.
3. **Generate:** A QR code is associated with the pet profile.
4. **Access:** Scanning the QR code opens the corresponding pet profile.
5. **Record:** Healthcare information is maintained digitally.
6. **Monitor:** The ESP32 and MPU6050 capture motion-related readings.
7. **Transmit:** Sensor readings are sent to the backend using an HTTP API.
8. **Store:** The backend stores the readings in PostgreSQL.
9. **Display:** The dashboard retrieves and displays the latest activity information.

## 💻 Getting Started

Follow these steps to run the project locally.

### Prerequisites

- Python 3.10 or later
- pip (Python package manager)
- Git
- Visual Studio Code
- PostgreSQL database access

For hardware activity monitoring:

- ESP32 development board
- MPU6050 sensor
- Jumper wires
- USB cable and suitable power source

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Navigate to the project directory:

```bash
cd YOUR_PROJECT_FOLDER
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Database

1. Create or select a Neon PostgreSQL project.
2. Obtain the PostgreSQL connection details.
3. Configure the database credentials using the environment variables or configuration method expected by the application.
4. Ensure the required database tables are available.

**Important:** Never upload database passwords, secret keys, or private connection strings to GitHub.

### 5. Run the Application

From the project root directory, execute:

```bash
python -m src.main
```

Open the local URL displayed by the Flask server in your browser.

## 🔌 Hardware Integration

The activity monitoring unit uses an ESP32 and an MPU6050 sensor.

### MPU6050 to ESP32 Connections

| MPU6050 Pin | ESP32 Connection |
|---|---|
| VCC | 3.3V |
| GND | GND |
| SDA | GPIO 21 |
| SCL | GPIO 22 |

*These are typical ESP32 I²C connections. Verify the pin configuration for your board.*

### Hardware Working Principle

1. MPU6050 detects motion using its three-axis accelerometer and gyroscope.
2. ESP32 reads sensor values through I²C.
3. ESP32 connects to a Wi-Fi network.
4. Sensor readings are transmitted using an HTTP POST request.
5. Flask receives and processes the readings.
6. The readings are stored in PostgreSQL.
7. The dashboard retrieves and displays the latest readings.

**API Endpoint:**

`/api/activity`

## ☁️ Deployment

The project uses the following cloud services:

| Component | Platform |
|---|---|
| Web Application Hosting | Render |
| Database Hosting | Neon PostgreSQL |
| Source Code Management | GitHub |

**Live Application:**  
https://smartpethealthsystem.onrender.com

## 🔐 Security Considerations

- Store database credentials securely.
- Exclude sensitive configuration files from version control.
- Validate incoming API requests.
- Use HTTPS for production deployment.
- Apply appropriate access controls to personal and healthcare information.

## 🚀 Future Enhancements

The following features are proposed for future development and are not part of the current implemented prototype:

- **GPS Tracking:** Enable location tracking to help owners locate their pets.
- **NFC-Based Identification:** Introduce NFC tags as an additional identification method.
- **Lost Pet Support:** Develop a mechanism to assist in identifying and recovering lost pets.
- **Advanced Activity Classification:** Use signal processing or machine learning to identify movement patterns.
- **Mobile Application:** Develop a dedicated mobile application.
- **Enhanced Notifications:** Introduce advanced reminders and notification functionality.
- **Improved Wearable Design:** Improve battery life, durability, and comfort.

## 💰 Estimated Prototype Budget

| Component | Estimated Cost (INR) |
|---|---:|
| ESP32 Development Board | ₹400–₹700 |
| MPU6050 Sensor | ₹100–₹200 |
| Collar / Wearable Casing | ₹200–₹400 |
| Jumper Wires and Connectors | ₹100–₹200 |
| Power Supply / Battery | ₹200–₹400 |
| QR Code Printing | ₹50–₹100 |
| Miscellaneous Components | ₹200–₹300 |
| **Estimated Total** | **₹1,250–₹2,300** |

*These are indicative estimates and may vary depending on suppliers and component availability. Software tools and initial free cloud-service tiers are excluded.*

## 🎓 Project Information

| Detail | Description |
|---|---|
| Project Title | Smart Pet Health and Vaccination Monitoring System |
| Project ID | ASIP-103 |
| Domain | IoT / Web Development / Pet Healthcare |
| Backend | Python Flask |
| Database | PostgreSQL |
| Hardware | ESP32 and MPU6050 |
| Deployment | Render and Neon |

## 👥 Contributors

Add the names of your project team members and their respective contributions here.

## 📄 License

This project is developed for academic and educational purposes. An appropriate open-source license can be added if the project is intended for public reuse and distribution.

---

**Smart Pet Health and Vaccination Monitoring System**

*Making pet healthcare records more accessible, organised, and connected.*

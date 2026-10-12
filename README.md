# 🚗 Intelli Park Map View

**Smart Parking Navigation System | Final Year Project**

Intelli Park Map View is a team-based project designed to simplify parking navigation by identifying available parking slots and finding the shortest path to a suitable slot using the **A* Search Algorithm**. The project combines a web interface with Python-based parking navigation and visual mapping.

## ✨ Key Features

- 🅿️ **Parking Slot Visualization** – Displays parking slots and their availability.
- 🗺️ **Shortest Path Navigation** – Uses the A* search algorithm to find an efficient route to a parking slot.
- 📍 **Slot Selection** – Identifies a suitable available parking slot.
- 📱 **QR Code Navigation** – Generates a QR code to access the uploaded navigation map.
- 🌐 **Web Interface** – Provides a visual interface for the parking project.

## 🛠️ Technologies Used

- **Frontend:** HTML, CSS, JavaScript
- **Programming Language:** Python
- **Libraries:** OpenCV, NumPy, Requests, QRCode
- **Algorithm:** A* Search Algorithm
- **Cloud Image Hosting:** ImgBB API

## ⚙️ How It Works

1. The system loads the parking background image and creates a parking grid.
2. Available parking slots are identified.
3. The A* search algorithm calculates a shortest path to an available slot.
4. The selected slot and navigation path are visualized on the parking map.
5. The map is uploaded to cloud image hosting, and a QR code is generated for access.

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- A modern web browser
- Required Python libraries

### Installation

Clone this repository:

```bash
git clone https://github.com/Ritchie06/Intellipark-mapview.git
cd Intellipark-mapview
```

Install the Python dependencies:

```bash
pip install opencv-python numpy requests qrcode[pil]
```

Ensure the parking background image `grnddd2.png` is available in the project directory.

Configure your ImgBB API key in the Python script, then run:

```bash
python parking_navigation.py
```

Open `index.html` in your browser to view the website.

> **Note:** The Python navigation script and website may run independently unless connected through a backend. The QR-code workflow also requires a valid ImgBB API key and an internet connection.

## 👩‍💻 Team Project

This project was developed collaboratively by a **team of four members** as our final-year engineering project.

- Team Size: 4 Members
- Project Type: Final-Year Academic Project
- Domain: Smart Parking and Navigation

## 🎯 Project Goal

To explore how pathfinding algorithms, visual mapping, and web technologies can help make parking navigation more efficient and user-friendly.

---

⭐ If you find this project interesting, feel free to explore the repository and its implementation.

**Developed as a Final-Year Team Project.**

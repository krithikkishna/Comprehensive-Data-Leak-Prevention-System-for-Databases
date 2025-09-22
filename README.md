# Comprehensive-Data-Leak-Prevention-System-for-Databases

This project is a full-stack security application designed to demonstrate a multi-layered approach to data leak prevention. It features a web-based frontend for data submission, a secure backend with a MySQL database, and a Python-based network firewall for real-time traffic analysis and threat mitigation.

---

## Table of Contents
* [Features](#features)
* [System Architecture](#system-architecture)
* [Technologies Used](#technologies-used)
* [Live Demo](#live-demo)
* [Local Setup and Installation](#local-setup-and-installation)
  * [Backend Server (Windows)](#backend-server-windows)
  * [Firewall (Kali Linux VM)](#firewall-kali-linux-vm)
* [Usage](#usage)
* [Author](#author)

---

## Features

*   **Secure Data Entry:** A clean, user-friendly web form for submitting user data.
*   **Robust Backend Server:** A Node.js and Express server handles data validation and securely communicates with the database.
*   **MySQL Database Storage:** User data is stored in a structured and reliable MySQL database.
*   **Real-Time Network Firewall:** A powerful Python firewall using `iptables` and `NetfilterQueue` to inspect and filter network packets based on custom rules.
*   **Configurable Security Rules:** Firewall rules (banned IPs, ports, and prefixes) are managed in an external `firewall_rules.json` file.
*   **Anomaly Detection:** Includes a basic algorithm to detect and block ICMP (ping) flood attacks.

---

## System Architecture

This project is composed of three main components that work together:

1.  **Frontend:** A static HTML form served to the user for data input.
2.  **Backend:** A Node.js server that listens for form submissions, processes the data, and saves it to a MySQL database.
3.  **Firewall:** A Python script running in a separate Linux environment that uses `iptables` to intercept network traffic and applies custom rules to block potential threats.

---

## Technologies Used

*   **Frontend:** HTML5, CSS3
*   **Backend:** Node.js, Express.js
*   **Database:** MySQL
*   **Firewall:** Python, Scapy, NetfilterQueue
*   **Hosting:** GitHub Pages (Frontend), Render (Backend & DB)

---

## Live Demo

*   **Frontend Application:** `(https://github.com/krithikkishna/Comprehensive-Data-Leak-Prevention-System-for-Databases/tree/main/frontend)`
*   **Backend Server:** Hosted on Render. The live frontend is configured to send data to this server.
---

## Local Setup and Installation

To run this project locally, you will need to run the backend and the firewall in separate environments.

### Backend Server (Windows)

1.  **Clone the repository:**
    ```
    git clone https://github.com/krithikkishna/Comprehensive-Data-Leak-Prevention-System-for-Databases.git
    cd Comprehensive-Data-Leak-Prevention-System-for-Databases/backend
    ```
2.  **Install dependencies:**
    ```
    npm install
    ```
3.  **Set up your MySQL database:**
    *   Ensure you have a MySQL server running.
    *   Create a database named `dataguard`.
    *   Update the credentials in `backend/server.js` with your MySQL username and password.
4.  **Start the server:**
    ```
    npm start
    ```
    The server will be running at `http://localhost:5501`.

### Firewall (Kali Linux VM)

The firewall component requires a full Linux kernel and cannot be run on WSL without a custom kernel. A Kali Linux VM is the recommended environment.

1.  **Transfer the `firewall` directory** to your Kali Linux machine.
2.  **Install dependencies:**
    ```
    sudo apt update
    sudo apt install -y python3-pip build-essential python3-dev libnetfilter-queue-dev iptables python3-scapy
    sudo pip install --break-system-packages NetfilterQueue
    ```
3.  **Configure `iptables`:**
    *   Switch to legacy mode: `sudo update-alternatives --config iptables` (and select the 'legacy' option).
    *   Create the capture rule: `sudo iptables -A INPUT -j NFQUEUE --queue-num 1`
4.  **Run the firewall:**
    ```
    cd /path/to/firewall
    sudo python3 firewall.py
    ```

---

## Usage

1.  Ensure both the backend server and the firewall script are running.
2.  Navigate to `http://localhost:5501` in your web browser.
3.  Submit data through the form to save it to the database.
4.  Generate network traffic on the Kali machine (e.g., `ping 8.8.8.8`) to see the firewall inspect packets in the terminal.

---

## Author

*   **Krithik Krishna M**
*   GitHub: [https://github.com/krithikrishna](https://github.com/krithikrishna)

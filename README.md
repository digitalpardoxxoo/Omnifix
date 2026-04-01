# OmniFix

Welcome to **OmniFix**! This is an autonomous IT support system designed to streamline issue resolution, act as a virtual helpdesk, and simulate various interactions. 

Whether you're exploring the repository for the first time or looking to contribute, this setup is designed to be accessible and straightforward.

## 🌟 Features

*   **Employee Portal**: A React frontend where users can submit tickets or view system status.
*   **Control Panel**: A separate React frontend designed for managers/admins to oversee all systems and handle operations.
*   **Python Backend**: The powerhouse API and orchestration engine that drives the data and autonomous workflows.

## 🚀 Getting Started

To get the project up and running locally, you'll need the following installed on your machine:
*   [Python](https://www.python.org/downloads/) (For the backend server)
*   [Node.js](https://nodejs.org/) (For running the React frontends)

### Running the Project

You can start the entire OmniFix system locally with just one file. We've included a handy `start.bat` script that boots up the entire environment for you!

**On Windows:**
1. Open the file explorer and go into the **OMNIFIX** folder.
2. Double-click the `start.bat` file to run it.
3. A terminal will open and show you the progress:
   - It will start the Python Backend on port 5000.
   - It will start the Employee App on port 3000.
   - It will start the Control Panel on port 3001.

Everything will automatically launch in your browser!

### Accessing the Portals
Once the project is running via the `start.bat` script, you can visit the following links:
*   **Employee Portal:** [http://localhost:3000](http://localhost:3000)
*   **Control Panel/Dashboard:** [http://localhost:3001](http://localhost:3001)

## 📁 Repository Structure

Here's a quick map to help you navigate:

*   **`/control_web`**: Contains the React code for the Admin/Manager Control panel.
*   **`/employee_web`**: Contains the React code for the Employee help portal.
*   **`app.py` / `Orchestrator` / `agents`**: The Python backend environment.
*   **`start.bat`**: The single starting script for Windows users.

---
*Created for efficiency, clarity, and next-generation IT support.*

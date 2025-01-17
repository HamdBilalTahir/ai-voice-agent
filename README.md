# AI Voice Agent

## Setup Instructions

To set up the project, follow these steps:

1. **Create a Virtual Environment**

   First, create a virtual environment to manage your project's dependencies. Run the following command in your terminal:

   ```bash
   python3 -m venv venv
   ```

   This will create a directory named `venv` in your project folder.

2. **Activate the Virtual Environment**

   Next, activate the virtual environment. Use the appropriate command for your operating system:

   - **macOS/Linux:**

     ```bash
     source venv/bin/activate
     ```

   - **Windows:**

     ```bash
     .\venv\Scripts\activate
     ```

3. **Install Requirements**

   With the virtual environment activated, install the required packages using the `requirements.txt` file:

   ```bash
   pip install -r requirements.txt
   ```

   This will install all the necessary dependencies for the project.

## Project Overview

This project is an AI Voice Agent designed to perform various tasks. Ensure you have all dependencies installed and the virtual environment activated before running the project.

## Running the Application

To run the application, use the following command:

```bash
uvicorn ai_voice_agent:app --reload
```

This command will start the application with automatic reloading enabled, allowing you to see changes without restarting the server manually.

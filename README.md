# Platform - Full Stack Application

This is the boilerplate for a comprehensive platform, built with Flask and React.

## Prerequisites
- Docker & Docker Compose
- Python 3.9+
- `pip` for installing Python packages
- Postgres Database

## How to Run

1.  **Install Python Dependencies:**
    Open your terminal in the project root (`card_platform/`) and install the `click` library for the setup script:
    ```bash
    pip install click python-dotenv
    ```

2.  **Configure Environment Variables:**
    Run the interactive setup script. It will securely prompt you for your secret keys and create the necessary `.env` file for the backend.
    ```bash
    python setup.py configure
    ```

3.  **Build and Run the Application:**
    Use Docker Compose to build the images and start the frontend, backend, and database containers.
    ```bash
    docker-compose up --build
    ```
    - The **Frontend** will be available at `http://localhost:3000`
    - The **Backend API** will be running at `http://localhost:5000`

4.  **Initialize the Database:**
    Once the containers are running, open a **new terminal window** and run the database setup command from the `setup.py` script. This executes the migration commands inside the running backend container.
    ```bash
    python setup.py db-init
    ```

The application is now fully set up and running!

## Project Structure

-   **`/backend`**: The Flask API.
-   **`/frontend`**: The React user interface.
-   **`/setup.py`**: A command-line utility for configuration and database management.
-   **`/docker-compose.yml`**: Orchestrates all the services.

# StockSaver

StockSaver is a web application built using FastAPI and SQLite that allows users to manage their inventory of images and associated metadata. It provides a user-friendly interface for uploading, editing, and managing images along with their details such as name, expiry date, category, and notes.

## Features

-   **Image Upload**: Users can upload images and store them in the database along with their metadata.
-   **Image Management**: Users can view, edit, and delete images from the inventory.
-   **Search**: Users can search for images based on keywords or metadata.
-   **Expiration Date Tracking**: Images can be marked with an expiry date, and the application can provide a list of images that are about to expire.
-   **Email Notifications**: Users can configure email notifications to be sent when images are about to expire.
-   **Authentication**: Users can authenticate using a simple username and password system.

## Technologies Used

-   **FastAPI**: A modern, fast (high-performance), web framework for building APIs with Python.
-   **SQLite**: A lightweight, serverless, and self-contained SQL database engine.
-   **Jinja2**: A template engine for Python that provides a simple and powerful way to generate dynamic HTML.
-   **HTMX**: A library for using HTML5 and CSS3 features to build interactive web applications using htmx attributes.
-   **Tailwind CSS**: A utility-first CSS framework for rapidly building custom user interfaces.

## Project Structure

The project consists of the following files and directories:

-   **app.py**: The main application file that sets up the FastAPI app and defines the routes.
-   **database.py**: Contains functions for interacting with the SQLite database.
-   **models.py**: Defines the data models used in the application.
-   **send.py**: Contains functions for sending email notifications.
-   **templates**: Contains HTML templates for rendering the application's views.
-   **static**: Contains static files such as CSS and JavaScript files.
-   **requirements.txt**: Lists the project's dependencies.

## Installation and Usage

To run the application locally, follow these steps:

1. Clone the repository: `git clone https://github.com/your-username/stock-saver.git`
2. Install the dependencies: `pip install -r requirements.txt`
3. Set up the SQLite database: `python database.py`
4. Run the application: `uvicorn app:app --reload`

The application will be accessible at `http://localhost:8000`.

## Contribution

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

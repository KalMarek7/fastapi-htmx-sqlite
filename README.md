# StockSaver

StockSaver is a web application built using FastAPI and HTMX that allows users to manage their inventory of images and associated metadata. It provides a user-friendly interface for uploading, editing, and managing images along with their details such as name, expiry date, category, and notes.

## Features

-   **Image Upload**: Users can upload images and store them in the database along with their metadata.
-   **Image Management**: Users can view, edit, and delete images from the inventory.
-   **Search**: Users can search for images based on keywords or metadata.
-   **Expiration Date Tracking**: Images can be marked with an expiry date, and the application can provide a list of images that are about to expire.
-   **Email Notifications**: Users can configure email notifications to be sent when images are about to expire.

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

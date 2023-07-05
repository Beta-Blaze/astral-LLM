# Flask Project Readme

This is a Flask project that provides a web application with various routes and functionalities. It utilizes the Flask framework and includes database integration using SQL Alchemy.

## Project Structure

The project has the following structure:

- `app.py`: This is the main file that creates the Flask application, initializes configurations, routes, and the database. It also runs the application.
- `config.py`: This file contains configuration settings for the Flask application, including the SQL Alchemy database URI and CORS configurations.
- `.gitignore`: This file specifies the files and directories that should be ignored by version control systems like Git.
- `Dockerfile`: This file is used to build a Docker image for the Flask application.
- `README.md`: This file provides information and instructions about the project.
- `requirements.txt`: This file lists the Python packages and their versions required to run the project.

The project directory also includes the following directories:

- `database/`: This directory contains the database related files.
  - `db.py`: This file defines functions for creating the database and tables using SQL Alchemy.
  - `model/`: This directory is a placeholder for the database model files. You can add your own models here.

- `instance/`: This directory is a placeholder for instance-specific files.
  - `__init__.py`: This file is an empty placeholder to make the directory a Python package.

- `resources/`: This directory contains resources used by the Flask application.
  - `config.py`: This file initializes the Flask application configurations.
  - `init_routes.py`: This file initializes the routes for the Flask application.

- `resources/routes/`: This directory contains the route handlers for different parts of the application.
  - `api.py`: This file defines routes and functions for handling API requests.
  - `pages.py`: This file defines routes and functions for rendering HTML pages.
  - `static.py`: This file defines routes and functions for serving static files.

- `static/`: This directory is used for storing static files like CSS, JavaScript, images, etc.
  - `favicon.ico`: This is the favicon file for the web application.

- `templates/`: This directory contains HTML templates used for rendering web pages.
  - `__init__.py`: This file is an empty placeholder to make the directory a Python package.

## Running the Application

To run the Flask application, follow these steps:

1. Install the required dependencies by running `pip install -r requirements.txt`.
2. Make sure you have SQLite installed on your system.
3. Create a virtual environment (optional but recommended).
4. Set up the Flask application configurations in `config.py`.
5. Run the following command in the project directory:

   ```shell
   python app.py
   ```

   This will start the Flask development server and the application will be accessible at `http://localhost:5000`.

## Docker Support

This project also includes a Dockerfile, which allows you to containerize the Flask application. To build and run the Docker image, follow these steps:

1. Make sure you have Docker installed on your system.
2. Open a terminal and navigate to the project directory.
3. Build the Docker image using the following command:

   ```shell
   docker build -t flask-app .
   ```

   This will build the Docker image with the tag `flask-app`.

4. Run the Docker container using the following command:

   ```shell
   docker run -p 5000:5000 flask-app
   ```

   This will start the Docker container and map port 5000 from the container to port 5000 on the host system. The application will be accessible at `http://localhost:5000`.

## Contributing



If you would like to contribute to this project, you can follow these steps:

1. Fork the repository on GitHub.
2. Clone the forked repository to your local machine.
3. Create a new branch for your changes.
4. Make the necessary changes and commit them.
5. Push the changes to your forked repository.
6. Submit a pull request to the original repository.

Please make sure to follow the existing code style and include tests for any new features or bug fixes.

## License

This project is licensed under the [MIT License](LICENSE). You are free to use, modify, and distribute the code as permitted by the license.
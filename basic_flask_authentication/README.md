# Basic Flask Authentication

This is a simple Flask web application that provides user authentication, including login, registration, and account management features. It uses Flask-Login for session management and SQLite for storing user credentials.

As a boilerplate template, you can copy this into your own directory, and work off of it.

## Endpoints

### Home (`/`)
- **Method**: GET
- **Description**: Renders the home page.

### Account (`/account`)
- **Method**: GET
- **Authentication Required**: Yes
- **Description**: Displays the user's account information, including username and account creation timestamp.

### Login (`/login`)
- **Method**: GET, POST
- **Description**: 
  - **GET**: Renders the login page.
  - **POST**: Authenticates the user based on username and password.

### Logout (`/logout`)
- **Method**: GET
- **Description**: Logs out the current user and redirects to the login page.

### Register (`/register`)
- **Method**: GET, POST
- **Description**: 
  - **GET**: Renders the registration page.
  - **POST**: Registers a new user with a username and password.

## Setup

To set up the application, follow these steps:

1. **Clone the repository**:

    ```bash
    git clone https://github.com/fosterhr/boilerplates
    cd boilerplates/basic_flask_authentication
    ```
    
2. **Create a virtual environment (optional but recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install required packages:**

    ```bash
    pip install Flask Flask-Login
    ```
    
4. **Create a `secret.key` file:**

    Create a file named `secret.key` in the root of the project directory and add a secret key to it.

5. **Run the application:**

    ```bash
    python app.py
    ```

6. **Access the application:**

    Open your web browser and navigate to ``http://localhost:80``.
    
## Secret Key Management

The application uses a secret key for session management, which is loaded from a file named secret.key. This key is essential for Flask's session handling and should be kept confidential.

- How to Store: Create a plain text file named `secret.key` in the root directory of your project. The file should contain a single line with your secret key.

## License

This project is licensed under the MIT License. See the LICENSE file for details.


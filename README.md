# FacturaApp

FacturaApp is a Django-based web application for managing client information and user authentication.

## Features

- User authentication with login and logout functionality.
- Client management with the ability to add, edit, and list clients.
- CSRF protection and Bootstrap styling for forms.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/facturaapp.git
    cd facturaapp
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Apply migrations:
    ```sh
    python manage.py migrate
    ```

5. Create a superuser:
    ```sh
    python manage.py createsuperuser
    ```

6. Run the development server:
    ```sh
    python manage.py runserver
    ```

## Usage

- Access the admin panel at `http://127.0.0.1:8000/admin/` to manage users and clients.
- Login at `http://127.0.0.1:8000/login/` and logout at `http://127.0.0.1:8000/logout/`.
- Manage clients at `http://127.0.0.1:8000/clients/`.

## Project Structure

- `facturapp/urls.py`: URL configuration for the project.
- `clients/urls.py`: URL configuration for the clients app.
- `templates/registration/login.html`: Template for the login page.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## License

This project is licensed under the MIT License.
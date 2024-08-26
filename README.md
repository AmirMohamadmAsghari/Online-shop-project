# Online Shop with Django

This project is an e-commerce web application built with Django, featuring a comprehensive set of functionalities including user authentication, product management, discount handling, and asynchronous task management with Celery. 

## Features

- **User Authentication**: Custom user model with registration, login, profile management, and password reset functionalities.
- **Product Management**: Product listing, searching, filtering by category, and reviews.
- **Discounts**: Apply discounts to products and manage discount codes.
- **Orders**: Create and manage orders, including the application of discount codes at checkout.
- **Asynchronous Tasks**: Background task handling with Celery and periodic tasks using Celery Beat.
- **Redis Integration**: Caching and Celery message broker and result backend using Redis.

## Project Screenshots

![Screenshot 1](assets/images/cart.png)
![Screenshot 2](assets/images/homepage.png)
![Screenshot 3](assets/images/login.png)


<h2>Project Screenshots</h2>

<p align="center">
  <img src="assets/images/homepage.png" alt="Screenshot 1" width="400" style="margin-right: 10px;">
  <img src="assets/images/login.png" alt="Screenshot 2" width="400" style="margin-right: 10px;">
  <img src="assets/images/cart.png" alt="Screenshot 3" width="400">
</p>

## Installation

### Prerequisites

- Python 3.8+
- Django 3.2+
- Redis
- Poetry
- Docker

### Setup

1. **Clone the repository:**

    ```sh
    git clone https://github.com/AmirMohamadmAsghari/Online-shop-project.git
    cd Online-shop-project
    ```

2. **Install dependencies using Poetry:**

    ```sh
    poetry install
    ```

3. **Activate the virtual environment:**

    ```sh
    poetry shell
    ```

4. **Environment variables:**

    Create a `.env` file in the root of your project and add the following configurations:

    
    ```env
    SECRET_KEY=your-secret-key
    DEBUG=True
    ALLOWED_HOSTS=localhost,127.0.0.1

    DATABASE_URL=postgres://user:password@localhost:5432/yourdatabase

    EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
    EMAIL_HOST=smtp.yourprovider.com
    EMAIL_PORT=587
    EMAIL_USE_TLS=True
    EMAIL_HOST_USER=your-email@domain.com
    EMAIL_HOST_PASSWORD=your-email-password

    CACHE_LOCATION=redis://127.0.0.1:6379/1
    CACHE_CLIENT_CLASS=django_redis.client.DefaultClient

    CELERY_BROKER_URL=redis://localhost:6379/0
    CELERY_RESULT_BACKEND=redis://localhost:6379/0
    ```

5. **Run database migrations:**

    ```sh
    python manage.py migrate
    ```

6. **Create a superuser:**

    ```sh
    python manage.py createsuperuser
    ```

7. **Start the development server:**

    ```sh
    python manage.py runserver
    ```

### Celery Setup

To start Celery worker and beat, open two separate terminal windows and run:

```sh
celery -A config worker --loglevel=info
celery -A config beat --loglevel=info

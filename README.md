# Shop Api

A django project using dajngo-rest-framework for developing apis for a shop project

![Project Logo](./media/github/1.png)


## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)

## Installation

To set up the project locally, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/rms82/drf_shop.git
    cd drf_shop
    ```

2. Create and activate a virtual environment (recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use venv\Scripts\activate
    ```

3. Install the project dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run database migrations:
    ```bash
    python manage.py migrate
    ```

5. Add data to database:
    ```bash
    python manage.py loaddata fixtures/category.json
    python manage.py loaddata fixtures/product.json
    ```

5. Start the development server:
    ```bash
    python manage.py runserver
    ```

6. Visit `http://localhost:8000` in your browser to access the project.

## Usage

Explain how to use your Django Rest Framework project. Provide examples, code snippets, or specific details about its functionality. If your project provides APIs, detail how to make API requests.

## API Documentation

Our project offers a comprehensive API for various functionalities. You can interact with these APIs to perform tasks related to our application.

### Base URL

- All API endpoints are accessible at: `https://api.example.com`

### Authentication

- To access the API, obtain an API key by contacting our support team.
- Include the API key in the headers of your HTTP requests:


### Available Endpoints

1. **GET /api/resource/**
 - Retrieve a list of resources.
 - No additional parameters required.
 - Example: `GET https://api.example.com/api/resource/`

2. **POST /api/resource/**
 - Create a new resource.
 - Request:
   ```http
   POST https://api.example.com/api/resource/
   Content-Type: application/json

   {
       "name": "New Resource",
       "description": "This is a new resource."
   }
   ```

3. **GET /api/resource/{id}/**
 - Retrieve details of a specific resource.
 - Request: `GET https://api.example.com/api/resource/123/`

4. **PUT /api/resource/{id}/**
 - Update a specific resource.
 - Request:
   ```http
   PUT https://api.example.com/api/resource/123/
   Content-Type: application/json

   {
       "name": "Updated Resource",
       "description": "This is an updated resource."
   }
   ```

5. **DELETE /api/resource/{id}/**
 - Delete a specific resource.
 - Request: `DELETE https://api.example.com/api/resource/123/`

For detailed information, including request and response formats, and additional endpoints, please refer to our [complete API documentation](https://api.example.com/docs/).

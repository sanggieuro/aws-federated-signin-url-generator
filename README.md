# AWS Federated Sign-In URL Generator

This project provides a simple Flask web application that generates an AWS Management Console sign-in URL using AWS STS (Security Token Service) federation tokens. Users can obtain a sign-in URL by providing their AWS access key ID and secret access key.

## Prerequisites

- Python 3.6 or higher
- AWS credentials with appropriate permissions
- Flask
- Boto3

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/aws-federated-signin-url-generator.git
    cd aws-federated-signin-url-generator
    ```

2. Create and activate a virtual environment:

    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

## Configuration

Ensure you have your AWS access key ID and secret access key ready. These credentials should have permissions to generate federation tokens.

## Running the Application

1. Start the Flask application:

    ```sh
    python app.py
    ```

2. The application will be running on `http://0.0.0.0:1337`.

## Usage

To get a federated sign-in URL, send a GET request to the root endpoint with your AWS credentials as query parameters:

```sh
curl "http://0.0.0.0:1337/?key_id=YOUR_AWS_ACCESS_KEY_ID&secret_key=YOUR_AWS_SECRET_ACCESS_KEY"
```

# Credits

Sanggiero @ breachforums.st

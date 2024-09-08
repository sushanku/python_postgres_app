# Flask File Upload & Download Application
This is a simple Python Flask application that allows users to upload and download files (e.g., images, PDFs, XML, CSVs) to and from a Postgres database. The application stores the files in the database and later allows users to download them through a web interface.

## Features
Upload files (images, PDFs, etc.) through a web form.
Download previously uploaded files via a web interface.
Store files in a Postgres database using the BYTEA data type.
Dockerized for easy setup and deployment.
Future Plan
In a future iteration, files will be moved to an S3 bucket for scalable and efficient file storage, with only metadata stored in the Postgres database.


## Prerequisites
Docker
Docker Compose

## Directory Structure
```
.
├── Dockerfile
├── app
│   └── templates
│       ├── download.html
│       └── upload.html
├── app.py
├── docker-compose.yml
└── requirements.txt
```

## How to Run the Application
Clone this Repository and change the directory
Build and Run the Application with Docker Compose: Make sure Docker and Docker Compose are installed on your system. To build and run the app, execute:


`docker compose up --build`

This command will:

Build the Docker images for the Flask app and Postgres database.
Start the containers and run the application on http://localhost:5000.

## Access the Application:

Upload a file by visiting http://localhost:5000.
Download a previously uploaded file by visiting http://localhost:5000/download.

## Shut Down the Application: To stop the application and remove the containers, run:
`docker-compose down`

## Deploying the Application
To deploy this application, you can follow these steps:

### Deploy with Docker Compose:

You can use Docker Compose to deploy this application in any environment that supports Docker, such as a cloud server (e.g., EC2, DigitalOcean, etc.).
Install Docker and Docker Compose on your server.
Transfer the files to the server and run:

`docker-compose up -d --build`


Set Up Reverse Proxy (Optional):

To expose the application to the internet, you can set up a reverse proxy (like Nginx or APACHE2) to route traffic to the Flask app.
Ensure that port 80 or 443 (for HTTPS) is correctly routed to http://localhost:5000.

### Environment Variables:

Make sure to update the POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB, and POSTGRES_HOST in the docker-compose.yml file for production deployment.


## Future Enhancements
Move file storage to S3: In the next phase, the files will be stored in an AWS S3 bucket, and only metadata will be stored in Postgres.
Add user authentication: Secure the file uploads and downloads by adding user authentication.
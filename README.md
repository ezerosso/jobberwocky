# Jobberwocky: A Job Posting and Searching Service

## Overview

This project implements the Jobberwocky service, a platform for companies to post job opportunities and for job seekers to discover them. It leverages Python, SQLite, Celery, and Docker to provide a robust and scalable solution.

## Key Features

- **Job Posting**: Users can create new job postings via a REST API.
- **Job Searching**: Users can search for job postings based on various criteria.
- **User Subscription**: Users can register with their email and a skill or interest, subscribing to receive email notifications about future job postings that match their preferences.
- **Data Integration**: The service performs data integration through a scheduled task that runs twice a day, searching an external data source (jobberwocky-extra-source) to expand the job pool.
- **Asynchronous Task Processing**: Celery is used to handle asynchronous tasks like sending email notifications.
- **Dockerized Environment**: The application is containerized using Docker for easy deployment and portability.

## Technology Stack

- **Backend**: Python, Flask
- **Database**: SQLite
- **Task Queue**: Celery
- **Containerization**: Docker

## Project Structure

jobberwocky/
    ├── app/
    │   ├── api/
    │   │   ├── routes.py
    │   ├── common/
    |   |   ├── decorators/
    |   │   │   ├── transaction.py
    |   │   │   ├── validations.py
    |   │   │   ├── error_handler.py
    |   │   ├── dtos/
    |   │   │   ├── job_dto.py
    |   │   ├── interfaces/
    |   │   │   ├── base_exception.py
    |   │   │   ├── external_service_exception.py
    |   │   │   ├── external_service_exception.py
    |   │   │   ├── subscriber_exception.py
    |   |   ├── mappers/
    |   │   │   ├── job_mapper.py
    |   |   ├── response/
    |   │   │   ├── api_response.py
    │   │   ├── logger.py
    │   ├── core/
    │   │   ├── celery_worker.py
    │   │   ├── config.py
    │   │   ├── container.py
    │   ├── enums/
    │   │   ├── job_source_type.py
    │   ├── events/
    |   │   ├── interfaces/
    |   │   │   ├── event_publisher.py
    |   │   │   ├── subscriber.py
    │   │   ├── email_notification_service.py
    │   │   ├── event_bus.py
    │   │   ├── job_created_event.py
    │   │   ├── job_notification_subscriber.py
    │   ├── interfaces/
    │   │   ├── external_job_service_interface.py
    │   │   ├── generic_repository_interface.py
    │   │   ├── job_repository_interface.py
    │   │   ├── notification_service_interface.py
    |   |   ├── notification_service_interface
    │   ├── models/
    │   │   ├── job_skill.py
    │   │   ├── job.py
    │   │   ├── skill.py
    │   │   ├── subscriber.py
    │   ├── repositories/
    │   │   ├── in_memory_job_repository.py
    │   │   ├── in_memory_subscriber_repository.py
    │   │   ├── sqlite_job_repository.py
    │   │   ├── sqlite_subscriber_repository.py
    │   ├── services/
    │   │   ├── external_job_service.py
    │   │   ├── github_job_source_service.py
    │   │   ├── job_service.py
    │   │   ├── subscriber_service.py
    │   ├── tasks/
    │   │   ├── external_jobs_task.py
    │   │   ├── notification_task.py
    │   ├── utils/
    │   │   ├── hash_util.py
    │   │   ├── search_matcher.py
    ├── tests/
    |   ├── tet1.py
    │   ├── test2.py
    ├── docker-compose.yml
    ├── Dockerfile
    ├── Jobberwocky.postman_collection.json
    ├── README.md
    ├── requirements.txt
    ├── run.py

## Running the Application

### Clone the Repository:

### bash
    git clone https://github.com/ezerosso/jobberwocky.git

### Build and Run the Docker Containers:
    docker-compose up -d

## Test

### Use the Postman collection allocated in the repository
    Jobberwocky.postman_collection.json

### Additional Notes
The application adheres to SOLID principles and clean architecture guidelines.
Consider implementing authentication and authorization for future enhancements.
For production environments, explore using a more robust database like PostgreSQL.
Explore caching strategies to improve performance.
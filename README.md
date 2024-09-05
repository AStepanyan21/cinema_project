
# Cinema Application

This project is a cinema management application that allows users to view cinema rooms, movies, and available seats. 
Users can book seats for a movie in a specific room, and the application will update seat availability in real-time.

## Features

- Multiple cinema rooms (e.g., Red, Blue, Green) with unique schedules and seat arrangements.
- Movies are shown in different rooms simultaneously with their respective schedules and posters.
- Users can select a room, view available movies, and book seats.
- Booked seats become unavailable for the duration of the movie.

## Technologies Used

- **FastAPI**: Main backend framework for CRUD operations.
- **Flask-Admin**: Provides an admin panel for managing cinema data.
- **PostgreSQL**: Database for storing rooms, movies, and bookings.
- **Docker**: Containerization of the application.
- **Docker Compose**: For managing multi-container Docker applications.
- **Pytest**: For unit testing.

## Prerequisites

- Docker and Docker Compose installed on your machine.
- A `.env` file with the necessary environment variables.

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
DB_NAME=your_database
DB_USER=your_user
DB_PASSWORD=your_password
SECRET_KEY=your_secret_key
APP_PORT=8000

DB_HOST=localhost
DB_PORT=5432
DB_URL=postgresql+asyncpg://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}
```

## Setup and Run

1. Clone the repository:

   ```bash
   git clone <repository_url>
   cd cinema_project
   ```

2. Build and start the application using Docker Compose:

   ```bash
   docker-compose up --build
   ```

3. The application will be available at `http://localhost:<APP_PORT>`. Replace `<APP_PORT>` with the port specified in your `.env` file.

## Running Tests

To run the unit tests with asynchronous support, use the following command:

```bash
docker exec -it <container_name> pytest --asyncio-mode=auto
```

Replace `<container_name>` with the name of the running application container.

## Database Migrations

To run database migrations using Alembic, execute:

```bash
docker exec -it <container_name> alembic upgrade head
```

Replace `<container_name>` with the name of the running application container.
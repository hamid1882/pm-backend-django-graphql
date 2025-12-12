# Project Management API

A Django-based GraphQL API for managing organizations, projects, and tasks. Built with Django and Graphene-Django to provide a modern, efficient interface for project management operations.

## Features

- Manage organizations with unique slugs and contact information
- Create and track projects within organizations
- Assign and manage tasks within projects
- Full CRUD operations via GraphQL API
- Django admin interface for data management
- GraphQL playground for interactive API exploration

## Models

- **Organization**: Companies or organizations in the system
- **Project**: Projects belonging to organizations with status tracking
- **Task**: Individual tasks within projects with assignment capabilities

## Technologies Used

- Django 4.2.4
- Graphene-Django 3.1.5
- SQLite (default database)
- Python 3.x

## Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Create a superuser: `python manage.py createsuperuser`
5. Start the server: `python manage.py runserver`

## Usage

Access the GraphQL playground at `http://127.0.0.1:8000/graphql/` to interact with the API.

Access the admin interface at `http://127.0.0.1:8000/admin/` for database management.

## License

This project is open-source and available under the MIT License.

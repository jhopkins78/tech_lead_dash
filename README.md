# Lead Commander - Flask Backend Integration

This project integrates the Lead Intelligence Dashboard HTML files with a Flask backend, providing a complete lead management system with authentication, database storage, and API endpoints.

## Features

- **User Authentication**: Login and registration system with secure password hashing
- **Lead Management**: Create, read, update, and delete leads
- **Task Management**: Assign and track tasks related to leads
- **Workflow Automation**: Create and execute automated workflows
- **Analytics**: Generate reports and insights from lead data
- **File Upload**: Import leads from CSV or Excel files

## Tech Stack

- **Backend**: Flask with SQLite database
- **ORM**: SQLAlchemy for database operations
- **Authentication**: Flask-Login for user session management
- **Frontend**: HTML, CSS, JavaScript (existing dashboard)
- **Data Processing**: Pandas for handling file imports

## Project Structure

```
lead_commander/
├── app.py                 # Main Flask application
├── init_db.py             # Database initialization script
├── requirements.txt       # Python dependencies
├── static/                # Static files
│   ├── js/
│   │   └── api.js         # JavaScript API client
│   └── css/
├── templates/             # HTML templates
│   ├── login.html         # Login page
│   └── register.html      # Registration page
├── uploads/               # Temporary upload directory
└── lead_commander.db      # SQLite database
```

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd lead-commander
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Initialize the database:
   ```
   python init_db.py
   ```
   This will create the database tables and populate them with sample data.

### Running the Application

1. Start the Flask development server:
   ```
   python app.py
   ```

2. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

3. Log in with the default credentials:
   - Admin user:
     - Username: `admin`
     - Password: `admin123`
   - Regular user:
     - Username: `user`
     - Password: `user123`

## API Documentation

The backend provides a RESTful API for interacting with the lead management system. The API endpoints are organized by resource:

### Authentication

- `POST /api/login`: Log in a user
- `POST /api/register`: Register a new user
- `GET /api/logout`: Log out the current user

### Leads

- `GET /api/leads`: Get all leads (with optional filtering)
- `GET /api/leads/<lead_id>`: Get a specific lead
- `POST /api/leads`: Create a new lead
- `PUT /api/leads/<lead_id>`: Update a lead
- `DELETE /api/leads/<lead_id>`: Delete a lead
- `POST /api/leads/upload`: Upload leads from a file

### Tasks

- `GET /api/tasks`: Get all tasks (with optional filtering)
- `POST /api/tasks`: Create a new task
- `PUT /api/tasks/<task_id>`: Update a task
- `DELETE /api/tasks/<task_id>`: Delete a task

### Workflows

- `GET /api/workflows`: Get all workflows
- `GET /api/workflows/<workflow_id>`: Get a specific workflow
- `POST /api/workflows`: Create a new workflow
- `PUT /api/workflows/<workflow_id>`: Update a workflow
- `DELETE /api/workflows/<workflow_id>`: Delete a workflow
- `POST /api/workflows/<workflow_id>/execute`: Execute a workflow

### Analytics

- `GET /api/analytics/lead_sources`: Get lead sources analytics
- `GET /api/analytics/lead_statuses`: Get lead statuses analytics
- `GET /api/analytics/lead_scores`: Get lead scores analytics
- `GET /api/analytics/conversion_rates`: Get conversion rates analytics
- `GET /api/analytics/activity_timeline`: Get activity timeline analytics

## Frontend Integration

The existing HTML dashboard has been integrated with the Flask backend using the JavaScript API client (`static/js/api.js`). This client provides methods for interacting with the backend API, handling authentication, and managing data.

To use the API client in your HTML files, include the following script tag:

```html
<script src="/static/js/api.js"></script>
```

Then, you can use the API client to interact with the backend:

```javascript
// Example: Get all leads
API.leads.getAll()
  .then(leads => {
    console.log('Leads:', leads);
    // Update UI with leads data
  })
  .catch(error => {
    console.error('Error fetching leads:', error);
  });
```

## Security Considerations

- The default admin credentials should be changed in production.
- The secret key in `app.py` should be changed to a secure random value.
- In production, consider using a more robust database like PostgreSQL.
- Implement HTTPS for secure communication.

## License

[MIT License](LICENSE)

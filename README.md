# Household Services Application

A full-stack application for managing household services, built with Flask, Vue.js, and SQLite.

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm 8+

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd household-services
```

2. Set up the backend:
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your settings
```

3. Set up the frontend:
```bash
# Install Node.js dependencies
npm install
```

4. Initialize the database:
```bash
# Create database and run migrations
flask db upgrade
```

### Running the Application

1. Start the backend server:
```bash
# In one terminal
python app.py
```

2. Start the frontend development server:
```bash
# In another terminal
npm run dev
```

The application will be available at:
- Frontend: http://localhost:5173
- Backend API: http://localhost:5000

## Testing the Application

### Default Admin Account
```
Email: admin@example.com
Password: Admin@123
```

### Testing Flow

1. **Register Test Accounts**
   - Register a customer account:
     - Click "Register" and select "Customer"
     - Fill in the required fields
     - Use a valid PIN code (e.g., "123456")

   - Register a professional account:
     - Click "Register" and select "Professional"
     - Fill in the required fields including service type and experience

2. **Admin Testing**
   - Login as admin
   - Navigate to "Professionals" to approve professional registrations
   - Create services under "Services" management
   - Monitor service requests and user activities in the dashboard

3. **Customer Testing**
   - Login as customer
   - Browse available services
   - Create service requests:
     - Select a service
     - Fill in request details (date, time, address)
     - Submit the request
   - View request status and history
   - Submit reviews for completed services

4. **Professional Testing**
   - Login as professional
   - View available service requests
   - Accept/reject requests
   - Mark requests as completed
   - View received reviews and ratings

### API Testing

Use the provided Postman collection (`POSTMAN_TESTING.md`) for API testing:

1. Import the collection into Postman
2. Set up environment variables
3. Follow the testing sequence in the collection

## Project Structure

```
household-services/
├── backend/
│   ├── app.py              # Flask application
│   ├── models.py           # Database models
│   └── routes/             # API routes
├── frontend/
│   ├── src/
│   │   ├── components/     # Vue components
│   │   ├── views/          # Vue views
│   │   ├── stores/         # Pinia stores
│   │   └── router/         # Vue Router
│   └── public/             # Static assets
└── migrations/             # Database migrations
```

## Features

### Admin Dashboard
- User management
- Service management
- Professional approval
- Analytics and reporting

### Customer Features
- Service browsing and search
- Request creation and tracking
- Review submission
- Request history

### Professional Features
- Request management
- Service completion
- Review management
- Performance metrics

## Security Features

- JWT authentication
- Role-based access control
- Rate limiting
- Input validation
- Password hashing

## Development Guidelines

### Backend (Flask)
- Follow PEP 8 style guide
- Use Flask blueprints for route organization
- Implement proper error handling
- Document API endpoints

### Frontend (Vue.js)
- Use Composition API
- Follow Vue.js style guide
- Implement proper form validation
- Use Pinia for state management

## Troubleshooting

### Common Issues

1. Database Issues
   ```bash
   # Reset database
   rm instance/household_services.db
   flask db upgrade
   ```

2. Frontend Build Issues
   ```bash
   # Clear npm cache
   npm cache clean --force
   # Reinstall dependencies
   rm -rf node_modules
   npm install
   ```

3. CORS Issues
   - Ensure backend is running on port 5000
   - Check Vite proxy configuration

### Support

For additional support:
1. Check the issue tracker
2. Review the documentation
3. Contact the development team

## License

This project is licensed under the MIT License - see the LICENSE file for details.
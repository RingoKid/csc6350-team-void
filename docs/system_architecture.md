# SPOT System Architecture

## System Overview
SPOT (Student Project Overview Tool) is a web application that allows users to showcase, discover, and rate developer projects. Below are the system diagrams showing the architecture and component interactions.

## High-Level Architecture
```mermaid
graph TB
    subgraph "Frontend - Vue.js"
        UI[User Interface]
        Router[Vue Router]
        State[Local Storage State]
    end

    subgraph "Backend - Django"
        API[Django REST API]
        Auth[JWT Authentication]
        DB[(PostgreSQL Database)]
    end

    UI --> Router
    Router --> State
    UI --> |HTTP Requests| API
    API --> |JWT Tokens| UI
    API --> Auth
    API --> DB
```

## Component Diagram
```mermaid
graph LR
    subgraph "Frontend Components"
        Home[HomeView]
        Login[Login]
        Signup[SignUp]
        Dashboard[Dashboard]
        ProjectList[ProjectList]
        SinglePage[SinglePageView]
        Search[SearchAndFilter]
        Create[CreateProject]
        Edit[EditProject]
    end

    subgraph "Backend Models"
        User[User Model]
        Project[Project Model]
        Rating[Rating Model]
        Feedback[Feedback Model]
        Collab[Collaboration Model]
        Report[Report Model]
    end

    Home --> ProjectList
    Dashboard --> ProjectList
    Search --> ProjectList
    ProjectList --> SinglePage
    SinglePage --> |Rate/Review| Project
    Create --> Project
    Edit --> Project
    
    User --> |Owns| Project
    User --> |Creates| Rating
    Project --> |Has| Rating
    Project --> |Has| Feedback
    Project --> |Has| Collab
    Project --> |Has| Report
```

## Authentication Flow
```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant A as Auth API
    participant D as Database

    U->>F: Enter Credentials
    F->>A: POST /api/token/
    A->>D: Validate User
    D-->>A: User Valid
    A-->>F: JWT Tokens
    F->>F: Store Tokens
    F-->>U: Redirect to Dashboard
```

## Project Rating Flow
```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant A as API
    participant D as Database

    U->>F: Rate Project (1-5 stars)
    F->>A: POST /api/projects/{id}/rate/
    A->>D: Create/Update Rating
    D-->>A: Rating Saved
    A-->>F: Rating Response
    F-->>U: Update UI
```

## Key Features

### Frontend
- Vue.js SPA with Vue Router
- JWT-based authentication
- Responsive UI with modern design
- Real-time rating updates
- Search and filtering capabilities

### Backend
- Django REST Framework API
- JWT authentication with SimpleJWT
- PostgreSQL database
- Custom user model
- Project management
- Rating system
- Search functionality

### Security Features
- JWT token authentication
- Protected API endpoints
- CORS configuration
- Password hashing
- Permission-based access control

## API Endpoints

### Authentication
- POST `/api/token/` - Get JWT tokens
- POST `/api/token/refresh/` - Refresh JWT token
- POST `/api/auth/signup/` - Register new user

### Projects
- GET `/api/projects/` - List all projects
- POST `/api/projects/` - Create new project
- GET `/api/projects/{id}/` - Get project details
- PUT `/api/projects/{id}/` - Update project
- DELETE `/api/projects/{id}/` - Delete project
- POST `/api/projects/{id}/rate/` - Rate project

### User
- GET `/api/user/projects/` - Get user's projects
- GET `/api/users/` - List users
- GET `/api/projects/search/` - Search projects 
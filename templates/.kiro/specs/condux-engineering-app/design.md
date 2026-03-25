# Design Document

## Overview

The Condux Tesmec Custom Manufacturing Process application is a locally-hosted web application built with modern web technologies. The system provides a comprehensive project management interface for custom engineering work, featuring a professional dark theme UI, automated project numbering, and complete workflow management from concept to completion.

## Architecture

### System Architecture
The application follows a client-server architecture with local hosting:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Browser   │◄──►│  FastAPI Server │◄──►│ SQLite Database │
│   (Frontend)    │    │   (Backend)     │    │   (Data Store)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │  File Storage   │
                       │   (Uploads)     │
                       └─────────────────┘
```

### Technology Stack
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla JS with modern features)
- **Backend**: FastAPI (Python) for REST API
- **Database**: SQLite for local data persistence
- **File Storage**: Local filesystem for uploaded documents
- **Styling**: Custom CSS with dark theme (black/dark blue)
- **Icons**: Font Awesome for UI elements

### Deployment Model
- **Local Hosting**: Single-user desktop application
- **Port**: Default localhost:8000
- **Data Location**: Application directory with portable database
- **File Storage**: Organized directory structure for uploads

## Components and Interfaces

### Frontend Components

#### 1. Main Navigation Component
```javascript
class NavigationComponent {
  - renderTabs()
  - handleTabSwitch()
  - updateActiveTab()
}
```

**Responsibilities:**
- Render main navigation tabs (New Project, Current/Open, Closed, Needs Attention)
- Handle tab switching and state management
- Maintain active tab highlighting

#### 2. Project Form Component
```javascript
class ProjectFormComponent {
  - renderNewProjectForm()
  - handleFormSubmission()
  - validateFormData()
  - manageFileUploads()
}
```

**Responsibilities:**
- Render dynamic project creation form
- Handle all form sections (Concept, Vendors, Engineering, etc.)
- Manage file uploads and validation
- Submit project data to backend

#### 3. Project List Component
```javascript
class ProjectListComponent {
  - renderProjectGrid()
  - filterProjects()
  - sortProjects()
  - handleProjectSelection()
}
```

**Responsibilities:**
- Display projects in grid/list format
- Provide filtering and sorting capabilities
- Handle project selection and navigation

#### 4. Project Detail Component
```javascript
class ProjectDetailComponent {
  - renderProjectDetails()
  - handleStatusUpdates()
  - manageProgressTracking()
  - handleProjectClosure()
}
```

**Responsibilities:**
- Display complete project information
- Handle in-progress updates and status changes
- Manage feasibility validation and visual indicators
- Process project completion workflow

### Backend API Endpoints

#### Project Management
```python
POST   /api/projects              # Create new project
GET    /api/projects              # List all projects
GET    /api/projects/{id}         # Get project details
PUT    /api/projects/{id}         # Update project
DELETE /api/projects/{id}         # Delete project (admin only)
```

#### Project Status Management
```python
PUT    /api/projects/{id}/status  # Update project status
POST   /api/projects/{id}/progress # Add progress update
GET    /api/projects/{id}/progress # Get progress history
```

#### File Management
```python
POST   /api/projects/{id}/files   # Upload project files
GET    /api/projects/{id}/files   # List project files
GET    /api/files/{file_id}       # Download specific file
DELETE /api/files/{file_id}       # Delete file
```

#### System Management
```python
GET    /api/system/next-ct-number # Get next available CT number
GET    /api/system/stats          # Get system statistics
POST   /api/system/backup         # Create data backup
```

## Data Models

### Project Model
```python
class Project:
    id: UUID (Primary Key)
    ct_number: str (Unique, Format: CT0000001)
    status: ProjectStatus (Enum)
    created_date: datetime
    updated_date: datetime
    
    # Concept Phase
    customer_request: str
    customer_number: str
    customer_contact: CustomerContact
    desired_completion_date: date
    
    # Feasibility
    is_feasible: bool
    feasibility_notes: str
    
    # Completion
    completion_summary: str
    completion_date: datetime
```

### Customer Contact Model
```python
class CustomerContact:
    id: UUID (Primary Key)
    project_id: UUID (Foreign Key)
    company_name: str
    contact_name: str
    email: str
    phone: str
    address: str
```

### Vendor Model
```python
class Vendor:
    id: UUID (Primary Key)
    project_id: UUID (Foreign Key)
    vendor_name: str
    contact_info: str
    quote_amount: decimal
    promised_lead_time: int (days)
    quote_date: date
    po_issued: bool
    po_date: date
    po_number: str
```

### Progress Update Model
```python
class ProgressUpdate:
    id: UUID (Primary Key)
    project_id: UUID (Foreign Key)
    update_text: str
    next_steps: str
    created_date: datetime
    created_by: str
```

### File Upload Model
```python
class ProjectFile:
    id: UUID (Primary Key)
    project_id: UUID (Foreign Key)
    file_name: str
    file_path: str
    file_type: FileType (Enum)
    file_category: FileCategory (Enum)
    upload_date: datetime
    file_size: int
```

### Enums
```python
class ProjectStatus(Enum):
    CONCEPT = "concept"
    PROOF_OF_CONCEPT = "proof_of_concept"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CLOSED_INFEASIBLE = "closed_infeasible"

class FileCategory(Enum):
    CUSTOMER_ATTACHMENT = "customer_attachment"
    VENDOR_QUOTE = "vendor_quote"
    VENDOR_PO = "vendor_po"
    CONCEPT_DRAWING = "concept_drawing"
    FABRICATION_DRAWING = "fabrication_drawing"
    VENDOR_DRAWING = "vendor_drawing"
    ASSEMBLY_DRAWING = "assembly_drawing"
    STEP_FILE = "step_file"
    COMPLETION_PHOTO = "completion_photo"
```

## User Interface Design

### Color Scheme
```css
:root {
  --primary-black: #000000;
  --primary-dark-blue: #1a237e;
  --secondary-dark-blue: #283593;
  --accent-blue: #3f51b5;
  --text-light: #ffffff;
  --text-secondary: #e0e0e0;
  --success-green: #4caf50;
  --error-red: #f44336;
  --warning-orange: #ff9800;
  --background-dark: #121212;
  --surface-dark: #1e1e1e;
}
```

### Layout Structure
```
┌─────────────────────────────────────────────────────┐
│                 Header (Logo + Title)               │
├─────────────────────────────────────────────────────┤
│  [New Project] [Current/Open] [Closed] [Attention] │
├─────────────────────────────────────────────────────┤
│                                                     │
│                 Main Content Area                   │
│                                                     │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐   │
│  │   Project   │ │   Project   │ │   Project   │   │
│  │    Card     │ │    Card     │ │    Card     │   │
│  └─────────────┘ └─────────────┘ └─────────────┘   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Project Form Layout
```
┌─────────────────────────────────────────────────────┐
│  Project: CT0000001                    [Save] [Cancel] │
├─────────────────────────────────────────────────────┤
│  ┌─ Concept ─────────────────────────────────────┐  │
│  │ Customer Request: [Text Area]                 │  │
│  │ Customer Info: [Form Fields]                  │  │
│  │ Attachments: [File Upload Area]               │  │
│  └───────────────────────────────────────────────┘  │
│  ┌─ Vendors ─────────────────────────────────────┐  │
│  │ [+ Add Vendor] [Vendor List/Grid]             │  │
│  └───────────────────────────────────────────────┘  │
│  ┌─ Engineering ─────────────────────────────────┐  │
│  │ [File Upload Categories with Drag & Drop]     │  │
│  └───────────────────────────────────────────────┘  │
│  ┌─ Proof of Concept ───────────────────────────┐  │
│  │ [✓] Feasible    [Close Project]              │  │
│  └───────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

## Error Handling

### Frontend Error Handling
- **Form Validation**: Real-time validation with user-friendly error messages
- **File Upload Errors**: Clear feedback for file size, type, and upload failures
- **Network Errors**: Graceful handling of API connection issues
- **Data Persistence**: Local storage backup for form data during network issues

### Backend Error Handling
- **Input Validation**: Comprehensive validation with detailed error responses
- **File System Errors**: Proper handling of disk space and permission issues
- **Database Errors**: Transaction rollback and data integrity protection
- **CT Number Conflicts**: Atomic operations to prevent duplicate numbering

### Error Response Format
```json
{
  "error": true,
  "message": "User-friendly error message",
  "details": "Technical details for debugging",
  "error_code": "VALIDATION_ERROR",
  "timestamp": "2025-01-21T10:30:00Z"
}
```

## Testing Strategy

### Unit Testing
- **Backend API**: Test all endpoints with various input scenarios
- **Data Models**: Validate model constraints and relationships
- **Business Logic**: Test CT number generation and project workflow
- **File Operations**: Test upload, storage, and retrieval operations

### Integration Testing
- **Database Operations**: Test complete CRUD operations
- **File System Integration**: Test file upload and storage workflows
- **API Integration**: Test frontend-backend communication
- **Workflow Testing**: Test complete project lifecycle scenarios

### User Acceptance Testing
- **Workflow Validation**: Test complete project creation to closure workflow
- **UI/UX Testing**: Validate user interface responsiveness and usability
- **File Management**: Test various file types and upload scenarios
- **Data Integrity**: Verify data persistence and backup/restore operations

### Performance Testing
- **File Upload Performance**: Test large file uploads and multiple concurrent uploads
- **Database Performance**: Test with realistic project volumes
- **UI Responsiveness**: Ensure smooth user experience with large datasets
- **Memory Usage**: Monitor application resource consumption

## Security Considerations

### Data Security
- **Local Data Protection**: Secure file permissions for database and uploads
- **Input Sanitization**: Prevent injection attacks and malicious file uploads
- **File Type Validation**: Restrict uploads to approved file types
- **Data Backup**: Secure backup procedures with encryption options

### Access Control
- **Single User Model**: Designed for single-user desktop deployment
- **File Access Control**: Proper file system permissions
- **Database Security**: SQLite file protection and backup encryption
- **Session Management**: Secure session handling for web interface

### File Upload Security
- **File Type Restrictions**: Whitelist approved file extensions
- **File Size Limits**: Prevent disk space exhaustion
- **Virus Scanning**: Integration points for antivirus scanning
- **Path Traversal Protection**: Secure file storage location management
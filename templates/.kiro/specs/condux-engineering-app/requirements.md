# Requirements Document

## Introduction

The Condux Tesmec Custom Manufacturing Process application is a locally-hosted project management system designed to track and manage custom engineering projects from initial concept through completion. The system provides a comprehensive workflow for managing customer requests, vendor relationships, engineering documentation, prototyping, and project execution.

## Glossary

- **System**: The Condux Tesmec Custom Manufacturing Process application
- **Project**: A custom engineering work order with unique CT number
- **User**: Condux Tesmec employee using the application
- **Customer**: External client requesting custom engineering work
- **Vendor**: External supplier providing materials or services
- **CT Number**: Unique project identifier in format CT0000001, CT0000002, etc.
- **Feasibility**: Determination of whether a project concept is technically viable
- **Proof of Concept**: Engineering validation phase before full development

## Requirements

### Requirement 1: Application Interface and Navigation

**User Story:** As a Condux Tesmec employee, I want a professional application interface with clear navigation, so that I can efficiently manage engineering projects.

#### Acceptance Criteria

1. THE System SHALL display the Condux Tesmec logo prominently at the top of the interface
2. THE System SHALL use a black and dark blue color scheme for the user interface
3. THE System SHALL provide navigation tabs for "New Project", "Current/Open Projects", "Closed Projects", and "Needs Attention"
4. WHEN a User selects a navigation tab, THE System SHALL display the corresponding project view
5. THE System SHALL maintain consistent styling and branding throughout all pages

### Requirement 2: Project Number Management

**User Story:** As a project manager, I want automatic project numbering, so that each project has a unique identifier that cannot be reused.

#### Acceptance Criteria

1. WHEN a new project is created, THE System SHALL automatically assign the next available CT number in sequence
2. THE System SHALL format project numbers as CT followed by 7 digits (CT0000001, CT0000002, etc.)
3. THE System SHALL ensure no CT number can be reused once assigned
4. THE System SHALL persist the current project counter across application restarts
5. THE System SHALL display the assigned CT number prominently in the project form

### Requirement 3: New Project Creation - Concept Phase

**User Story:** As a project manager, I want to capture customer requirements and information, so that I can properly scope and plan custom engineering work.

#### Acceptance Criteria

1. THE System SHALL provide a "Customer Request" section with a fillable description text box
2. THE System SHALL include fields for customer number, main contact information, and desired completion date
3. THE System SHALL allow Users to upload attachments including customer-supplied pictures and documents
4. THE System SHALL validate required customer information before allowing project creation
5. THE System SHALL save customer information with the project record

### Requirement 4: Vendor Management

**User Story:** As a procurement specialist, I want to track vendor quotes and purchase orders, so that I can manage supplier relationships and delivery timelines.

#### Acceptance Criteria

1. THE System SHALL provide a vendors section for each project
2. THE System SHALL allow Users to add multiple vendors with quotes and promised lead-times
3. THE System SHALL support PDF upload for vendor quotes and documentation
4. THE System SHALL track issued Purchase Orders with dates and estimated lead-times
5. THE System SHALL display vendor information in an organized, searchable format

### Requirement 5: Engineering Documentation Management

**User Story:** As an engineer, I want to upload and organize project drawings and files, so that all technical documentation is centrally managed.

#### Acceptance Criteria

1. THE System SHALL provide an Engineering section for document uploads
2. THE System SHALL support upload of concept drawings, fabrication drawings, and vendor part drawings
3. THE System SHALL accept STEP files and final assembly drawings/instructions
4. THE System SHALL organize uploaded files by category and display them clearly
5. THE System SHALL maintain file version control and upload timestamps

### Requirement 6: Proof of Concept Validation

**User Story:** As an engineering manager, I want to validate project feasibility, so that we only proceed with viable projects and properly close infeasible ones.

#### Acceptance Criteria

1. THE System SHALL provide a "Proof of Concept" section with a "Feasible" checkbox
2. WHEN the Feasible checkbox is selected, THE System SHALL illuminate the Proof of Concept section with a green border
3. WHEN feasibility is confirmed, THE System SHALL enable the "In Progress" stage
4. IF feasibility is not confirmed, THE System SHALL provide a "Close Project" option
5. WHEN a project is closed due to infeasibility, THE System SHALL illuminate the section with a red border and move the project to "Closed Projects"

### Requirement 7: In-Progress Project Management

**User Story:** As a project manager, I want to track project progress and manage ongoing activities, so that I can ensure timely completion and proper documentation.

#### Acceptance Criteria

1. THE System SHALL provide an "In-Progress" section for active project management
2. THE System SHALL allow upload of issued Purchase Orders with PDF and issue date
3. THE System SHALL provide a progress updates form with date stamps
4. THE System SHALL display the 3 most recent updates at the top with older updates hidden
5. WHEN a User selects "older updates", THE System SHALL display all historical progress entries
6. THE System SHALL include a "Next Steps" field for task delegation and action items

### Requirement 8: Project Completion and Closure

**User Story:** As a project manager, I want to properly close completed projects with documentation, so that we maintain a complete project history and lessons learned.

#### Acceptance Criteria

1. THE System SHALL provide a "Complete Project" section at the end of active projects
2. THE System SHALL allow Users to write a project summary
3. THE System SHALL support upload of completion pictures and final documentation
4. WHEN a project is marked complete, THE System SHALL move it to the "Closed Projects" tab
5. THE System SHALL maintain all project history and documentation after closure

### Requirement 9: Project Status Views and Organization

**User Story:** As a manager, I want to view projects by status, so that I can prioritize work and identify projects needing attention.

#### Acceptance Criteria

1. THE System SHALL display current/open projects in a dedicated view
2. THE System SHALL show closed projects in a separate historical view
3. THE System SHALL identify projects "Needs Attention" based on overdue dates or stalled progress
4. THE System SHALL provide filtering and sorting capabilities within each project view
5. THE System SHALL display key project information in summary format for quick review

### Requirement 10: Data Persistence and File Management

**User Story:** As a system administrator, I want reliable data storage and file management, so that project information is never lost and easily accessible.

#### Acceptance Criteria

1. THE System SHALL store all project data in a local database
2. THE System SHALL maintain uploaded files in an organized directory structure
3. THE System SHALL provide backup and restore capabilities for project data
4. THE System SHALL ensure data integrity across application sessions
5. THE System SHALL handle file uploads securely with appropriate validation
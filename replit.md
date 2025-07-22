# Python Mathematical Console

## Overview

This is a Streamlit-based interactive Python console designed for mathematical computing and code execution. The application provides a web interface for executing Python code, managing execution sessions, and handling mathematical computations with output visualization capabilities.

## User Preferences

Preferred communication style: Simple, everyday language.
GitHub username: infraredracoon1 (primary account for this project)
Framework preference: Keep enhanced libraries and advanced terminal capabilities - "dope as hell"

## System Architecture

The application follows a modular architecture with clear separation of concerns:

- **Frontend**: Streamlit web interface providing an interactive console experience
- **Backend**: Python execution engine with output capture and variable management
- **Session Management**: Persistent session handling with save/load capabilities
- **Code Execution**: Isolated Python code execution with matplotlib integration

## Key Components

### 1. Main Application (`app.py`)
- **Purpose**: Primary Streamlit application entry point
- **Responsibilities**: UI management, session state initialization, user interaction handling
- **Architecture Decision**: Uses Streamlit's session state for maintaining application state across interactions
- **Rationale**: Streamlit provides a simple way to create interactive web applications without complex frontend frameworks

### 2. Code Executor (`code_executor.py`)
- **Purpose**: Handles Python code execution with output capture
- **Key Features**: 
  - Isolated namespace execution
  - Output and error capture
  - Matplotlib plot handling with non-GUI backend
  - Variable management
- **Architecture Decision**: Uses exec() with custom namespace for code execution
- **Rationale**: Provides controlled Python execution while maintaining variable persistence between executions

### 3. Session Manager (`session_manager.py`)
- **Purpose**: Manages session persistence and data serialization
- **Key Features**:
  - Session save/load functionality
  - Export capabilities
  - Variable and output history serialization
- **Architecture Decision**: Uses Streamlit session state for persistence with JSON serialization
- **Rationale**: Leverages Streamlit's built-in session management while providing additional export functionality

## Data Flow

1. **User Input**: Code entered through Streamlit interface
2. **Execution**: Code processed by CodeExecutor with namespace isolation
3. **Output Capture**: Results, errors, and plots captured and formatted
4. **State Management**: Execution history and variables stored in session state
5. **Display**: Results rendered in Streamlit interface
6. **Persistence**: Sessions can be saved/loaded through SessionManager

## External Dependencies

### Core Dependencies
- **Streamlit**: Web application framework for the user interface
- **Matplotlib**: Mathematical plotting and visualization
- **NumPy**: Numerical computing (imported in code executor namespace)

### Architecture Decisions
- **Matplotlib Backend**: Uses 'Agg' (non-GUI) backend for server-side plot generation
- **Rationale**: Enables plot generation in web environment without GUI dependencies

## Deployment Strategy

The application is designed for Streamlit deployment with the following characteristics:

- **Stateless Architecture**: Core application logic doesn't rely on persistent storage
- **Session Management**: Uses Streamlit's session state for user session persistence
- **Resource Management**: Matplotlib configured for server-side rendering
- **Scalability**: Each user session maintains isolated Python namespace

### Deployment Considerations
- No external database required for basic functionality
- Session data persists only during user session (browser-based)
- Suitable for single-user or small-scale multi-user deployment
- Can be easily deployed on Streamlit Cloud, Heroku, or similar platforms

## Notable Design Patterns

1. **Namespace Isolation**: Each user gets isolated Python execution environment
2. **State Management**: Comprehensive session state handling for interactive experience
3. **Modular Design**: Clear separation between UI, execution, and session management
4. **Error Handling**: Graceful error capture and display for code execution failures

## Recent Changes: Latest modifications with dates

### July 22, 2025 - Transformation to Abney Unification Framework
- **Framework Rebranding**: Transformed from Python Mathematical Console to Abney Unification Framework
- **Enhanced Scientific Stack**: Added pandas, seaborn, scikit-learn, sympy, networkx for comprehensive research capabilities
- **Advanced Examples**: Created unified mathematical demonstration covering symbolic math, data analysis, and network science
- **GitHub Repository**: Configured for infraredracoon1/Abney_Unification_Framework with complete documentation
- **Extended Capabilities**: Supports fluid dynamics, symbolic computation, machine learning, and graph theory
- **Research-Grade Platform**: Designed for advanced mathematical research and computational analysis
- **Repository Migration**: Updated to use infraredracoon1 GitHub account with enhanced framework capabilities
- **Streamlit Configuration**: Restored proper configuration for optimal performance
- **User Confirmation**: User confirmed satisfaction with enhanced libraries and terminal - framework ready for production
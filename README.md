# Smart Task Analyzer

An intelligent task prioritization system that scores and sorts tasks based on multiple factors including urgency, importance, effort, and dependencies.

## Setup Instructions

### Prerequisites
- Python 3.8+
- Django 4.0+
- Modern web browser

### Installation

1. Clone the repository:
git clone <your-repo-url>
cd task-analyzer

text

2. Set up backend:
cd backend
python -m venv venv

On Windows:
venv\Scripts\activate

On Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

text

3. Open frontend:
   - Option A: Open `frontend/index.html` directly in browser
   - Option B: Right-click `frontend/index.html` in VS Code → "Open with Live Server"

4. Access application:
   - If using Live Server: `http://localhost:5500`
   - If using Django: `http://127.0.0.1:8000`

## Algorithm Explanation

### Priority Scoring System

The Smart Task Analyzer uses a weighted scoring algorithm that considers four key factors, with a maximum total score of 100 points:

**1. Urgency (40 points max):**
Tasks are scored based on proximity to their due date. Overdue tasks receive maximum urgency (40 points), tasks due today or tomorrow get 35 points, and tasks due further in the future receive proportionally lower scores. This ensures time-sensitive work is prioritized appropriately. The urgency component uses a tiered scoring system: overdue tasks get highest priority, followed by tasks due within 1 day, 3 days, 7 days, and 14 days, with scores decreasing as deadlines become more distant.

**2. Importance (30 points max):**
User-provided importance ratings on a 1-10 scale are normalized to a 30-point scale. This allows users to explicitly flag high-priority work that may not be urgent but is strategically important. Tasks with importance ratings of 8-10 are classified as "High importance," 6-7 as "Medium importance," and below 6 as "Lower importance."

**3. Effort (15 points max):**
Lower-effort tasks receive higher scores, implementing the "quick wins" principle. Tasks requiring ≤1 hour receive the maximum 15 points, 1-3 hours get 10 points, 3-8 hours get 5 points, and tasks over 8 hours get only 2 points. This encourages tackling quick tasks to build momentum and clear the backlog efficiently.

**4. Dependencies (15 points max):**
Tasks that block other tasks receive additional points (5 points per blocked task, capped at 15 points). This prevents bottlenecks in dependent workflows and ensures foundational work is completed first. The system also detects circular dependencies using depth-first search to prevent infinite loops.

### Strategy System

Four configurable strategies adjust the weight multipliers for different work styles:

- **Smart Balance**: Equal 1.0x weighting of all factors for balanced prioritization
- **Fastest Wins**: 4.0x multiplier on effort, 0.5x on other factors - ideal for building momentum
- **High Impact**: 3.0x multiplier on importance, 1.5x on dependencies - focuses on strategic value
- **Deadline Driven**: 3.0x multiplier on urgency - for time-critical situations

After applying strategy multipliers, the final weighted score determines priority levels: Critical (≥70), High (≥50), Medium (≥30), Low (<30).

### Edge Case Handling

- **Overdue tasks**: Assigned maximum urgency score to ensure immediate attention
- **Missing data**: Default values applied (importance=5, hours=1) to prevent errors
- **Circular dependencies**: Detected using depth-first search with recursion stack tracking
- **Invalid dates**: System defaults to today's date and continues processing
- **Empty task lists**: Frontend validation prevents API calls with zero tasks

## Design Decisions

**1. Separate scoring.py module:**
Isolated the algorithm logic into a dedicated module for better testability, maintainability, and separation of concerns. This allows the scoring system to be tested independently and potentially reused in other contexts.

**2. Strategy pattern implementation:**
Used configurable multipliers rather than separate algorithms for each strategy. This reduces code duplication, makes the system more maintainable, and allows easy addition of new strategies without modifying core logic.

**3. Frontend-first validation:**
Implemented basic validation in the frontend to reduce unnecessary API calls and provide immediate user feedback. This improves user experience and reduces server load.

**4. CORS configuration:**
Enabled cross-origin requests to support flexible deployment options (Django-served frontend, Live Server, or separate hosting). Configured for common development ports while maintaining security awareness.

**5. Stateless API design:**
Tasks are analyzed on-demand without database persistence. This simplifies the assignment scope while demonstrating RESTful API design principles and allows the system to handle any task structure without schema migrations.

**6. Trade-off: Simplicity vs. Persistence:**
Chose not to implement database models for tasks, focusing instead on algorithmic quality and API design. In production, persistence would be essential, but for this assignment, the stateless approach better demonstrates problem-solving and code quality.

## Time Breakdown

- **Algorithm design and implementation**: 90 minutes
  - Scoring logic, strategy system, edge case handling
- **Backend API endpoints and serializers**: 45 minutes
  - REST framework setup, validation, error handling
- **Frontend UI and JavaScript**: 75 minutes
  - Form inputs, JSON import, results display, styling
- **Testing and debugging**: 45 minutes
  - Unit tests, CORS fixes, end-to-end testing
- **Documentation and cleanup**: 25 minutes
  - README, code comments, final review

**Total: ~4.5 hours**

## Testing

Run unit tests:
cd backend
python manage.py test tasks

text

Test coverage includes:
- Urgency scoring for overdue tasks
- Importance calculation validation
- Effort scoring (quick wins)
- Circular dependency detection
- Strategy multiplier verification
- Complete priority calculation integration

## Features Implemented

### Core Requirements
✅ Priority scoring algorithm with 4 weighted factors  
✅ Multiple sorting strategies (Smart Balance, Fastest Wins, High Impact, Deadline Driven)  
✅ POST /api/tasks/analyze/ endpoint  
✅ POST /api/tasks/suggest/ endpoint (top 3 recommendations)  
✅ Form input for individual tasks  
✅ JSON bulk import  
✅ Visual priority indicators with color coding  
✅ Task explanations showing why each score was assigned  
✅ Responsive design using Tailwind CSS  
✅ Error handling and loading states  
✅ Edge case handling (overdue, missing data, circular dependencies)  

### Testing
✅ 6 unit tests covering core algorithm functionality  
✅ Manual end-to-end testing across different scenarios  

## Future Improvements

Given additional time, the following enhancements would add significant value:

1. **Persistent storage**: Implement Django Task model with database for saving user tasks across sessions

2. **User authentication**: Add user accounts so each person can manage their own task lists

3. **Enhanced dependency visualization**: Interactive graph view showing task relationships and highlighting circular dependencies visually

4. **Date intelligence**: Consider weekends and holidays when calculating urgency, skipping non-working days in deadline calculations

5. **Historical analytics**: Track which suggested tasks were completed, measure accuracy of priority predictions, and display productivity trends

6. **Batch operations**: Allow editing or deleting multiple tasks simultaneously

7. **Export functionality**: CSV and JSON export of prioritized task lists for sharing or integration with other tools

8. **Eisenhower Matrix view**: 2D grid visualization plotting tasks by urgency vs. importance

9. **Learning system**: Allow users to provide feedback on suggestions and adjust algorithm weights based on their preferences over time

10. **Mobile app**: Native iOS/Android apps for task management on the go

## Technology Stack

- **Backend**: Python 3.x, Django 5.2.8, Django REST Framework 3.16.1
- **Frontend**: HTML5, JavaScript (ES6), Tailwind CSS (via CDN)
- **Development Tools**: SQLite, django-cors-headers 4.9.0
- **Testing**: Django TestCase framework

## Project Structure

task-analyzer/
├── backend/
│ ├── manage.py
│ ├── requirements.txt
│ ├── task_analyzer/
│ │ ├── settings.py
│ │ ├── urls.py
│ │ ├── wsgi.py
│ │ └── asgi.py
│ └── tasks/
│ ├── views.py
│ ├── scoring.py
│ ├── serializers.py
│ ├── urls.py
│ ├── tests.py
│ └── models.py
├── frontend/
│ └── index.html
└── README.md

text

## Author Notes

This assignment demonstrated my ability to:
- Translate business requirements into working code
- Design flexible, configurable algorithms
- Handle edge cases and ambiguous requirements
- Write clean, maintainable code with proper separation of concerns
- Create functional, user-friendly interfaces
- Document design decisions and trade-offs

The focus was on code quality, problem-solving approach, and demonstrating understanding of software engineering principles rather than feature completeness.

## License

This project was created as a technical assessment for a Software Development Intern position.
How to Create the File
Option 1: In VS Code
In VS Code, right-click on task-analyzer folder

Select "New File"

Name it: README.md

Paste the content above

Save (Ctrl+S)

Option 2: Using Command Line
bash
cd C:\Users\HP\Desktop\task-analyzer
notepad README.md
# Paste the content, then save and close
That's it! This README covers all the required sections from the assignment requirements. 📝


# mindjunkies

## Team Members
- [shafayetsadi](https://github.com/Shafayetsadi/)  (Team Leader)
- [md-tonmoy007](https://github.com/md-tonmoy007)
- [SaimaLearnathon](https://github.com/SaimaLearnathon)

## Mentor
- [Md. Redwanuzzaman](https://github.com/redwanuzzaman)

## Project Description
**Nexora** is a modern **Learning Management System (LMS)** built using **Django** and **Tailwind CSS**. It offers a seamless platform for managing courses, users, courses, assignments, and learning content efficiently. Designed to empower teachers and students, MindJunkies focuses on scalability, user experience, and modern web standards.

## 🛠️ Features
- User Authentication (Registration, Login, Social Auth, Email Verification)
- Role-based Access Control (Teachers, Students, Moderators)
- Course Management (Create, Join, Edit)
- Markdown-based Content Writing for Teachers
- Live Video Conferencing with Chat, Polls, and Screen Sharing
- Assignment Submission and Evaluation
- Payment Integration for Premium Features
- Responsive Design with Tailwind CSS

---

## Getting Started

Follow these steps to set up the project locally:

### Prerequisites
- Python 3.13+
- uv
-
1. Clone the repository:
    ```sh
    git clone https://github.com/Learnathon-By-Geeky-Solutions/mindjunkies
    cd mindjunkies
    ```
2. Install dependencies:
    ```sh
    pip install uv
    uv sync
    ```
3. Start development:
    ```sh
    cp .env.example .env # Modify the environment variables
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver
    python manage.py tailwind watch
    ```
4. Open [http://localhost:8000](http://localhost:8000) in your browser.

## Development Guidelines
1. Create feature branches:
    ```sh
    git checkout -b feature/your-feature-name
    ```
2. Commit Changes:
   - Keep commits small and focused.
   - Use clear and descriptive commit messages.
    ```sh
    git add .
    git commit -m "Add feature: [feature-name]"
    ```
3. Push Your Changes:
    ```sh
    git push origin feature/your-feature-name
    ```
4. Submit a Pull Request:
    - Open a Pull Request against the `develop` branch.
    - Add a clear title and description.
    - Mention the issue number (if any) in the description.
    - Assign the PR to the appropriate reviewer.

## Project Structure

```plaintext
# TODO: Update the project structure
mindjunkies/
├── accounts/       # User authentication and profile management
├── courses/        # Course creation, management, and participation
├── assignments/    # Assignment submission and evaluation
├── video/          # Live video conferencing feature
├── static/         # Static files (CSS, JS, images)
├── templates/      # HTML templates
├── config/         # Django project settings and configurations
└── manage.py       # Django project entry point
```

## Resources
- [Project Documentation](docs/)
- [Development Setup](docs/setup.md)
- [Contributing Guidelines](CONTRIBUTING.md)

## Tools and Technologies
- Django
- Tailwind CSS
- DaisyUI
- SQLite (Development), PostgreSQL (Production)
- AWS (Deployment)
- Git and GitHub

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

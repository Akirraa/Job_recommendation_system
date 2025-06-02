# Smart Job Recommendation System

An AI-powered Django platform that recommends jobs to users based on parsed resumes, semantic matching, and multi-layer NLP techniques. Built with REST and GraphQL APIs, asynchronous processing, and modern NLP libraries like spaCy and Sentence-BERT.

---

## 🚀 Features

* 🔐 JWT-based Authentication with role support (Job Seeker, Recruiter) and Throttle for request limiting
* 📄 Resume upload with automatic parsing (name, email, phone, education, skills, experience, location)
* 🧠 Multi-layer recommendation engine:

  * Layer 1: TF-IDF filtering
  * Layer 2: Sentence-BERT semantic re-ranking
* ⚙️ Asynchronous resume processing and recommendation generation using Celery + Redis
* 🧬 Vector storage for jobs and users
* 🔍 GraphQL support for advanced querying and filtering
* 🧾 REST API for user, resume, job, and recommendation management

---

## 🧱 Tech Stack

* **Backend:** Django, Django REST Framework, Graphene-Django
* **NLP:** spaCy, HuggingFace Transformers, pdfplumber, Sentence-Transformers
* **Database:** PostgreSQL
* **Asynchronous Tasks:** Celery + Redis
* **Authentication:** JWT (djangorestframework-simplejwt)

---

## 📦 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Akirraa/Job_recommendation_system.git
cd jobRecommandation
```

### 2. Create and Activate a Virtual Environment

```bash
pipenv shell  # or python -m venv venv && source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` File

```env
DEBUG=True
SECRET_KEY=your_secret_key

# Database
DB_NAME=your_db
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# Redis
REDIS_URL=redis://localhost:6379
```

### 5. Run Migrations

```bash
python manage.py migrate
```

### 6. Run Redis

Make sure Redis is running:

```bash
redis-server
```

### 7. Start Celery Workers

```bash
celery -A jobRecommandation worker --loglevel=info --pool=solo
```

(Optional) Start Celery Beat for periodic tasks:

```bash
celery -A jobRecommandation beat --loglevel=info
```

### 8. Run the Django Server

```bash
python manage.py runserver
```

---

## 📤 Resume Upload & Parsing

* PDF resumes are parsed using `pdfplumber` for raw text.
* `ResumeData` is generated using spaCy NLP and regex extractors:

  * Name
  * Email
  * Phone Number
  * Location
  * Skills
  * Education
  * Experience

```bash
python manage.py parse_resumes
```

---

## 🧬 Vector Generation

* **User Vectors:** Generated from parsed resume data using Sentence-BERT.

```bash
python manage.py generate_user_vectors
```

* **Job Vectors:** TF-IDF vectors from job title and description.

```bash
python manage.py generate_job_vectors
```

---

## 🔁 Recommendation Pipeline

1. **Layer 1:** Matches user vectors to job vectors (TF-IDF based)
2. **Layer 2:** Re-ranks top jobs using Sentence-BERT similarity
3. **Layer 3:** (Coming soon) Context-aware personalization

```bash
python manage.py generate_recommendations
python manage.py semantic_rerank
```

---

## 🔐 REST API Endpoints

| Endpoint                     | Method | Description                |
| ---------------------------- | ------ | -------------------------- |
| `/api/auth/register/`        | POST   | Register a new user        |
| `/api/auth/login/`           | POST   | Login and obtain JWT       |
| `/api/auth/profile/`         | GET    | Get current user's profile |
| `/api/resumes/upload/`       | POST   | Upload a resume file       |
| `/api/resumes/<id>/data/`    | GET    | Get parsed resume info     |
| `/api/recommendations/`      | GET    | List job recommendations   |
| `/api/recommendations/save/` | POST   | Save a job recommendation  |
| `/api/recommendations/skip/` | POST   | Skip a job recommendation  |

Use your JWT in headers:

```http
Authorization: Bearer <token>
```

---

## 🧪 GraphQL API

Available at: `/api/recommendations/graphql/`

### Sample Query
To get all recommendations  use :
```graphql
query GetAllRecommendations {
  allRecommendations {
    generatedAt
    id
    job {
      description
      id
      title
    }
    user {
      email
      fullName
      id
    }
    score
  }
}
```

### Sample Mutation
To generate JobVectors use :
```graphql
mutation {
  generateJobVectors {
    message
    success
  }
}
```
To generate UserVectors use:
```graphql
mutation {
  generateUserVectors {
    message
    success
  }
}
```
To generate Recommendations use:
```graphql
mutation {
  generateRecommendations {
    message
    success
  }
}
```
To do a semanic rerank use:
```graphql
mutation {
  semanticRerank {
    message
    success
  }
}
``` 
To Parse Resumes use:
```graphql
mutation {
  parseResumes {
    success
    message
  }
}
```

---

## 🗂 Project Structure

```
jobRecommandation/
├── Applications/
├── UserAuth/         # Custom User + Profiles
├── Jobs/             # Job model + Skill taxonomy
├── Resume/           # Resume upload + parsing
├── Recommendations/  # Multi-layer recommendation engine
├── templates/
├── manage.py
```

---

## 🧪 Testing

Links are available in a simple home page. (Exemple: Use `/api/recommendations/graphql/` for testing GraphQL.)
Alternatively,
Use Postman, Insomnia, or curl for REST endpoints.

manage.py commands are also available for:
-parsing resumes.
-Generating UserVectors, JobVectors and recommendations.
-Semantic Rerank.

commands are:

```bash
python manage.py parse_resumes
```
```bash
python manage.py generate_job_vectors 
```
```bash
python manage.py generate_user_vectors
```
```bash
python manage.py generate_recommendations
```
```bash
python manage.py semantic_rerank
```
---

## 🛠 To Do

* Add third layer to recommendation engine (contextual / collaborative filtering)
* Improve NLP parsing for certifications, projects, etc.
* Add resume parsing via HuggingFace pipeline (NER)
* Add job search by skill match
* Add test coverage
* Dockerize the project for production
* Frontend in React or Next.js (optional)

---

## 🧑‍💻 Contributors

Built with ❤️ by [Akirraa](https://github.com/Akirraa)
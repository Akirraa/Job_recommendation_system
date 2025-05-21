
```markdown
# Smart Job Recommendation System

A Django-based platform that offers AI-driven job recommendations using resume parsing, NLP, and multi-layer semantic matching. Supports both REST and GraphQL APIs for flexible integration.

---

## Features

- Resume upload and automated parsing with PDFMiner and Transformer-based NLP models  
- Extraction of candidate info: name, email, phone, location, skills, education, experience, certifications, projects  
- Multi-layer recommendation engine: TF-IDF + Sentence-BERT semantic re-ranking  
- Asynchronous processing with Celery and Redis  
- JWT authentication and role-based access control (job seekers, recruiters)  
- REST API endpoints for auth, resumes, recommendations  
- GraphQL API for advanced queries and mutations  
- Pagination, filtering, and search support  
- Save or skip job recommendations via API

---

## Tech Stack

- Python 3.11, Django, Django REST Framework  
- Graphene-Django for GraphQL  
- Celery + Redis for asynchronous tasks  
- NLP: spaCy, HuggingFace Transformers, pdfminer.six  
- PostgreSQL database  
- JWT Authentication

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Akirraa/smart-job-recommendation.git
cd jobRecommandation
```

### 2. Create and activate virtual environment

```bash
pipenv shell
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root with at least:

```env
# general settings
DEBUG=True
SECRET_KEY= yoursecretkey


# Database
DB_NAME=DBNAME
DB_USER=DBUSER
DB_PASSWORD=DBPASSWORD
DB_HOST=localhost
DB_PORT=5432

REDIS_URL= REDIS_URL
```

### 5. Apply migrations

```bash
python manage.py migrate
```

### 6. Run Redis (needed for Celery)

Make sure Redis server is running locally or use a remote Redis service.

### 7. Start Celery worker

```bash
celery -A jobRecommandation worker --loglevel=info --pool=solo
```

### 8. (Optional) Start Celery beat scheduler for periodic tasks

```bash
celery -A jobRecommandation beat --loglevel=info 
```

### 9. Run Django development server

```bash
python manage.py runserver
```

---

## API Overview

### REST API

| Endpoint                     | Method | Description                    |
|------------------------------|--------|-------------------------------|
| `/api/auth/register/`         | POST   | Register new user              |
| `/api/auth/login/`            | POST   | Obtain JWT token               |
| `/api/auth/profile/`          | GET    | Retrieve authenticated profile|
| `/api/resume/upload/`         | POST   | Upload resume file             |
| `/api/resume/data/<id>/`      | GET    | Get parsed resume data         |
| `/api/recommendations/`       | GET    | List job recommendations       |
| `/api/recommendations/save/`  | POST   | Save a recommendation          |
| `/api/recommendations/skip/`  | POST   | Skip a recommendation          |

- Use JWT token in `Authorization: Bearer <token>` header for protected endpoints.
- CSRF protection is enabled by default on session-based auth; use `@csrf_exempt` or token headers appropriately if needed for APIs.

---

### GraphQL API

- Available at `/graphql/`
- Supports queries and mutations:

#### Sample Queries

```graphql
query {
  recommendations(userId: 1, first: 10, status: "pending") {
    edges {
      node {
        id
        job {
          title
          industry
        }
        score
        status
      }
    }
  }
}
```

```graphql
query {
  userVector(userId: 1) {
    id
    vector
  }
}
```

#### Sample Mutations

```graphql
mutation {
  saveRecommendation(recommendationId: 3) {
    success
    message
  }
}

mutation {
  updateUserVector(userId: 1, vector: "[0.12, 0.34, ...]") {
    userVector {
      id
    }
  }
}
```

---

## Resume Parsing Details

- Uploaded resumes are processed asynchronously by Celery workers.
- Resume text is extracted using `pdfminer.six`.
- NLP extraction of name, email, phone, location, skills, education, experience, certifications, and projects is done using spaCy and Transformer models.
- Parsed data is saved in the `ResumeData` model linked to the uploaded `Resume`.

---

## Testing the APIs

### REST

Use tools like **Postman** or **curl**.

Example login:

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password"}'
```

Include the returned token in `Authorization` header for subsequent requests.

### GraphQL

Access the GraphiQL interface at `http://localhost:8000/api/recommendations/graphql/` to manually test queries and mutations.

---

## Project Structure (Main apps)

```
jobRecommandation/
├── Applications/
├── Jobs/
├── Recommendations/
├── Resume/
├── UserAuth/
├── templates/
└── manage.py
```

---

## What’s Done

- Custom User model with role-based access
- Resume upload and parsing pipeline with Celery
- NLP extraction with Transformers and spaCy
- Job and User vectors for semantic recommendation
- REST and GraphQL endpoints for recommendations and user data
- Pagination, filtering, and mutation support in GraphQL
- JWT authentication for secure access

---

## What’s Next

- Improve NLP extraction (certifications, projects parsing refinements)
- Enhance recommendation algorithms and caching
- Add third layer for the recommendation engine
- Add frontend React/Next.js integration (optional)
- Add more comprehensive test coverage
- Deploy to cloud environment with Docker


---
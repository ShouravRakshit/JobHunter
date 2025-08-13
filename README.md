# **JobHunter: Automated Job Scraper for Workday-Powered Career Portals**

# **Overview**
JobHunter is an end-to-end system designed to automate the collection and analysis of job postings from Workday-powered career portals. The project scrapes verified job listings, cleans and preprocesses the collected text using Natural Language Processing (NLP) techniques, and provides structured insights for job seekers and recruiters. By focusing initially on the local job market (a "Canada-first" approach), JobHunter enhances job discovery and matching, overcoming many of the shortcomings found on traditional platforms like LinkedIn or Indeed.

# **Features**
- Web Scraping:
Utilizes Scrapy, Selenium, and BeautifulSoup to dynamically extract job postings from over 35 Workday-powered websites.

- Data Cleaning & Preprocessing:
Removes HTML tags, special characters, and irrelevant content from raw job texts using BeautifulSoup, NLTK, and spaCy. Standardizes job titles and extracts relevant skills via Named Entity Recognition (NER).

- Experience Extraction:
Implements both LLM-based and rule-based methods to extract and normalize experience requirements, defaulting to "0-5 years" for most roles and "5+ years" for managerial positions.

- Semantic Search:
Leverages SentenceTransformer (BERT-based embeddings) and FAISS to generate embeddings from a combined text field (including job title, description, extracted skills, and experience). Enables rapid semantic search across the dataset.

# **Backend**
- Built using Django REST Framework, the API provides endpoints for:

- Listing jobs with industry and experience filters (e.g., /api/jobs/).

- Retrieving detailed job information (e.g., /api/jobs/<job_id>/).

- Performing semantic search queries (e.g., /api/search/?q=...&top_k=...).

# **Frontend**
- A React-based interface demonstrates interactive filtering and semantic search, allowing users to quickly access and explore relevant job postings.


# **Installation**
## Clone the Repository:

1. Open a terminal and clone the repository using Git:

```
git clone https://github.com/ShouravRakshit/JobHunter.git
```

2. Navigate to the cloned repository:
```
cd JobHunter
```

## Set Up the Backend

1. Create and activate a Python virtual environment:

```
python -m venv .venv
source .venv/Scripts/activate    # On Windows: .venv\Scripts\activate.bat
```

2. Install the dependencies:

```
pip install -r requirements.txt
```

## Data Processing
# Create a data folder and run these files below
```
nlp_models -> extract_keywords -> keyword_extraction_tf_idf -> extract_locations -> llm -> job_classification_llama -> job_description_summarization_llama -> extract_experience_llm 
-> normalize_experience -> update_experience_defaults -> bert_faiss_index -> rule_based_experience
```

Apply Django migrations:

```
python manage.py migrate
```

## Set Up the Frontend

1. Navigate to the frontend folder:
```
cd frontend
```

2. Install npm dependencies:
```
npm install
```

# **Usage**

## Running the Backend API
In the backend folder (JobHunter/backend/jobhunter), start the Django server
```
python manage.py runserver
```

## The API endpoints will be accessible at

List Jobs
```
http://localhost:8000/api/jobs/
```

Job Detail
```
http://localhost:8000/api/jobs/<job_id>/
```
Semantic Search
```
http://localhost:8000/api/search/?q=your_query&top_k=5
```

## Running the Frontend
In the frontend folder (JobHunter/frontend), start the React development server
```
npm start
```

The application should open in your browser at 
```
http://localhost:3000
```
where you can interact with buttons for quick filtering and a search bar for semantic queries.

# **References**
- NeuralNine (YouTube video). Retrieved from: https://www.youtube.com/watch?v=JIz-hiRrZ2g&ab_channel=NeuralNine

- codebasics (YouTube video). Retrieved from: https://www.youtube.com/watch?v=2XUhKpH0p4M&ab_channel=codebasics

- Summer Institute in Computational Social Science (YouTube video). Retrieved from: https://www.youtube.com/watch?v=IUAHUEy1V0Q&t=12s&ab_channel=SummerInstituteinComputationalSocialScience

- Analytics Vidhya (YouTube video). Retrieved from: https://www.youtube.com/watch?v=3oHXpWIvIBs&ab_channel=AnalyticsVidhya

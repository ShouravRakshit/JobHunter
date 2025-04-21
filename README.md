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

Set Up the Backend:

Create and activate a Python virtual environment:

bash
Copy
python -m venv .venv
source .venv/bin/activate    # On Windows: .venv\Scripts\activate
Install the dependencies:

bash
Copy
pip install -r requirements.txt
Apply Django migrations:

bash
Copy
python manage.py migrate
Set Up the Frontend:

Navigate to the frontend folder:

bash
Copy
cd frontend
Install npm dependencies:

bash
Copy
npm install
Usage
Running the Backend API
In the backend folder (JobHunter/backend/jobhunter), start the Django server:

bash
Copy
python manage.py runserver
The API endpoints will be accessible at:

List Jobs: http://localhost:8000/api/jobs/

Job Detail: http://localhost:8000/api/jobs/<job_id>/

Semantic Search: http://localhost:8000/api/search/?q=your_query&top_k=5

Running the Frontend
In the frontend folder (JobHunter/frontend), start the React development server:

bash
Copy
npm start
The application should open in your browser at http://localhost:3000, where you can interact with buttons for quick filtering and a search bar for semantic queries.

Evaluation
Skill Coverage:
A rule-based evaluation showed an average skill coverage of 92.5%. This metric indicates that 92.5% of the skills extracted via NER appear in the original cleaned job descriptions.

Scraping Performance:
The system successfully scrapes an average of 100 job postings per company across 35 websites, yielding over 7,500 postings in total. On average, each company’s scraping process takes about 3 minutes.

Semantic Search Relevance:
Example queries such as “entry-level data analytics job with Python and SQL” return highly relevant results from the FAISS index, demonstrating the efficacy of our semantic search using BERT embeddings.

Future Enhancements
User Feedback Integration:
Collect user interaction data (e.g., click-through rates) for continuous improvement.

Advanced Evaluation:
Integrate formal metrics (Precision, Recall, F1-score) once a labeled dataset is available.

Front-End Improvements:
Enhance UI features, filtering, and detailed job views.

Additional NLP Tasks:
Implement job description summarization and salary estimation, and potentially integrate external data (e.g., Glassdoor).

References
NeuralNine (YouTube video). Retrieved from: https://www.youtube.com/watch?v=JIz-hiRrZ2g&ab_channel=NeuralNine

codebasics (YouTube video). Retrieved from: https://www.youtube.com/watch?v=2XUhKpH0p4M&ab_channel=codebasics

Summer Institute in Computational Social Science (YouTube video). Retrieved from: https://www.youtube.com/watch?v=IUAHUEy1V0Q&t=12s&ab_channel=SummerInstituteinComputationalSocialScience

Analytics Vidhya (YouTube video). Retrieved from: https://www.youtube.com/watch?v=3oHXpWIvIBs&ab_channel=AnalyticsVidhya

License
[Include license information if applicable—e.g., MIT License.]

# api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_list_or_404
from .utils import JOB_POSTINGS, embed_query 
import numpy as np
from ml_loader import load_faiss

class JobListView(APIView):
    """
    GET /api/jobs?industry=Software%20Development&experience=0-5%20years
    Returns a filtered list of job postings in ephemeral storage.
    """
    def get(self, request):
        industry = request.GET.get('industry', '').lower()
        experience = request.GET.get('experience', '').lower()

        # Filter data from JOB_POSTINGS
        filtered = []
        for job in JOB_POSTINGS:
            # Convert fields to lowercase for comparison
            job_industry = str(job.get('llm_category', '')).lower()  
            job_experience = str(job.get('experience_normalized', '')).lower()

            # Check if industry matches 
            if industry and industry not in job_industry:
                continue

            # Check if experience matches 
            if experience and experience not in job_experience:
                continue

            filtered.append(job)

        return Response(filtered, status=status.HTTP_200_OK)

class JobSemanticSearchView(APIView):
    """
    GET /api/search?q=Your%20Query&top_k=5
    Uses FAISS to find top_k relevant postings.
    """
    def get(self, request):
        query = request.GET.get('q', '')
        top_k = int(request.GET.get('top_k', 5))

        if not query:
            return Response({"detail": "No query provided."}, status=status.HTTP_400_BAD_REQUEST)

        # Load the index + mapping 
        index, mapping = load_faiss()

        query_vec = embed_query(query)
        distances, indices = index.search(query_vec, top_k)
        results = [mapping[i] for i in indices[0]]

        return Response(results, status=status.HTTP_200_OK)

class JobDetailView(APIView):
    """
    GET /api/jobs/<int:job_id> 
    Return a single job posting by ID or index in ephemeral data.
    """
    def get(self, request, job_id):
        
        if job_id < 0 or job_id >= len(JOB_POSTINGS):
            return Response({"detail": "Job not found."}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(JOB_POSTINGS[job_id], status=status.HTTP_200_OK)

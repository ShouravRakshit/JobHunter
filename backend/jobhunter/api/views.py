# api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_list_or_404

from .utils import JOB_POSTINGS, FAISS_INDEX, MAPPING, embed_query
import faiss
import numpy as np

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
            job_industry = str(job.get('llm_category', '')).lower()  # or whatever column has industry info
            job_experience = str(job.get('experience_normalized', '')).lower()

            # Check if industry matches (if provided)
            if industry and industry not in job_industry:
                continue

            # Check if experience matches (if provided)
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

        if not FAISS_INDEX:
            return Response({"detail": "FAISS index not loaded."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Embed the query
        query_vec = embed_query(query)
        # Perform FAISS search
        distances, indices = FAISS_INDEX.search(query_vec, top_k)

        results = []
        for idx in indices[0]:
            job_data = MAPPING[idx]  # MAPPING might have 'combined_text' or minimal fields
            # If you want to link this MAPPING entry back to JOB_POSTINGS, you need a consistent ID
            results.append(job_data)

        return Response(results, status=status.HTTP_200_OK)

class JobDetailView(APIView):
    """
    GET /api/jobs/<int:job_id> 
    Return a single job posting by ID or index in ephemeral data.
    """
    def get(self, request, job_id):
        # job_id is the index in ephemeral data or some unique ID if you stored it
        # For simplicity, treat it like an index in JOB_POSTINGS
        if job_id < 0 or job_id >= len(JOB_POSTINGS):
            return Response({"detail": "Job not found."}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(JOB_POSTINGS[job_id], status=status.HTTP_200_OK)

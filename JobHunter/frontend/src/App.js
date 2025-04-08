import React, { useState } from "react";

function App() {
  const [jobs, setJobs] = useState([]);
  const [query, setQuery] = useState("");
  const [topK, setTopK] = useState(5);

  // Fetch filtered jobs from /api/jobs/
  const fetchJobs = async (industry, experience) => {
    // Build endpoint: /api/jobs/?industry=Data%20Science&experience=0-5%20years
    let url = "/api/jobs/";
    const params = new URLSearchParams();
    if (industry) params.append("industry", industry);
    if (experience) params.append("experience", experience);

    url += "?" + params.toString();

    try {
      const res = await fetch(url);
      const data = await res.json();
      setJobs(data); // store the results in state
    } catch (err) {
      console.error("Error fetching jobs:", err);
      setJobs([]);
    }
  };

  // Perform semantic search via /api/search/?q=...&top_k=...
  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query) return;

    const url = `/api/search/?q=${encodeURIComponent(query)}&top_k=${topK}`;
    try {
      const res = await fetch(url);
      if (!res.ok) {
        console.error("Search error:", res.statusText);
        setJobs([]);
        return;
      }
      const data = await res.json();
      setJobs(data);
    } catch (err) {
      console.error("Error performing search:", err);
      setJobs([]);
    }
  };

  return (
    <div style={{ maxWidth: "800px", margin: "auto", padding: "1rem" }}>
      <h1>JobPortal Demo</h1>

      {/* Buttons for quick filters */}
      <div style={{ marginBottom: "1rem" }}>
        <button onClick={() => fetchJobs("software development")}>
          Software Dev Jobs
        </button>
        <button onClick={() => fetchJobs("data science")}>
          Data Science
        </button>
        <button onClick={() => fetchJobs(null, "0-5 years")}>
          0-5 Years Exp
        </button>
        <button onClick={() => fetchJobs(null, "5+ years")}>
          5+ Years Exp
        </button>
      </div>

      {/* Semantic search form */}
      <form onSubmit={handleSearch} style={{ marginBottom: "1rem" }}>
        <input
          type="text"
          placeholder="Enter job search query"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          style={{ marginRight: "0.5rem" }}
        />
        <input
          type="number"
          value={topK}
          onChange={(e) => setTopK(e.target.value)}
          style={{ width: "60px", marginRight: "0.5rem" }}
        />
        <button type="submit">Search</button>
      </form>

      {/* Results section */}
      <h2>Results</h2>
      {jobs.length > 0 ? (
        jobs.map((job, idx) => (
          <div key={idx} style={{ border: "1px solid #ccc", marginBottom: "1rem", padding: "0.5rem" }}>
            <h3>{job.title || "No Title"}</h3>
            <p>
              {/* Show a snippet of the description if it exists */}
              {job.cleaned_description
                ? job.cleaned_description.slice(0, 150) + "..."
                : "No description available"}
            </p>
            <p>Experience: {job.experience_normalized || "N/A"}</p>
          </div>
        ))
      ) : (
        <p>No results or no jobs found.</p>
      )}
    </div>
  );
}

export default App;

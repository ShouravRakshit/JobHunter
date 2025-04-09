import React, { useState } from "react";

function App() {
  const [jobs, setJobs] = useState([]);
  const [query, setQuery] = useState("");
  const [topK, setTopK] = useState(5);
  const [isLoading, setIsLoading] = useState(false);
  const [activeFilter, setActiveFilter] = useState(null);

  // Define style objects for our components
  const styles = {
    container: {
      minHeight: "100vh",
      backgroundColor: "#121212",
      color: "#f0f0f0",
      fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
      display: "flex",
      flexDirection: "column"
    },
    header: {
      backgroundColor: "#1e1e1e",
      padding: "1.5rem 0",
      borderBottom: "1px solid #333",
      marginBottom: "2rem"
    },
    headerContent: {
      maxWidth: "800px",
      margin: "0 auto",
      padding: "0 1rem"
    },
    mainTitle: {
      fontSize: "2rem",
      fontWeight: "bold",
      color: "#4fd1c5",
      margin: 0
    },
    subtitle: {
      color: "#a0aec0",
      marginTop: "0.25rem"
    },
    main: {
      maxWidth: "800px",
      margin: "0 auto",
      padding: "0 1rem",
      flex: 1
    },
    searchPanel: {
      backgroundColor: "#1e1e1e",
      borderRadius: "0.5rem",
      padding: "1.5rem",
      marginBottom: "2rem",
      boxShadow: "0 4px 6px rgba(0, 0, 0, 0.1)"
    },
    sectionTitle: {
      fontSize: "1.25rem",
      fontWeight: 600,
      color: "#4fd1c5",
      marginBottom: "1rem"
    },
    filterButtons: {
      display: "flex",
      flexWrap: "wrap",
      gap: "0.5rem",
      marginBottom: "1.5rem"
    },
    filterButton: {
      padding: "0.5rem 1rem",
      borderRadius: "0.375rem",
      border: "none",
      cursor: "pointer",
      transition: "background-color 0.2s",
      backgroundColor: "#2d3748",
      color: "#e2e8f0"
    },
    activeFilterButton: {
      padding: "0.5rem 1rem",
      borderRadius: "0.375rem",
      border: "none",
      cursor: "pointer",
      transition: "background-color 0.2s",
      backgroundColor: "#0d9488",
      color: "white",
      fontWeight: 500
    },
    searchForm: {
      display: "flex",
      flexWrap: "wrap",
      gap: "0.5rem",
      alignItems: "center"
    },
    searchInput: {
      flexGrow: 1,
      padding: "0.5rem 1rem",
      backgroundColor: "#2d3748",
      color: "white",
      border: "none",
      borderRadius: "0.375rem",
      outline: "none"
    },
    labelText: {
      marginRight: "0.5rem", 
      color: "#a0aec0"
    },
    numberInput: {
      width: "60px",
      padding: "0.5rem",
      backgroundColor: "#2d3748",
      color: "white",
      border: "none",
      borderRadius: "0.375rem",
      outline: "none"
    },
    searchButton: {
      padding: "0.5rem 1.5rem",
      backgroundColor: "#0d9488",
      color: "white",
      border: "none",
      borderRadius: "0.375rem",
      fontWeight: 500,
      cursor: "pointer",
      transition: "background-color 0.2s"
    },
    resultsContainer: {
      marginBottom: "2rem"
    },
    resultsHeader: {
      display: "flex",
      justifyContent: "space-between",
      alignItems: "center",
      marginBottom: "1rem"
    },
    loadingText: {
      color: "#a0aec0"
    },
    jobsList: {
      display: "flex",
      flexDirection: "column",
      gap: "1.5rem"
    },
    jobCard: {
      backgroundColor: "#1e1e1e",
      borderRadius: "0.5rem",
      padding: "1.25rem",
      boxShadow: "0 2px 4px rgba(0, 0, 0, 0.1)",
      border: "1px solid #333",
      transition: "border-color 0.2s"
    },
    jobTitle: {
      fontSize: "1.125rem",
      fontWeight: 600,
      color: "#4fd1c5",
      marginBottom: "0.5rem"
    },
    jobCompany: {
      color: "#a0aec0",
      marginBottom: "0.75rem",
      fontWeight: 500
    },
    jobDescription: {
      color: "#d1d5db",
      marginBottom: "1rem"
    },
    skillsContainer: {
      display: "flex",
      flexWrap: "wrap",
      gap: "0.5rem",
      marginBottom: "0.75rem"
    },
    skillTag: {
      padding: "0.25rem 0.75rem",
      backgroundColor: "#2d3748",
      color: "#4fd1c5",
      borderRadius: "0.375rem",
      fontSize: "0.875rem"
    },
    jobDetails: {
      display: "flex",
      justifyContent: "space-between",
      color: "#a0aec0",
      fontSize: "0.875rem"
    },
    boldText: {
      fontWeight: 500
    },
    noResults: {
      backgroundColor: "#1e1e1e",
      borderRadius: "0.5rem",
      padding: "2rem",
      textAlign: "center",
      color: "#a0aec0",
      border: "1px solid #333"
    },
    noResultsTitle: {
      fontSize: "1.125rem", 
      marginBottom: "0.5rem"
    },
    footer: {
      backgroundColor: "#1e1e1e",
      padding: "1.5rem 0",
      borderTop: "1px solid #333",
      marginTop: "auto"
    },
    footerContent: {
      maxWidth: "800px",
      margin: "0 auto",
      padding: "0 1rem",
      textAlign: "center",
      color: "#a0aec0"
    }
  };

  // Fetch filtered jobs from /api/jobs/
  const fetchJobs = async (industry, experience) => {
    setIsLoading(true);
    setActiveFilter({ industry, experience });
    
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
    } finally {
      setIsLoading(false);
    }
  };

  // Perform semantic search via /api/search/?q=...&top_k=...
  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query) return;
    
    setIsLoading(true);
    setActiveFilter(null);
    
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
    } finally {
      setIsLoading(false);
    }
  };

  // Helper function to determine if a filter is active
  const isFilterActive = (industry, experience) => {
    if (!activeFilter) return false;
    
    if (industry && !experience) {
      return activeFilter.industry === industry;
    } else if (!industry && experience) {
      return activeFilter.experience === experience;
    }
    return false;
  };

  return (
    <div style={styles.container}>
      <header style={styles.header}>
        <div style={styles.headerContent}>
          <h1 style={styles.mainTitle}>JobHunter</h1>
          <p style={styles.subtitle}>Find your next career opportunity</p>
        </div>
      </header>

      <main style={styles.main}>
        {/* Search section */}
        <div style={styles.searchPanel}>
          <h2 style={styles.sectionTitle}>Job Search</h2>
          
          {/* Buttons for quick filters */}
          <div style={styles.filterButtons}>
            
            <button 
              onClick={() => fetchJobs("data science")}
              style={isFilterActive("data science", null) ? styles.activeFilterButton : styles.filterButton}
            >
              Data Science
            </button>
            <button 
              onClick={() => fetchJobs(null, "0-5 years")}
              style={isFilterActive(null, "0-5 years") ? styles.activeFilterButton : styles.filterButton}
            >
              0-5 Years Exp
            </button>
            <button 
              onClick={() => fetchJobs(null, "5+ years")}
              style={isFilterActive(null, "5+ years") ? styles.activeFilterButton : styles.filterButton}
            >
              5+ Years Exp
            </button>
          </div>
          
          {/* Semantic search form */}
          <form onSubmit={handleSearch} style={styles.searchForm}>
            <input
              type="text"
              placeholder="Enter job search query"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              style={styles.searchInput}
            />
            <div style={{ display: "flex", alignItems: "center" }}>
              <label style={styles.labelText}>Top K:</label>
              <input
                type="number"
                value={topK}
                onChange={(e) => setTopK(e.target.value)}
                style={styles.numberInput}
                min="1"
                max="50"
              />
            </div>
            <button type="submit" style={styles.searchButton}>Search</button>
          </form>
        </div>

        {/* Results section */}
        <div style={styles.resultsContainer}>
          <div style={styles.resultsHeader}>
            <h2 style={styles.sectionTitle}>
              Results 
              {jobs.length > 0 && ` (${jobs.length} jobs found)`}
            </h2>
            {isLoading && (
              <div style={styles.loadingText}>Loading...</div>
            )}
          </div>

          {jobs.length > 0 ? (
            <div style={styles.jobsList}>
              {jobs.map((job, idx) => (
                <div key={idx} style={styles.jobCard}>
                  <h3 style={styles.jobTitle}>
                    {job.title || "No Title"}
                  </h3>
                  {job.company && (
                    <p style={styles.jobCompany}>
                      <span>{job.company}</span>
                      {job.location && ` • ${job.location}`}
                    </p>
                  )}
                  {job.cleaned_description && (
                    <div>
                      <p style={styles.jobDescription}>
                        {job.cleaned_description.slice(0, 300)}
                        {job.cleaned_description.length > 300 ? "..." : ""}
                      </p>
                    </div>
                  )}
                  <div style={styles.skillsContainer}>
                    {job.extracted_skills && job.extracted_skills.split(',').map((skill, i) => (
                      <span key={i} style={styles.skillTag}>
                        {skill.trim()}
                      </span>
                    ))}
                  </div>
                  <div style={styles.jobDetails}>
                    {job.experience_normalized && (
                      <div>
                        <span style={styles.boldText}>Experience:</span> {job.experience_normalized}
                      </div>
                    )}
                    {job.salary_range && (
                      <div>
                        <span style={styles.boldText}>Salary:</span> {job.salary_range}
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div style={styles.noResults}>
              {isLoading ? (
                <p>Searching for jobs...</p>
              ) : (
                <div>
                  <p style={styles.noResultsTitle}>No jobs found</p>
                  <p>Try adjusting your search criteria or explore one of our category filters</p>
                </div>
              )}
            </div>
          )}
        </div>
      </main>

      <footer style={styles.footer}>
        <div style={styles.footerContent}>
          <p>© 2025 JobHunter Demo - Find your dream job today</p>
        </div>
      </footer>
    </div>
  );
}

export default App;
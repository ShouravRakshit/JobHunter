import csv
import re
import spacy

nlp = spacy.load("en_core_web_sm")

SKILLS_DB = [
     "python", "java", "c++", "c#", "excel", "sap", "project management",
    "aws", "azure", "react", "node.js", "leadership", "machine learning",
    "sql", "linux", "docker", "kubernetes", "git", "data analysis",
    "cloud", "power bi", "tableau", "spark", "hadoop", "nosql", "mongodb",
    "postgresql", "oracle", "mysql", "javascript", "typescript", "html",
    "css", "angular", "vue", "jquery", "bootstrap", "flask", "django",
    "spring", "hibernate", "rest", "soap", "api", "microservices",
    "agile", "scrum", "kanban", "devops", "ci/cd", "jenkins", "ansible",
    "terraform", "puppet", "chef", "nagios", "splunk", "elk", "grafana",
    "prometheus, " "kibana", "logstash", "rabbitmq", "kafka", "redis",
    "memcached", "cassandra", "hbase", "zookeeper", "elasticsearch",
    "nginx", "apache", "tomcat", "jboss", "weblogic", "websphere",
    "junit", "selenium", "appium", "testng", "maven", "gradle",
    "ant", "jenkins", "bamboo", "jira", "confluence", "bitbucket",
    "github", "gitlab", "trello", "slack", "asana", "basecamp",
    "microsoft office", "google workspace", "slack", "zoom", "webex",
    "microsoft teams", "outlook", "gmail", "calendar", "drive",
    "sheets", "docs", "slides", "forms", "meet", "hangouts", "chat",
    "teams", "onedrive", "sharepoint", "powerpoint", "word", "excel",
    "access", "photoshop", "illustrator", "indesign", "premiere",
    "after effects", "lightroom", "xd", "sketch", "figma", "invision",
    "zeplin", "microsoft dynamics", "salesforce", "hubspot", "zendesk",
    "freshdesk", "intercom", "servicenow", "jira service management",
    "sap business one", "oracle netsuite", "microsoft dynamics 365",
    "sap s/4hana", "oracle erp", "sap erp", "oracle fusion",
    "oracle e-business suite", "sap business bydesign", "sap crm",
    "oracle crm", "microsoft dynamics crm", "salesforce crm",
    "hubspot crm", "zendesk crm", "freshdesk crm", "intercom crm",
    "servicenow crm", "jira service management crm", "sap business one crm",
    "oracle netsuite crm", "microsoft dynamics 365 crm", "sap s/4hana crm",
    "oracle erp crm", "sap erp crm", "oracle fusion crm",
    "oracle e-business suite crm", "sap business bydesign crm",
    "business intelligence", "data visualization", "statistical analysis",
    "product management", "stakeholder management", "strategic planning",
    "financial analysis", "budgeting", "forecasting", "risk management",
    "six sigma", "lean", "process improvement", "change management",
    "business analysis", "requirements gathering", "uml", "bpmn",
    "data mining", "data modeling", "etl", "data warehousing",
    "quality assurance", "quality control", "iso 9001", "itil",
    "business development", "negotiation", "contract management",
    "vendor management", "supply chain", "procurement", "logistics",
    "operations management", "portfolio management", "pmp", "prince2",
    "blockchain", "cybersecurity", "network security", "penetration testing",
    "ethical hacking", "cryptography", "encryption", "firewall",
    "rust", "golang", "kotlin", "swift", "objective-c", "perl",
    "php", "ruby", "scala", "r programming", "matlab", "autocad",
    "solidworks", "catia", "ansys", "plc programming", "scada",
    "embedded systems", "iot", "artificial intelligence", "deep learning",
    "natural language processing", "computer vision", "robotics",
    "image processing", "signal processing", "control systems",
    "fpga", "vhdl", "verilog", "pcb design", "microcontroller",
    "arduino", "raspberry pi", "3d printing", "mechatronics",
    "electrical engineering", "mechanical engineering", "civil engineering",
    "structural engineering", "chemical engineering", "biomedical engineering",
    "aerospace engineering", "automotive engineering", "industrial engineering",
    "systems engineering", "environmental engineering", "materials engineering",
    "quality engineering", "process engineering", "manufacturing engineering",
    "production engineering", "maintenance engineering", "reliability engineering",
    "safety engineering", "risk engineering", "compliance engineering",
    "regulatory affairs", "technical writing", "documentation",
    "user manuals", "instruction manuals", "technical manuals",
    "training manuals", "whitepapers", "case studies", "tutorials",
    "api documentation", "user guides", "online help", "knowledge base",
    "release notes", "installation guides", "configuration guides",
    "troubleshooting guides", "reference guides", "glossaries",
    "style guides", "templates", "forms", "checklists", "flowcharts",
    "diagrams", "screenshots", "videos", "animations", "infographics",
    "illustrations", "icons", "logos", "branding", "typography",
]

def standardize_job_title(title):
    # lowercase
    title = title.lower()
    # remove punctuation (keeping letters, digits, whitespace)
    title = re.sub(r"[^\w\s]", "", title)
    synonyms = {
        "sr": "senior",
        "mgr": "manager",
        "assoc": "associate",
        "jr": "junior",
        "dev": "developer",
        "eng": "engineer",
        "swe": "software engineer",
        "prog": "programmer",
        "arch": "architect",
        "admin": "administrator",
        "sys": "system",
        "tech": "technical",
        "dir": "director",
        "exec": "executive",
        "vp": "vice president",
        "cto": "chief technology officer",
        "ceo": "chief executive officer",
        "cfo": "chief financial officer",
        "hr": "human resources",
        "mkt": "marketing",
        "ops": "operations",
        "qa": "quality assurance",
        "pm": "project manager",
        "asst": "assistant",
        "coord": "coordinator",
        "spec": "specialist",
        "prof": "professional",
        "cert": "certified",
        "temp": "temporary",
        "perm": "permanent",
        "cont": "contract",
        "pt": "part-time",
        "ft": "full-time",
        "prog": "programmer",
        "arch": "architect",
        "admin": "administrator",
        "sys": "system",
    }

    tokens = title.split()
    replaced_tokens = []
    for t in tokens:
        replaced_tokens.append(synonyms.get(t, t))

    # rejoin into a single string
    standardized = " ".join(replaced_tokens)
    return standardized.strip()

# extract skills
def extract_skills_spacy(text):
    doc = nlp(text)
    found_skills = set()

    # convert each token to lowercase
    tokens = [token.text.lower() for token in doc]

    # checking if each skill in SKILLS_DB is present
    for skill in SKILLS_DB:
        # Simple approach: if the skill is exactly in the tokens
        skill_tokens = skill.split()
        # For single-word skill, just check if skill in tokens
        if len(skill_tokens) == 1:
            if skill in tokens:
                found_skills.add(skill)
        else:
            
            for i in range(len(tokens) - len(skill_tokens) + 1):
                window = tokens[i : i + len(skill_tokens)]
                if window == skill_tokens:
                    found_skills.add(skill)
                    break  

    return list(found_skills)

# Process jobs for skills and standardized titles
def process_jobs_for_skills(input_csv, output_csv):
    
    with open(input_csv, newline="", encoding="utf-8") as fin, \
         open(output_csv, "w", newline="", encoding="utf-8") as fout:

        reader = csv.DictReader(fin)
        fieldnames = reader.fieldnames + ["standardized_title", "extracted_skills"]
        writer = csv.DictWriter(fout, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            original_title = row.get("title", "") or ""
            cleaned_desc = row.get("cleaned_description", "") or ""

            # standardize the job title
            std_title = standardize_job_title(original_title)

            # extract skills from the cleaned description
            skills = extract_skills_spacy(cleaned_desc)

            # Update row
            row["standardized_title"] = std_title
            row["extracted_skills"] = ", ".join(skills)

            writer.writerow(row)

def main():
    input_csv = "JobHunter/data/cleaned_jobs.csv"      
    output_csv = "JobHunter/data/jobs_with_skills.csv" 
    process_jobs_for_skills(input_csv, output_csv)
    print(f"Done! Skills extracted and titles standardized. Results in {output_csv}.")

if __name__ == "__main__":
    main()


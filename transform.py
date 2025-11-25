import re
import pandas as pd
import os
from typing import Dict, Any, List

# --- Configuration (MUST match the file path used in your extraction module) ---
LOCAL_TEXT_FILE = "temp_resume_text.txt" 

# --- Configuration for Skills ---
SKILL_KEYWORDS = [
    "Python", "Java", "SQL", "HTML", "CSS", "MERN Stack", 
    "React.js", "Node.js", "Express.js", "MongoDB", "Chart.js", 
    "Agile Methodologies", "GitHub", "VS Code", "DevOps", "AWS"
]

def read_raw_text_from_file(local_path: str) -> str:
    if not os.path.exists(local_path):
        raise FileNotFoundError(f"Error: Raw text file not found at {local_path}. Extraction may have failed.")
    
    with open(local_path, 'r', encoding='utf-8') as f:
        raw_text = f.read()
    
    print(f"✅ Successfully read raw text from {local_path}.")
    return raw_text

def parse_resume_text(raw_text: str) -> pd.DataFrame:
    if not raw_text:
        cols = ["Name", "Experience_List", "Summary", "Email", "Skills"]
        return pd.DataFrame(columns=cols)

    parsed_data: Dict[str, Any] = {
        "Name": "N/A",
        "Summary": "N/A",
        "Email": "N/A",
        "Skills": "",
        "Experience_List": [] 
    }

    # --- 1. Basic Contact & Identity Extraction ---
    
    #extract the name , assuming the name is the start line  
    name_match = re.search(r"^(.*?)(?=\n)", raw_text, re.MULTILINE)
    if name_match:
        parsed_data["Name"] = name_match.group(0).strip()
    
    # Extract Email
    email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", raw_text)
    if email_match:
        parsed_data["Email"] = email_match.group(0)

    # Extract Summary/Objective
    summary_match = re.search(r"OBJECTIVE\s+(.*?)\s+TECHNICAL SKILLS", raw_text, re.DOTALL | re.IGNORECASE)
    if summary_match:
        summary_text = summary_match.group(1).replace('\n', ' ').strip()
        parsed_data["Summary"] = summary_text

    # Extract Skills
    skills_block_match = re.search(r"TECHNICAL SKILLS\s+(.*?)(INTERNSHIPS|PROJECTS)", raw_text, re.DOTALL | re.IGNORECASE)
    raw_skills = skills_block_match.group(1) if skills_block_match else ""
    
        
    found_skills = [skill for skill in SKILL_KEYWORDS if re.search(re.escape(skill), raw_skills, re.IGNORECASE)]
    parsed_data["Skills"] = ", ".join(sorted(list(set(found_skills))))

    # --- 2. Experience Aggregation (List of Strings) ---
    
    internship_block_match = re.search(r"INTERNSHIPS\s+(.*?)(PROJECTS|EDUCATION)", raw_text, re.DOTALL | re.IGNORECASE)
    internship_block = internship_block_match.group(1) if internship_block_match else ""

    # EXP_PATTERN: Captures the Organization/Title + the Date Range
    EXP_PATTERN = r"(AICTE EY-GDS Internship-Edunet Foundation|Cognizant Agile Methodology Virtual Internship)\s*(\(.*?\))"
    
    exp_matches = re.findall(EXP_PATTERN, internship_block, re.DOTALL)

    for match in exp_matches:
        organization_title = match[0].strip() 
        duration = match[1].strip()       
        
        # Combine into the required single string format
        entry_string = f"{organization_title} {duration}"
        parsed_data["Experience_List"].append(entry_string)
    if parsed_data["Experience_List"]:
        parsed_data["Experience_List"] = " ; ".join(parsed_data["Experience_List"])
    else:
        parsed_data["Experience_List"] = ""
    
    # --- 3. Final Transformation to Single-Row DataFrame ---
    df = pd.DataFrame([parsed_data]) 
    
    return df



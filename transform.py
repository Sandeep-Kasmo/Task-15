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
        return pd.DataFrame(columns=["Name","Email","Summary","Skills","Experience_List","Education"])
    parsed_data={"Name":"N/A","Summary":"N/A","Email":"N/A","Skills":"","Experience_List":[],"Education":""}
    name_match=re.search(r"^(.*?)(?=\n)",raw_text,re.MULTILINE)
    if name_match:
        parsed_data["Name"]=name_match.group(0).strip()
    email_match=re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",raw_text)
    if email_match:
        parsed_data["Email"]=email_match.group(0)
    summary_match=re.search(r"(OBJECTIVE|SUMMARY|PROFESSIONAL SUMMARY)\s+(.*?)(TECHNICAL SKILLS|SKILLS|EDUCATION|INTERNSHIPS)",raw_text,re.DOTALL|re.IGNORECASE)
    if summary_match:
        parsed_data["Summary"]=re.sub(r"\s+"," ",summary_match.group(2).replace("\n"," ").strip())
    skills_block=re.search(r"(TECHNICAL SKILLS|SKILLS)\s+(.*?)(INTERNSHIPS|PROJECTS|EDUCATION)",raw_text,re.DOTALL|re.IGNORECASE)
    raw_skills=skills_block.group(2) if skills_block else ""
    found=[s for s in SKILL_KEYWORDS if re.search(re.escape(s),raw_skills,re.IGNORECASE)]
    parsed_data["Skills"]=", ".join(sorted(set(found)))
    intern_block=re.search(r"INTERNSHIPS\s+(.*?)(PROJECTS|EDUCATION|SKILLS|$)",raw_text,re.DOTALL|re.IGNORECASE)
    intern_text=intern_block.group(1) if intern_block else ""
    exp_pattern=r"(AICTE EY-GDS Internship-Edunet Foundation|Cognizant Agile Methodology Virtual Internship)\s*(\(.*?\))"
    exp_matches=re.findall(exp_pattern,intern_text,re.DOTALL)
    for m in exp_matches:
        parsed_data["Experience_List"].append(f"{m[0].strip()} {m[1].strip()}")
    parsed_data["Experience_List"]=" ; ".join(parsed_data["Experience_List"]) if parsed_data["Experience_List"] else ""
    edu_block=re.search(r"(EDUCATION|ACADEMICS|QUALIFICATION|EDUCATIONAL BACKGROUND)\s+(.*?)(PROJECTS|SKILLS|INTERNSHIPS|EXPERIENCE|$)",raw_text,re.DOTALL|re.IGNORECASE)
    if edu_block:
        parsed_data["Education"]=re.sub(r"\s+"," ",edu_block.group(2).strip())
    return pd.DataFrame([parsed_data])



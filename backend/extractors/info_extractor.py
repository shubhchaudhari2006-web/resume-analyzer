import re
from datetime import datetime

class InfoExtractor:
    """Extract information from resume text"""
    
    def __init__(self, text):
        self.text = text
        self.lines = text.split('\n')
    
    def extract_all(self):
        """
        Extract all information from resume
        
        Returns:
            Dictionary with all extracted information
        """
        return {
            'contact': self.extract_contact_info(),
            'summary': self.extract_summary(),
            'experience': self.extract_experience(),
            'education': self.extract_education(),
            'skills': self.extract_skills(),
            'certifications': self.extract_certifications(),
            'projects': self.extract_projects()
        }
    
    def extract_contact_info(self):
        """
        Extract contact information (email, phone, location)
        """
        contact = {}
        
        # Email extraction
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        emails = re.findall(email_pattern, self.text)
        if emails:
            contact['email'] = emails[0]
        
        # Phone extraction
        phone_pattern = r'\b(?:\+?1[-.]?)?\(?([0-9]{3})\)?[-.]?([0-9]{3})[-.]?([0-9]{4})\b'
        phones = re.findall(phone_pattern, self.text)
        if phones:
            contact['phone'] = ''.join(phones[0])
        
        # LinkedIn extraction
        linkedin_pattern = r'linkedin\.com/in/([a-zA-Z0-9-]+)'
        linkedins = re.findall(linkedin_pattern, self.text, re.IGNORECASE)
        if linkedins:
            contact['linkedin'] = linkedins[0]
        
        # GitHub extraction
        github_pattern = r'github\.com/([a-zA-Z0-9-]+)'
        githubs = re.findall(github_pattern, self.text, re.IGNORECASE)
        if githubs:
            contact['github'] = githubs[0]
        
        return contact
    
    def extract_summary(self):
        """
        Extract professional summary or objective
        """
        summary_keywords = ['summary', 'objective', 'about', 'profile']
        summary_text = ""
        
        for i, line in enumerate(self.lines):
            if any(keyword in line.lower() for keyword in summary_keywords):
                # Get next 3-4 lines as summary
                for j in range(i+1, min(i+4, len(self.lines))):
                    if self.lines[j].strip():
                        summary_text += self.lines[j] + " "
                break
        
        return summary_text.strip()
    
    def extract_experience(self):
        """
        Extract work experience
        """
        experience = []
        
        exp_keywords = ['experience', 'work history', 'employment']
        exp_start = -1
        
        for i, line in enumerate(self.lines):
            if any(keyword in line.lower() for keyword in exp_keywords):
                exp_start = i
                break
        
        if exp_start == -1:
            return experience
        
        # Extract job titles and companies
        job_pattern = r'([A-Za-z\s]+)\s*(?:at|@)\s*([A-Za-z\s&.,]+)'
        
        for i in range(exp_start, len(self.lines)):
            line = self.lines[i]
            match = re.search(job_pattern, line)
            if match:
                experience.append({
                    'title': match.group(1).strip(),
                    'company': match.group(2).strip()
                })
        
        return experience[:5]  # Return top 5 positions
    
    def extract_education(self):
        """
        Extract education information
        """
        education = []
        
        edu_keywords = ['education', 'degree', 'university', 'college']
        degree_types = ['bachelor', 'master', 'phd', 'diploma', 'certification', 'b.s.', 'm.s.', 'b.a.', 'm.a.']
        
        for line in self.lines:
            lower_line = line.lower()
            if any(keyword in lower_line for keyword in edu_keywords + degree_types):
                if line.strip():
                    education.append(line.strip())
        
        return education[:5]  # Return top 5 education entries
    
    def extract_skills(self):
        """
        Extract skills section
        """
        skills = []
        
        skills_keywords = ['skills', 'technical skills', 'competencies']
        skills_start = -1
        
        for i, line in enumerate(self.lines):
            if any(keyword in line.lower() for keyword in skills_keywords):
                skills_start = i
                break
        
        if skills_start == -1:
            return skills
        
        # Get lines after skills section
        for i in range(skills_start + 1, min(skills_start + 15, len(self.lines))):
            line = self.lines[i].strip()
            if line and not any(keyword in line.lower() for keyword in ['experience', 'education', 'certification', 'project']):
                # Split by comma or semicolon
                skill_items = re.split(r'[,;]', line)
                for skill in skill_items:
                    skill = skill.strip()
                    if skill and len(skill) > 2:
                        skills.append(skill)
        
        return skills[:20]  # Return top 20 skills
    
    def extract_certifications(self):
        """
        Extract certifications and licenses
        """
        certifications = []
        
        cert_keywords = ['certification', 'certified', 'license', 'credential']
        
        for line in self.lines:
            if any(keyword in line.lower() for keyword in cert_keywords):
                if line.strip():
                    certifications.append(line.strip())
        
        return certifications[:10]  # Return top 10 certifications
    
    def extract_projects(self):
        """
        Extract projects
        """
        projects = []
        
        project_keywords = ['project', 'github', 'portfolio', 'built']
        
        for line in self.lines:
            if any(keyword in line.lower() for keyword in project_keywords):
                if line.strip():
                    projects.append(line.strip())
        
        return projects[:10]  # Return top 10 projects

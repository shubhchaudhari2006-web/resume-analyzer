import re

class SkillExtractor:
    """Extract and categorize skills from resume"""
    
    # Skill categories
    TECHNICAL_SKILLS = {
        'Programming Languages': ['python', 'java', 'javascript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust', 'kotlin', 'swift', 'typescript'],
        'Web Technologies': ['html', 'css', 'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask', 'spring', 'asp.net'],
        'Databases': ['sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'oracle', 'firebase', 'dynamodb', 'cassandra'],
        'DevOps & Cloud': ['docker', 'kubernetes', 'aws', 'azure', 'gcp', 'jenkins', 'ci/cd', 'terraform', 'ansible'],
        'Data & AI/ML': ['machine learning', 'deep learning', 'tensorflow', 'pytorch', 'sklearn', 'pandas', 'numpy', 'spark', 'hadoop'],
        'Mobile Development': ['android', 'ios', 'flutter', 'react native', 'xamarin', 'swift']
    }
    
    SOFT_SKILLS = {
        'Leadership': ['leadership', 'team lead', 'manager', 'mentor', 'coaching'],
        'Communication': ['communication', 'presentation', 'public speaking', 'writing', 'negotiation'],
        'Problem Solving': ['problem solving', 'analytical', 'critical thinking', 'troubleshooting'],
        'Project Management': ['project management', 'agile', 'scrum', 'kanban', 'waterfall'],
        'Collaboration': ['collaboration', 'teamwork', 'cross-functional', 'cooperation']
    }
    
    def __init__(self, text):
        self.text = text.lower()
    
    def extract_all_skills(self):
        """
        Extract and categorize all skills
        
        Returns:
            Dictionary with categorized skills
        """
        return {
            'technical': self.extract_technical_skills(),
            'soft': self.extract_soft_skills(),
            'summary': self.get_skill_summary()
        }
    
    def extract_technical_skills(self):
        """
        Extract technical skills and categorize them
        
        Returns:
            Dictionary with technical skill categories
        """
        technical_skills = {}
        
        for category, skills in self.TECHNICAL_SKILLS.items():
            found_skills = []
            for skill in skills:
                if skill in self.text:
                    found_skills.append(skill)
            if found_skills:
                technical_skills[category] = found_skills
        
        return technical_skills
    
    def extract_soft_skills(self):
        """
        Extract soft skills and categorize them
        
        Returns:
            Dictionary with soft skill categories
        """
        soft_skills = {}
        
        for category, skills in self.SOFT_SKILLS.items():
            found_skills = []
            for skill in skills:
                if skill in self.text:
                    found_skills.append(skill)
            if found_skills:
                soft_skills[category] = found_skills
        
        return soft_skills
    
    def get_skill_summary(self):
        """
        Get summary statistics about skills
        
        Returns:
            Summary dictionary
        """
        technical = self.extract_technical_skills()
        soft = self.extract_soft_skills()
        
        total_technical = sum(len(skills) for skills in technical.values())
        total_soft = sum(len(skills) for skills in soft.values())
        
        return {
            'total_technical_skills': total_technical,
            'total_soft_skills': total_soft,
            'technical_categories_count': len(technical),
            'soft_categories_count': len(soft),
            'has_technical_skills': total_technical > 0,
            'has_soft_skills': total_soft > 0
        }

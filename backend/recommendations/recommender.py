class ResumeRecommender:
    """Generate recommendations for resume improvement"""
    
    def __init__(self, extracted_data):
        self.data = extracted_data
        self.recommendations = []
        self.score = 0
    
    def generate_recommendations(self):
        """
        Generate all recommendations for resume improvement
        
        Returns:
            List of recommendations
        """
        self.recommendations = []
        
        # Check contact information
        self._check_contact_info()
        
        # Check sections
        self._check_sections()
        
        # Check skills
        self._check_skills()
        
        # Check experience
        self._check_experience()
        
        # Check education
        self._check_education()
        
        return self.recommendations
    
    def calculate_score(self):
        """
        Calculate resume score (0-100)
        
        Returns:
            Score value
        """
        self.score = 0
        max_score = 100
        
        # Contact info (15 points)
        contact = self.data.get('contact', {})
        if contact.get('email'):
            self.score += 5
        if contact.get('phone'):
            self.score += 5
        if contact.get('linkedin'):
            self.score += 5
        
        # Summary (10 points)
        if self.data.get('summary'):
            self.score += 10
        
        # Experience (25 points)
        experience = self.data.get('experience', [])
        self.score += min(len(experience) * 5, 25)
        
        # Education (15 points)
        education = self.data.get('education', [])
        if education:
            self.score += 15
        
        # Skills (20 points)
        skills = self.data.get('skills', [])
        if skills:
            self.score += min(len(skills), 20)
        
        # Certifications (10 points)
        certifications = self.data.get('certifications', [])
        if certifications:
            self.score += 10
        
        # Projects (5 points)
        projects = self.data.get('projects', [])
        if projects:
            self.score += 5
        
        return min(self.score, max_score)
    
    def _check_contact_info(self):
        """Check contact information completeness"""
        contact = self.data.get('contact', {})
        
        if not contact.get('email'):
            self.recommendations.append({
                'category': 'Contact Information',
                'type': 'error',
                'message': 'Add your email address',
                'impact': 'high',
                'suggestion': 'Include a professional email address where recruiters can reach you.'
            })
        
        if not contact.get('phone'):
            self.recommendations.append({
                'category': 'Contact Information',
                'type': 'warning',
                'message': 'Consider adding a phone number',
                'impact': 'medium',
                'suggestion': 'A phone number allows quick contact from recruiters.'
            })
        
        if not contact.get('linkedin'):
            self.recommendations.append({
                'category': 'Contact Information',
                'type': 'suggestion',
                'message': 'Add LinkedIn profile link',
                'impact': 'low',
                'suggestion': 'Include your LinkedIn URL to provide more professional background.'
            })
    
    def _check_sections(self):
        """Check if all important sections are present"""
        required_sections = [
            ('summary', 'Professional Summary'),
            ('experience', 'Work Experience'),
            ('education', 'Education'),
            ('skills', 'Skills')
        ]
        
        for section_key, section_name in required_sections:
            section_data = self.data.get(section_key)
            if not section_data or len(section_data) == 0:
                self.recommendations.append({
                    'category': 'Resume Structure',
                    'type': 'error' if section_key in ['experience', 'education'] else 'warning',
                    'message': f'Missing {section_name} section',
                    'impact': 'high' if section_key in ['experience', 'education'] else 'medium',
                    'suggestion': f'Add a {section_name} section to provide important information to recruiters.'
                })
    
    def _check_skills(self):
        """Check skills section"""
        skills = self.data.get('skills', [])
        
        if not skills or len(skills) == 0:
            self.recommendations.append({
                'category': 'Skills',
                'type': 'error',
                'message': 'No skills found',
                'impact': 'high',
                'suggestion': 'Add a detailed Skills section with technical and soft skills.'
            })
        elif len(skills) < 5:
            self.recommendations.append({
                'category': 'Skills',
                'type': 'warning',
                'message': 'Add more skills',
                'impact': 'medium',
                'suggestion': 'Include at least 10-15 relevant skills to improve visibility.'
            })
        
        if len(skills) > 0:
            self.recommendations.append({
                'category': 'Skills',
                'type': 'suggestion',
                'message': 'Organize skills by category',
                'impact': 'low',
                'suggestion': 'Group skills into categories (e.g., Programming Languages, Frameworks, Tools) for better readability.'
            })
    
    def _check_experience(self):
        """Check work experience"""
        experience = self.data.get('experience', [])
        
        if not experience or len(experience) == 0:
            self.recommendations.append({
                'category': 'Work Experience',
                'type': 'warning',
                'message': 'Consider adding work experience',
                'impact': 'high',
                'suggestion': 'Include your professional work experience with company names and job titles.'
            })
        elif len(experience) < 2:
            self.recommendations.append({
                'category': 'Work Experience',
                'type': 'suggestion',
                'message': 'Add more work experience',
                'impact': 'medium',
                'suggestion': 'Include at least 2-3 previous positions to show career growth.'
            })
    
    def _check_education(self):
        """Check education section"""
        education = self.data.get('education', [])
        
        if not education or len(education) == 0:
            self.recommendations.append({
                'category': 'Education',
                'type': 'warning',
                'message': 'Add educational background',
                'impact': 'high',
                'suggestion': 'Include your degree(s), institution names, and graduation dates.'
            })
        
        # Check for certifications
        certifications = self.data.get('certifications', [])
        if not certifications or len(certifications) == 0:
            self.recommendations.append({
                'category': 'Education',
                'type': 'suggestion',
                'message': 'Add certifications (if any)',
                'impact': 'low',
                'suggestion': 'Include relevant certifications like AWS, Google, Microsoft, etc. to strengthen your profile.'
            })
    
    def get_summary(self):
        """
        Get a summary of recommendations
        
        Returns:
            Summary dictionary
        """
        recommendations = self.generate_recommendations()
        score = self.calculate_score()
        
        errors = [r for r in recommendations if r['type'] == 'error']
        warnings = [r for r in recommendations if r['type'] == 'warning']
        suggestions = [r for r in recommendations if r['type'] == 'suggestion']
        
        return {
            'score': score,
            'total_recommendations': len(recommendations),
            'critical_issues': len(errors),
            'warnings': len(warnings),
            'suggestions': len(suggestions),
            'recommendations': recommendations,
            'score_message': self._get_score_message(score)
        }
    
    def _get_score_message(self, score):
        """Get message based on score"""
        if score >= 85:
            return 'Excellent resume! Ready to apply for jobs.'
        elif score >= 70:
            return 'Good resume. Consider the recommendations to improve further.'
        elif score >= 50:
            return 'Fair resume. Address critical issues to improve competitiveness.'
        else:
            return 'Your resume needs significant improvements. Start with critical issues.'

import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from config import config
from parsers import PDFParser, DOCXParser, TextParser
from extractors import InfoExtractor, SkillExtractor
from recommendations import ResumeRecommender
from utils import allowed_file, save_uploaded_file, get_file_extension

def create_app(config_name='development'):
    """
    Application factory
    
    Args:
        config_name: Configuration environment
        
    Returns:
        Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Enable CORS
    CORS(app)
    
    # Create upload folder if it doesn't exist
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    # Store analyzed resumes in memory (for demo)
    analyzed_resumes = {}
    
    # Routes
    @app.route('/')
    def index():
        """Home page"""
        return render_template('index.html')
    
    @app.route('/results/<file_id>')
    def results(file_id):
        """Results page"""
        if file_id not in analyzed_resumes:
            return render_template('index.html', error='Resume not found')
        return render_template('results.html', file_id=file_id)
    
    # API Routes
    @app.route('/api/upload', methods=['POST'])
    def upload_resume():
        """
        API endpoint to upload and analyze resume
        
        Returns:
            JSON response with file_id and analysis
        """
        try:
            # Check if file is in request
            if 'file' not in request.files:
                return jsonify({'error': 'No file provided'}), 400
            
            file = request.files['file']
            
            if file.filename == '':
                return jsonify({'error': 'No file selected'}), 400
            
            if not allowed_file(file.filename, app.config['ALLOWED_EXTENSIONS']):
                return jsonify({'error': 'File type not allowed. Use PDF, DOCX, or TXT'}), 400
            
            # Save file
            file_id, file_path = save_uploaded_file(file, app.config['UPLOAD_FOLDER'])
            
            # Parse resume based on file type
            ext = get_file_extension(file.filename)
            
            if ext == 'pdf':
                text = PDFParser.parse(file_path)
            elif ext == 'docx':
                text = DOCXParser.parse(file_path)
            elif ext == 'txt':
                text = TextParser.parse(file_path)
            else:
                return jsonify({'error': 'Unsupported file type'}), 400
            
            # Extract information
            info_extractor = InfoExtractor(text)
            extracted_info = info_extractor.extract_all()
            
            # Extract and categorize skills
            skill_extractor = SkillExtractor(text)
            skills_info = skill_extractor.extract_all_skills()
            extracted_info['skills_analysis'] = skills_info
            
            # Generate recommendations
            recommender = ResumeRecommender(extracted_info)
            recommendations_summary = recommender.get_summary()
            
            # Store results
            analyzed_resumes[file_id] = {
                'filename': file.filename,
                'extracted_info': extracted_info,
                'recommendations': recommendations_summary,
                'raw_text': text
            }
            
            return jsonify({
                'success': True,
                'file_id': file_id,
                'score': recommendations_summary['score'],
                'message': 'Resume analyzed successfully'
            }), 200
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/results/<file_id>')
    def get_results(file_id):
        """
        API endpoint to get analysis results
        
        Args:
            file_id: Resume file ID
            
        Returns:
            JSON with extracted information
        """
        if file_id not in analyzed_resumes:
            return jsonify({'error': 'Resume not found'}), 404
        
        resume_data = analyzed_resumes[file_id]
        return jsonify({
            'filename': resume_data['filename'],
            'extracted_info': resume_data['extracted_info']
        }), 200
    
    @app.route('/api/recommendations/<file_id>')
    def get_recommendations(file_id):
        """
        API endpoint to get recommendations
        
        Args:
            file_id: Resume file ID
            
        Returns:
            JSON with recommendations
        """
        if file_id not in analyzed_resumes:
            return jsonify({'error': 'Resume not found'}), 404
        
        resume_data = analyzed_resumes[file_id]
        return jsonify(resume_data['recommendations']), 200
    
    @app.route('/api/score/<file_id>')
    def get_score(file_id):
        """
        API endpoint to get resume score
        
        Args:
            file_id: Resume file ID
            
        Returns:
            JSON with score details
        """
        if file_id not in analyzed_resumes:
            return jsonify({'error': 'Resume not found'}), 404
        
        resume_data = analyzed_resumes[file_id]
        recommendations = resume_data['recommendations']
        
        return jsonify({
            'score': recommendations['score'],
            'score_message': recommendations['score_message'],
            'total_recommendations': recommendations['total_recommendations'],
            'critical_issues': recommendations['critical_issues'],
            'warnings': recommendations['warnings'],
            'suggestions': recommendations['suggestions']
        }), 200
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors"""
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors"""
        return jsonify({'error': 'Internal server error'}), 500
    
    return app

if __name__ == '__main__':
    app = create_app(os.getenv('FLASK_ENV', 'development'))
    app.run(debug=True, host='0.0.0.0', port=5000)

# Resume Analyzer

A Python-based resume analyzer that extracts information from resumes and provides intelligent recommendations for improvement.

## Features

- **Resume Parsing**: Extract information from PDF, DOCX, and TXT files
- **Information Extraction**: 
  - Personal details (name, email, phone, location)
  - Skills and technical expertise
  - Work experience and achievements
  - Education and certifications
  - Projects and portfolio links
- **Smart Recommendations**: 
  - Suggestions for skill improvements
  - Resume formatting recommendations
  - Missing sections identification
  - ATS (Applicant Tracking System) optimization tips
- **Score/Rating**: Overall resume score based on completeness and quality

## Tech Stack

- **Backend**: Python 3.9+
- **NLP**: spaCy, NLTK
- **Document Parsing**: PyPDF2, python-docx
- **API**: Flask
- **Frontend**: HTML5, CSS3, JavaScript

## Project Structure

```
resume-analyzer/
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── requirements.txt
│   ├── parsers/
│   │   ├── __init__.py
│   │   ├── pdf_parser.py
│   │   ├── docx_parser.py
│   │   └── text_parser.py
│   ├── extractors/
│   │   ├── __init__.py
│   │   ├── info_extractor.py
│   │   └── skill_extractor.py
│   ├── recommendations/
│   │   ├── __init__.py
│   │   └── recommender.py
│   ├── utils/
│   │   ├── __init__.py
│   │   └── helpers.py
│   └── templates/
│       ├── index.html
│       └── results.html
├── frontend/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
└── .gitignore
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/shubhchaudhari2006-web/resume-analyzer.git
cd resume-analyzer
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r backend/requirements.txt
python -m spacy download en_core_web_sm
```

4. Run the application:
```bash
cd backend
python app.py
```

5. Open browser and go to `http://localhost:5000`

## Usage

1. Upload your resume (PDF, DOCX, or TXT)
2. Click "Analyze"
3. View extracted information
4. Get personalized recommendations
5. Check your resume score

## API Endpoints

- `POST /api/upload` - Upload resume file
- `GET /api/results/<file_id>` - Get analysis results
- `GET /api/recommendations/<file_id>` - Get recommendations
- `GET /api/score/<file_id>` - Get resume score

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License

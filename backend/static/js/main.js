// Main JavaScript for Resume Analyzer

document.addEventListener('DOMContentLoaded', function () {
    const uploadForm = document.getElementById('uploadForm');
    const fileInput = document.getElementById('fileInput');
    const fileLabel = document.querySelector('.file-label');
    const fileInfo = document.getElementById('fileInfo');
    const fileName = document.getElementById('fileName');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const errorMessage = document.getElementById('errorMessage');

    if (uploadForm) {
        // File input change
        fileInput.addEventListener('change', function () {
            if (this.files && this.files[0]) {
                fileName.textContent = this.files[0].name;
                fileInfo.classList.remove('hidden');
            }
        });

        // Drag and drop
        fileLabel.addEventListener('dragover', function (e) {
            e.preventDefault();
            this.style.backgroundColor = '#fdf0fb';
        });

        fileLabel.addEventListener('dragleave', function () {
            this.style.backgroundColor = '#f0f4ff';
        });

        fileLabel.addEventListener('drop', function (e) {
            e.preventDefault();
            if (e.dataTransfer.files && e.dataTransfer.files[0]) {
                fileInput.files = e.dataTransfer.files;
                fileName.textContent = e.dataTransfer.files[0].name;
                fileInfo.classList.remove('hidden');
            }
            this.style.backgroundColor = '#f0f4ff';
        });

        // Form submission
        uploadForm.addEventListener('submit', function (e) {
            e.preventDefault();
            errorMessage.classList.add('hidden');
            loadingSpinner.classList.remove('hidden');

            const formData = new FormData(this);

            fetch('/api/upload', {
                method: 'POST',
                body: formData
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Redirect to results page
                        window.location.href = `/results/${data.file_id}`;
                    } else {
                        showError(data.error || 'An error occurred');
                        loadingSpinner.classList.add('hidden');
                    }
                })
                .catch(error => {
                    showError('Error uploading file: ' + error);
                    loadingSpinner.classList.add('hidden');
                });
        });
    }
});

function showError(message) {
    const errorMessage = document.getElementById('errorMessage');
    if (errorMessage) {
        errorMessage.textContent = message;
        errorMessage.classList.remove('hidden');
    }
}

// Load results
function loadResults(fileId) {
    Promise.all([
        fetch(`/api/results/${fileId}`).then(r => r.json()),
        fetch(`/api/recommendations/${fileId}`).then(r => r.json()),
        fetch(`/api/score/${fileId}`).then(r => r.json())
    ])
        .then(([resultsData, recommendationsData, scoreData]) => {
            displayScore(scoreData);
            displayExtractedInfo(resultsData.extracted_info);
            displayRecommendations(recommendationsData.recommendations);
        })
        .catch(error => {
            console.error('Error loading results:', error);
            showError('Error loading analysis results');
        });
}

function displayScore(scoreData) {
    const scoreValue = document.getElementById('scoreValue');
    const scoreMessage = document.getElementById('scoreMessage');
    const scoreBreakdown = document.getElementById('scoreBreakdown');

    if (scoreValue) scoreValue.textContent = scoreData.score;
    if (scoreMessage) scoreMessage.textContent = scoreData.score_message;

    if (scoreBreakdown) {
        scoreBreakdown.innerHTML = `
            <div class="score-item">
                <span>Critical Issues:</span>
                <strong>${scoreData.critical_issues}</strong>
            </div>
            <div class="score-item">
                <span>Warnings:</span>
                <strong>${scoreData.warnings}</strong>
            </div>
            <div class="score-item">
                <span>Suggestions:</span>
                <strong>${scoreData.suggestions}</strong>
            </div>
        `;
    }
}

function displayExtractedInfo(extractedInfo) {
    // Contact Info
    const contactInfo = document.getElementById('contactInfo');
    if (contactInfo) {
        const contact = extractedInfo.contact || {};
        if (Object.keys(contact).length > 0) {
            contactInfo.innerHTML = `
                ${contact.email ? `<p><strong>Email:</strong> ${contact.email}</p>` : ''}
                ${contact.phone ? `<p><strong>Phone:</strong> ${contact.phone}</p>` : ''}
                ${contact.linkedin ? `<p><strong>LinkedIn:</strong> <a href="https://linkedin.com/in/${contact.linkedin}" target="_blank">${contact.linkedin}</a></p>` : ''}
                ${contact.github ? `<p><strong>GitHub:</strong> <a href="https://github.com/${contact.github}" target="_blank">${contact.github}</a></p>` : ''}
            `;
        } else {
            contactInfo.innerHTML = '<p class="empty-state">No contact information found</p>';
        }
    }

    // Summary
    const summaryInfo = document.getElementById('summaryInfo');
    if (summaryInfo) {
        if (extractedInfo.summary) {
            summaryInfo.innerHTML = `<p>${extractedInfo.summary}</p>`;
        } else {
            summaryInfo.innerHTML = '<p class="empty-state">No professional summary found</p>';
        }
    }

    // Experience
    const experienceInfo = document.getElementById('experienceInfo');
    if (experienceInfo) {
        const experience = extractedInfo.experience || [];
        if (experience.length > 0) {
            experienceInfo.innerHTML = '<ul>' + experience.map(exp =>
                `<li><strong>${exp.title}</strong> at ${exp.company}</li>`
            ).join('') + '</ul>';
        } else {
            experienceInfo.innerHTML = '<p class="empty-state">No work experience found</p>';
        }
    }

    // Education
    const educationInfo = document.getElementById('educationInfo');
    if (educationInfo) {
        const education = extractedInfo.education || [];
        if (education.length > 0) {
            educationInfo.innerHTML = '<ul>' + education.map(edu =>
                `<li>${edu}</li>`
            ).join('') + '</ul>';
        } else {
            educationInfo.innerHTML = '<p class="empty-state">No education information found</p>';
        }
    }

    // Skills
    const skillsInfo = document.getElementById('skillsInfo');
    if (skillsInfo) {
        const skills = extractedInfo.skills || [];
        if (skills.length > 0) {
            skillsInfo.innerHTML = '<div class="skills-list">' + skills.map(skill =>
                `<span class="skill-tag">${skill}</span>`
            ).join('') + '</div>';
        } else {
            skillsInfo.innerHTML = '<p class="empty-state">No skills found</p>';
        }
    }

    // Certifications
    const certificationsInfo = document.getElementById('certificationsInfo');
    if (certificationsInfo) {
        const certifications = extractedInfo.certifications || [];
        if (certifications.length > 0) {
            certificationsInfo.innerHTML = '<ul>' + certifications.map(cert =>
                `<li>${cert}</li>`
            ).join('') + '</ul>';
        } else {
            certificationsInfo.innerHTML = '<p class="empty-state">No certifications found</p>';
        }
    }
}

function displayRecommendations(recommendations) {
    const recommendationsList = document.getElementById('recommendationsList');
    if (!recommendationsList) return;

    // Store all recommendations
    window.allRecommendations = recommendations;

    // Display initial recommendations
    renderRecommendations(recommendations, 'all');

    // Add filter functionality
    const filterButtons = document.querySelectorAll('.filter-btn');
    filterButtons.forEach(button => {
        button.addEventListener('click', function () {
            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            const filter = this.dataset.filter;
            renderRecommendations(recommendations, filter);
        });
    });
}

function renderRecommendations(recommendations, filter) {
    const recommendationsList = document.getElementById('recommendationsList');
    if (!recommendationsList) return;

    let filtered = recommendations;
    if (filter !== 'all') {
        filtered = recommendations.filter(r => r.type === filter);
    }

    if (filtered.length === 0) {
        recommendationsList.innerHTML = '<p class="empty-state">No recommendations in this category</p>';
        return;
    }

    recommendationsList.innerHTML = filtered.map(rec => `
        <div class="recommendation-item ${rec.type}">
            <div class="recommendation-header">
                <span class="recommendation-icon">${getRecommendationIcon(rec.type)}</span>
                <span class="recommendation-type">${rec.type}</span>
            </div>
            <div class="recommendation-message">${rec.message}</div>
            <div class="recommendation-suggestion"><strong>Suggestion:</strong> ${rec.suggestion}</div>
            <div style="margin-top: 8px; font-size: 0.85em; color: #999;">${rec.category}</div>
        </div>
    `).join('');
}

function getRecommendationIcon(type) {
    switch (type) {
        case 'error':
            return '❌';
        case 'warning':
            return '⚠️';
        case 'suggestion':
            return '💡';
        default:
            return '📌';
    }
}

// Add CSS for skill tags
const style = document.createElement('style');
style.textContent = `
    .skills-list {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
    }
    
    .skill-tag {
        display: inline-block;
        padding: 6px 12px;
        background-color: #f0f4ff;
        color: #6366f1;
        border-radius: 20px;
        font-size: 0.9em;
        border: 1px solid #6366f1;
    }
`;
document.head.appendChild(style);

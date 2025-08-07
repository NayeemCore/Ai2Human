// DOM Elements
const hamburgerBtn = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');
const inputBtns = document.querySelectorAll('.input-btn');
const inputTextarea = document.getElementById('inputText');
const outputTextarea = document.getElementById('outputText');
const humanizeBtn = document.getElementById('humanizeBtn');
const outputMode = document.getElementById('outputMode');
const wordCount = document.getElementById('wordCount');
const charCount = document.getElementById('charCount');
const humanizationScore = document.getElementById('humanizationScore');
const processingTime = document.getElementById('processingTime');
const copyBtn = document.getElementById('copyBtn');
const downloadBtn = document.getElementById('downloadBtn');
const shareBtn = document.getElementById('shareBtn');
const advancedOptionsBtn = document.getElementById('advancedOptionsBtn');
const modal = document.getElementById('advancedModal');
const closeModal = document.querySelector('.close-modal');

// Mobile menu toggle
hamburgerBtn.addEventListener('click', () => {
    navMenu.classList.toggle('active');
    hamburgerBtn.classList.toggle('active');
});

// Input type switching with automatic paste functionality
inputBtns.forEach((btn, index) => {
    btn.addEventListener('click', () => {
        if (index === 0) { // Paste Text button
            setActiveInputType('text');
            handleAutomaticPaste();
        } else { // Upload File button
            setActiveInputType('file');
        }
    });
});

// Automatic paste functionality
async function handleAutomaticPaste() {
    try {
        if (navigator.clipboard && navigator.clipboard.readText) {
            const clipboardText = await navigator.clipboard.readText();
            if (clipboardText && clipboardText.trim().length > 0) {
                inputTextarea.value = clipboardText;
                updateStats();
                showNotification('Text pasted successfully!', 'success');
            } else {
                showNotification('Clipboard is empty. Please copy some text first.', 'warning');
            }
        } else {
            showNotification('Automatic paste not supported. Please paste manually (Ctrl+V).', 'info');
        }
    } catch (error) {
        console.error('Paste failed:', error);
        showNotification('Could not access clipboard. Please paste manually (Ctrl+V).', 'warning');
    }
}

// Notification system for user feedback
function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existingNotifications = document.querySelectorAll('.notification');
    existingNotifications.forEach(notification => notification.remove());
    
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <span class="notification-icon">${getNotificationIcon(type)}</span>
            <span class="notification-message">${message}</span>
        </div>
    `;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${getNotificationColor(type)};
        color: white;
        padding: 12px 20px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 10000;
        font-family: 'Inter', sans-serif;
        font-size: 14px;
        max-width: 300px;
        animation: slideIn 0.3s ease-out;
    `;
    
    // Add to page
    document.body.appendChild(notification);
    
    // Auto remove after 4 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-in';
        setTimeout(() => notification.remove(), 300);
    }, 4000);
}

function getNotificationIcon(type) {
    const icons = {
        success: '✓',
        warning: '⚠',
        error: '✗',
        info: 'ℹ'
    };
    return icons[type] || icons.info;
}

function getNotificationColor(type) {
    const colors = {
        success: '#10b981',
        warning: '#f59e0b',
        error: '#ef4444',
        info: '#3b82f6'
    };
    return colors[type] || colors.info;
}

function setActiveInputType(type) {
    inputBtns.forEach(btn => btn.classList.remove('active'));
    
    if (type === 'text') {
        inputBtns[0].classList.add('active');
        document.querySelector('.file-upload').style.display = 'none';
        document.querySelector('.text-input').style.display = 'block';
    } else {
        inputBtns[1].classList.add('active');
        document.querySelector('.text-input').style.display = 'none';
        document.querySelector('.file-upload').style.display = 'block';
    }
}

// Text input handling
inputTextarea.addEventListener('input', updateStats);

function updateStats() {
    const text = inputTextarea.value;
    const words = text.trim() ? text.trim().split(/\s+/).length : 0;
    const chars = text.length;
    
    wordCount.textContent = words;
    charCount.textContent = chars;
}

// Humanize button functionality with backend API integration
humanizeBtn.addEventListener('click', async () => {
    const inputText = inputTextarea.value.trim();
    
    if (!inputText) {
        showNotification('Please enter some text to humanize.', 'warning');
        return;
    }
    
    // Update button state
    humanizeBtn.textContent = 'Processing...';
    humanizeBtn.disabled = true;
    
    try {
        // Get selected mode
        const selectedMode = outputMode.value;
        
        // Send request to backend API
        const response = await fetch('/api/humanize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: inputText,
                mode: selectedMode
            })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Humanization failed');
        }
        
        const result = await response.json();
        
        // Display results
        displayResults(result);
        
    } catch (error) {
        console.error('Humanization failed:', error);
        showNotification(`Humanization failed: ${error.message}`, 'error');
    } finally {
        // Reset button state
        humanizeBtn.textContent = 'Humanize Text';
        humanizeBtn.disabled = false;
    }
});

function displayResults(result) {
    // Display humanized text
    outputTextarea.innerHTML = result.humanizedText;
    outputPlaceholder.style.display = 'none';
    outputContent.style.display = 'block';
    
    // Update statistics
    const modeNames = {
        'fast': 'Fast Mode (Target: 75% AI, 25% Human)',
        'balanced': 'Balanced Mode (Target: 50% AI, 50% Human)', 
        'aggressive': 'Aggressive Mode (Target: 0% AI, 100% Human)'
    };
    
    // Display AI detection score
    humanizationScore.innerHTML = `
        <div class="score-display">
            <div class="score-header">${modeNames[result.mode]}</div>
            <div class="score-container">
                <div class="score-item">
                    <div class="score-label">AI-Generated</div>
                    <div class="score-value ${getScoreClass(result.achievedAIScore, result.targetAIScore)}">
                        ${result.achievedAIScore}%
                    </div>
                    <div class="score-target">Target: ${result.targetAIScore}%</div>
                </div>
                <div class="score-item">
                    <div class="score-label">Human-Written</div>
                    <div class="score-value ${getScoreClass(result.achievedHumanScore, result.targetHumanScore)}">
                        ${result.achievedHumanScore}%
                    </div>
                    <div class="score-target">Target: ${result.targetHumanScore}%</div>
                </div>
            </div>
        </div>
    `;
    
    // Display processing time
    processingTime.textContent = `${(result.processingTime / 1000).toFixed(1)}s`;
    
    // Show achievement notification
    const achievementText = getAchievementText(result.achievedAIScore, result.targetAIScore);
    showNotification(achievementText.message, achievementText.type);
}

function getScoreClass(achieved, target) {
    const difference = Math.abs(achieved - target);
    if (difference <= 10) return 'score-excellent';
    if (difference <= 20) return 'score-good';
    return 'score-needs-improvement';
}

function getAchievementText(achieved, target) {
    const difference = Math.abs(achieved - target);
    
    if (difference <= 5) {
        return {
            message: `🎯 Excellent! Achieved ${achieved}% AI detection (Target: ${target}%)`,
            type: 'success'
        };
    } else if (difference <= 15) {
        return {
            message: `✅ Good result! Achieved ${achieved}% AI detection (Target: ${target}%)`,
            type: 'success'
        };
    } else {
        return {
            message: `⚠️ Close! Achieved ${achieved}% AI detection (Target: ${target}%)`,
            type: 'warning'
        };
    }
}

// Output actions
copyBtn.addEventListener('click', async () => {
    try {
        await navigator.clipboard.writeText(outputTextarea.value);
        showNotification('Text copied to clipboard!', 'success');
    } catch (error) {
        showNotification('Failed to copy text. Please copy manually.', 'error');
    }
});

downloadBtn.addEventListener('click', () => {
    const text = outputTextarea.value;
    if (!text) {
        showNotification('No text to download.', 'warning');
        return;
    }
    
    const blob = new Blob([text], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'humanized-text.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    showNotification('Text downloaded successfully!', 'success');
});

shareBtn.addEventListener('click', async () => {
    const text = outputTextarea.value;
    if (!text) {
        showNotification('No text to share.', 'warning');
        return;
    }
    
    if (navigator.share) {
        try {
            await navigator.share({
                title: 'Humanized Text',
                text: text
            });
        } catch (error) {
            if (error.name !== 'AbortError') {
                fallbackShare(text);
            }
        }
    } else {
        fallbackShare(text);
    }
});

function fallbackShare(text) {
    try {
        navigator.clipboard.writeText(text);
        showNotification('Text copied to clipboard for sharing!', 'success');
    } catch (error) {
        showNotification('Sharing not supported. Please copy manually.', 'info');
    }
}

// Advanced options modal
advancedOptionsBtn.addEventListener('click', () => {
    modal.style.display = 'block';
});

closeModal.addEventListener('click', () => {
    modal.style.display = 'none';
});

window.addEventListener('click', (e) => {
    if (e.target === modal) {
        modal.style.display = 'none';
    }
});

// File upload handling
const fileInput = document.getElementById('fileInput');
const dropZone = document.querySelector('.drop-zone');

dropZone.addEventListener('click', () => {
    fileInput.click();
});

dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('drag-over');
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('drag-over');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('drag-over');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFileUpload(files[0]);
    }
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFileUpload(e.target.files[0]);
    }
});

async function handleFileUpload(file) {
    const allowedTypes = [
        'text/plain',
        'application/pdf',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    ];
    
    if (!allowedTypes.includes(file.type)) {
        showNotification('Please upload a TXT, PDF, DOC, or DOCX file.', 'error');
        return;
    }
    
    try {
        let text = '';
        
        if (file.type === 'text/plain') {
            text = await file.text();
        } else {
            showNotification('File uploaded. PDF and DOC files require manual text extraction.', 'info');
            return;
        }
        
        inputTextarea.value = text;
        updateStats();
        setActiveInputType('text');
        showNotification('File content loaded successfully!', 'success');
        
    } catch (error) {
        console.error('File processing failed:', error);
        showNotification('Failed to process file. Please try again.', 'error');
    }
}

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setActiveInputType('text');
    updateStats();
});

// Add CSS animations for notifications
const notificationStyles = document.createElement('style');
notificationStyles.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .notification-content {
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .notification-icon {
        font-weight: bold;
        font-size: 16px;
    }
    
    .score-display {
        text-align: center;
    }
    
    .score-header {
        font-size: 12px;
        color: #666;
        margin-bottom: 4px;
    }
    
    .score-value {
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 2px;
    }
    
    .score-target {
        font-size: 11px;
        color: #888;
    }
    
    .score-excellent {
        color: #10b981;
    }
    
    .score-good {
        color: #3b82f6;
    }
    
    .score-needs-improvement {
        color: #f59e0b;
    }
`;
document.head.appendChild(notificationStyles);


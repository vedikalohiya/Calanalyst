document.addEventListener('DOMContentLoaded', () => {
    // Elements
    const elements = {
        userInput: document.getElementById('userInput'),
        charCount: document.getElementById('charCount'),
        submitBtn: document.getElementById('submitBtn'),
        clearBtn: document.getElementById('clearBtn'),
        responseDiv: document.getElementById('response'),
        responseContent: document.getElementById('responseContent'),
        sampleQuestions: document.querySelectorAll('.chip')
    };

    // Constants
    const MAX_CHARS = 1000;
    const WARNING_THRESHOLD = 800;
    const CRITICAL_THRESHOLD = 950;

    // Character Counter
    elements.userInput.addEventListener('input', updateCharCount);

    function updateCharCount() {
        const count = elements.userInput.value.length;
        elements.charCount.textContent = `${count}/${MAX_CHARS}`;

        if (count > CRITICAL_THRESHOLD) {
            elements.charCount.style.color = 'var(--error-color)';
        } else if (count > WARNING_THRESHOLD) {
            elements.charCount.style.color = 'var(--accent-color)';
        } else {
            elements.charCount.style.color = 'var(--text-secondary)';
        }
    }

    // Clear Button
    elements.clearBtn.addEventListener('click', () => {
        elements.userInput.value = '';
        updateCharCount();
        elements.responseDiv.style.display = 'none';
        elements.userInput.focus();
    });

    // Sample Questions
    elements.sampleQuestions.forEach(chip => {
        chip.addEventListener('click', () => {
            const question = chip.getAttribute('data-question');
            elements.userInput.value = question;
            updateCharCount();
            elements.userInput.focus();
            // Optional: Auto-submit? Let's leave it for user to press send for now.
        });
    });

    // Submit Handler
    elements.submitBtn.addEventListener('click', handleSubmit);

    // Ctrl+Enter support
    elements.userInput.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.key === 'Enter') {
            handleSubmit();
        }
    });

    async function handleSubmit() {
        const query = elements.userInput.value.trim();

        if (!query) {
            showToast('Please enter a question first.', 'error');
            return;
        }

        if (query.length < 5) {
            showToast('Please describe your question in more detail.', 'warning');
            return;
        }

        setLoadingState(true);

        const formData = new FormData();
        formData.append('query', query);

        try {
            const response = await fetch('/get_response', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.message || `Server error: ${response.status}`);
            }

            renderResponse(data);

        } catch (error) {
            console.error('Submission Error:', error);
            renderError(error.message);
        } finally {
            setLoadingState(false);
        }
    }

    function setLoadingState(isLoading) {
        elements.submitBtn.disabled = isLoading;
        if (isLoading) {
            elements.submitBtn.innerHTML = '<span class="loading-spinner"></span> Processing...';
            elements.responseDiv.style.display = 'block';
            elements.responseContent.innerHTML = `
                <div class="loading">
                    <div class="dot"></div>
                    <div class="dot"></div>
                    <div class="dot"></div>
                </div>`;
        } else {
            elements.submitBtn.innerHTML = '<i class="fas fa-paper-plane"></i> Ask Now';
        }
    }

    function renderResponse(data) {
        const answer = formatText(data.answer || 'No answer provided.');
        const sourceDoc = data.source_document || 'N/A';
        const docName = data.doc || 'Unknown';

        const isError = data.answer === "Error";
        if (isError) {
            renderError(data.source_document || "Unknown error occurred.");
            return;
        }

        elements.responseDiv.style.display = 'block';
        elements.responseContent.innerHTML = `
            <div class="response-card">
                <div class="response-header">
                    <i class="fas fa-robot"></i> Answer
                </div>
                <div class="response-text">
                    ${answer}
                </div>
                <button class="source-toggle" onclick="toggleSource(this)">
                    <i class="fas fa-chevron-right"></i> View Source Context
                </button>
                <div class="source-content">
                    <div class="mb-2"><strong>Document:</strong> ${docName}</div>
                    <div><strong>Context:</strong><br>${sourceDoc}</div>
                </div>
            </div>
        `;
    }

    function renderError(message) {
        elements.responseDiv.style.display = 'block';
        elements.responseContent.innerHTML = `
            <div class="response-card" style="border-left-color: var(--error-color);">
                <div class="response-header" style="color: var(--error-color);">
                    <i class="fas fa-exclamation-circle"></i> Error
                </div>
                <div class="response-text">
                    ${message}
                </div>
            </div>
        `;
    }

    function formatText(text) {
        return text
            .replace(/\n\n/g, '<br><br>')
            .replace(/\n/g, '<br>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>');
    }

    function showToast(message, type = 'info') {
        // Simple alert for now, could be a fancy toast
        alert(message);
    }
});

// Global function for toggle because it's called from innerHTML
window.toggleSource = function (btn) {
    const content = btn.nextElementSibling;
    const icon = btn.querySelector('i');
    content.classList.toggle('show');

    if (content.classList.contains('show')) {
        icon.classList.remove('fa-chevron-right');
        icon.classList.add('fa-chevron-down');
    } else {
        icon.classList.remove('fa-chevron-down');
        icon.classList.add('fa-chevron-right');
    }
};

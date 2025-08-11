// Global variables
let currentImageId = null;
let currentDownloadUrl = null;

// Main application initialization
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Initialize form handlers
    const generateForm = document.getElementById('generateForm');
    if (generateForm) {
        initializeGenerateForm();
    }
    
    // Initialize gallery if on gallery page
    if (document.getElementById('imageModal')) {
        initializeGallery();
    }
    
    // Initialize character counter
    initializeCharacterCounter();
    
    // Initialize recent images on home page
    if (document.getElementById('recentImages')) {
        loadRecentImages();
    }
}

// Character counter for prompt textarea
function initializeCharacterCounter() {
    const promptTextarea = document.getElementById('prompt');
    const charCount = document.getElementById('charCount');
    
    if (promptTextarea && charCount) {
        promptTextarea.addEventListener('input', function() {
            charCount.textContent = this.value.length;
            
            // Visual feedback for character limit
            if (this.value.length > 900) {
                charCount.style.color = '#dc3545';
            } else if (this.value.length > 800) {
                charCount.style.color = '#fd7e14';
            } else {
                charCount.style.color = '#6c757d';
            }
        });
    }
}

// Initialize image generation form
function initializeGenerateForm() {
    const form = document.getElementById('generateForm');
    const generateBtn = document.getElementById('generateBtn');
    const loadingSection = document.getElementById('loadingSection');
    const resultSection = document.getElementById('resultSection');
    const errorSection = document.getElementById('errorSection');
    
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = new FormData(form);
        const prompt = formData.get('prompt').trim();
        const modelName = formData.get('model_name');
        
        if (!prompt) {
            showError('Please enter a prompt for your image.');
            return;
        }
        
        // Start generation process
        showLoading();
        hideError();
        hideResult();
        
        try {
            const response = await fetch('/api/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    prompt: prompt,
                    model_name: modelName
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                showResult(result);
                // Refresh recent images
                setTimeout(loadRecentImages, 1000);
            } else {
                showError(result.error || 'Failed to generate image. Please try again.');
            }
            
        } catch (error) {
            console.error('Generation error:', error);
            showError('Network error. Please check your connection and try again.');
        } finally {
            hideLoading();
        }
    });
    
    // Try again button
    const tryAgainBtn = document.getElementById('tryAgainBtn');
    if (tryAgainBtn) {
        tryAgainBtn.addEventListener('click', function() {
            hideError();
            form.scrollIntoView({ behavior: 'smooth' });
        });
    }
    
    // Generate another button
    const generateAnotherBtn = document.getElementById('generateAnotherBtn');
    if (generateAnotherBtn) {
        generateAnotherBtn.addEventListener('click', function() {
            hideResult();
            form.scrollIntoView({ behavior: 'smooth' });
            document.getElementById('prompt').focus();
        });
    }
    
    // Download button
    const downloadBtn = document.getElementById('downloadBtn');
    if (downloadBtn) {
        downloadBtn.addEventListener('click', function() {
            if (currentDownloadUrl) {
                window.open(currentDownloadUrl, '_blank');
            }
        });
    }
}

// Show loading state
function showLoading() {
    const loadingSection = document.getElementById('loadingSection');
    const generateBtn = document.getElementById('generateBtn');
    
    if (loadingSection) {
        loadingSection.classList.remove('d-none');
        loadingSection.classList.add('fade-in');
        
        // Animate progress bar
        const progressBar = loadingSection.querySelector('.progress-bar');
        if (progressBar) {
            animateProgressBar(progressBar);
        }
    }
    
    if (generateBtn) {
        generateBtn.disabled = true;
        generateBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Generating...';
    }
}

// Hide loading state
function hideLoading() {
    const loadingSection = document.getElementById('loadingSection');
    const generateBtn = document.getElementById('generateBtn');
    
    if (loadingSection) {
        loadingSection.classList.add('d-none');
    }
    
    if (generateBtn) {
        generateBtn.disabled = false;
        generateBtn.innerHTML = '<i class="fas fa-magic me-2"></i>Generate Image';
    }
}

// Show generation result
function showResult(result) {
    const resultSection = document.getElementById('resultSection');
    const imageContainer = document.getElementById('imageContainer');
    
    if (resultSection && imageContainer) {
        // Create image element
        const img = document.createElement('img');
        img.src = `/static/generated/${result.filename}`;
        img.alt = 'Generated image';
        img.className = 'img-fluid rounded shadow';
        img.style.maxHeight = '400px';
        
        // Clear container and add image
        imageContainer.innerHTML = '';
        imageContainer.appendChild(img);
        
        // Store current image info
        currentImageId = result.image_id;
        currentDownloadUrl = result.download_url;
        
        // Show result section with animation
        resultSection.classList.remove('d-none');
        resultSection.classList.add('slide-in-up');
        
        // Scroll to result
        setTimeout(() => {
            resultSection.scrollIntoView({ behavior: 'smooth' });
        }, 300);
    }
}

// Hide result section
function hideResult() {
    const resultSection = document.getElementById('resultSection');
    if (resultSection) {
        resultSection.classList.add('d-none');
        resultSection.classList.remove('slide-in-up');
    }
}

// Show error message
function showError(message) {
    const errorSection = document.getElementById('errorSection');
    const errorMessage = document.getElementById('errorMessage');
    
    if (errorSection && errorMessage) {
        errorMessage.textContent = message;
        errorSection.classList.remove('d-none');
        errorSection.classList.add('fade-in');
        
        // Scroll to error
        setTimeout(() => {
            errorSection.scrollIntoView({ behavior: 'smooth' });
        }, 100);
    }
}

// Hide error section
function hideError() {
    const errorSection = document.getElementById('errorSection');
    if (errorSection) {
        errorSection.classList.add('d-none');
        errorSection.classList.remove('fade-in');
    }
}

// Animate progress bar
function animateProgressBar(progressBar) {
    let progress = 0;
    const interval = setInterval(() => {
        progress += Math.random() * 15;
        if (progress > 90) progress = 90;
        
        progressBar.style.width = `${progress}%`;
        
        if (progress >= 90) {
            clearInterval(interval);
        }
    }, 800);
    
    // Complete the progress bar when loading is done
    return () => {
        clearInterval(interval);
        progressBar.style.width = '100%';
        setTimeout(() => {
            progressBar.style.width = '0%';
        }, 500);
    };
}

// Load recent images for home page
async function loadRecentImages() {
    const recentImagesContainer = document.getElementById('recentImages');
    if (!recentImagesContainer) return;
    
    try {
        const response = await fetch('/gallery');
        const text = await response.text();
        
        // Parse the HTML to extract recent images
        const parser = new DOMParser();
        const doc = parser.parseFromString(text, 'text/html');
        const imageCards = doc.querySelectorAll('.image-card');
        
        recentImagesContainer.innerHTML = '';
        
        if (imageCards.length === 0) {
            recentImagesContainer.innerHTML = `
                <div class="col-12 text-center py-4">
                    <p class="text-muted">No images generated yet. Create your first masterpiece!</p>
                </div>
            `;
            return;
        }
        
        // Show only first 6 images
        const recentCards = Array.from(imageCards).slice(0, 6);
        recentCards.forEach(card => {
            const col = document.createElement('div');
            col.className = 'col-lg-2 col-md-4 col-6';
            
            // Simplify the card for recent images display
            const img = card.querySelector('img');
            const title = card.querySelector('.card-title');
            
            if (img && title) {
                col.innerHTML = `
                    <div class="card h-100 shadow-sm border-0 recent-image-card">
                        <div class="recent-image-container">
                            <img src="${img.src}" class="card-img-top" alt="${title.textContent}" loading="lazy">
                        </div>
                    </div>
                `;
            }
            
            recentImagesContainer.appendChild(col);
        });
        
    } catch (error) {
        console.error('Error loading recent images:', error);
        recentImagesContainer.innerHTML = `
            <div class="col-12 text-center py-4">
                <p class="text-muted">Unable to load recent images.</p>
            </div>
        `;
    }
}

// Initialize gallery functionality
function initializeGallery() {
    // Image modal functionality
    const imageModal = document.getElementById('imageModal');
    const modalImage = document.getElementById('modalImage');
    const modalPrompt = document.getElementById('modalPrompt');
    const modalModel = document.getElementById('modalModel');
    const modalDate = document.getElementById('modalDate');
    const modalDownloadBtn = document.getElementById('modalDownloadBtn');
    
    // View buttons
    document.querySelectorAll('.view-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const imageSrc = this.dataset.imageSrc;
            const imagePrompt = this.dataset.imagePrompt;
            const imageModel = this.dataset.imageModel;
            const imageDate = this.dataset.imageDate;
            
            if (modalImage) modalImage.src = imageSrc;
            if (modalPrompt) modalPrompt.textContent = imagePrompt;
            if (modalModel) modalModel.textContent = imageModel;
            if (modalDate) modalDate.textContent = imageDate;
            if (modalDownloadBtn) {
                const filename = imageSrc.split('/').pop();
                modalDownloadBtn.href = `/download/${filename}`;
            }
        });
    });
    
    // Delete functionality
    const deleteModal = document.getElementById('deleteModal');
    const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');
    let imageToDelete = null;
    
    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.stopPropagation();
            imageToDelete = this.dataset.imageId;
            const deleteModalInstance = new bootstrap.Modal(deleteModal);
            deleteModalInstance.show();
        });
    });
    
    if (confirmDeleteBtn) {
        confirmDeleteBtn.addEventListener('click', async function() {
            if (!imageToDelete) return;
            
            try {
                const response = await fetch(`/api/delete/${imageToDelete}`, {
                    method: 'DELETE'
                });
                
                const result = await response.json();
                
                if (result.success) {
                    // Remove the image card from DOM
                    const imageCard = document.querySelector(`[data-image-id="${imageToDelete}"]`);
                    if (imageCard) {
                        imageCard.closest('.col-lg-4, .col-md-6').remove();
                    }
                    
                    // Hide modal
                    const deleteModalInstance = bootstrap.Modal.getInstance(deleteModal);
                    deleteModalInstance.hide();
                    
                    // Show success message
                    showToast('Image deleted successfully', 'success');
                    
                    // Check if page is empty and reload if needed
                    const remainingImages = document.querySelectorAll('.image-card');
                    if (remainingImages.length === 0) {
                        setTimeout(() => {
                            window.location.reload();
                        }, 1000);
                    }
                } else {
                    showToast('Failed to delete image', 'error');
                }
                
            } catch (error) {
                console.error('Delete error:', error);
                showToast('Network error while deleting image', 'error');
            }
            
            imageToDelete = null;
        });
    }
}

// Show toast notification
function showToast(message, type = 'info') {
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show position-fixed`;
    toast.style.cssText = `
        top: 100px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
        animation: slideInRight 0.3s ease-out;
    `;
    
    toast.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    document.body.appendChild(toast);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (toast.parentNode) {
            toast.remove();
        }
    }, 5000);
}

// Add custom CSS for toast animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    .recent-image-card {
        transition: transform 0.3s ease;
    }
    
    .recent-image-card:hover {
        transform: translateY(-3px);
    }
    
    .recent-image-container {
        overflow: hidden;
        border-radius: 12px;
    }
    
    .recent-image-container img {
        width: 100%;
        height: 120px;
        object-fit: cover;
        transition: transform 0.3s ease;
    }
    
    .recent-image-card:hover .recent-image-container img {
        transform: scale(1.05);
    }
`;
document.head.appendChild(style);

// Utility function to debounce API calls
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Add smooth scrolling for anchor links
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

// Add keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + Enter to generate image
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        const generateBtn = document.getElementById('generateBtn');
        if (generateBtn && !generateBtn.disabled) {
            generateBtn.click();
        }
    }
    
    // Escape to close modals
    if (e.key === 'Escape') {
        const openModal = document.querySelector('.modal.show');
        if (openModal) {
            const modalInstance = bootstrap.Modal.getInstance(openModal);
            modalInstance.hide();
        }
    }
});

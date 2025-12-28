// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const browseButton = document.getElementById('browseButton');
const fileList = document.getElementById('fileList');
const filesContainer = document.getElementById('filesContainer');
const analyzeButton = document.getElementById('analyzeButton');
const textInput = document.getElementById('textInput');
const spinner = analyzeButton.querySelector('.spinner');
const resultsContainer = document.getElementById('resultsContainer');


// Event listeners for file upload
browseButton.addEventListener('click', () => {
    fileInput.click();
});

fileInput.addEventListener('change', handleFileSelect);

// Drag and drop functionality
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('drag-over');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('drag-over');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('drag-over');
    
    if (e.dataTransfer.files.length) {
        fileInput.files = e.dataTransfer.files;
        handleFileSelect();
    }
});

// Handle file selection
function handleFileSelect() {
    const files = fileInput.files;
    
    if (files.length === 0) return;
    
    // Clear previous file list
    filesContainer.innerHTML = '';
    
    // Add each file to the list
    for (let i = 0; i < files.length; i++) {
        const file = files[i];
        addFileToList(file);
    }
    
    // Show the file list
    fileList.style.display = 'block';
    
    // Update upload area text
    uploadArea.querySelector('.upload-text').textContent = 
        `${files.length} file(s) selected. Drag and drop to add more or click to browse.`;
}

// Add a file to the displayed list
function addFileToList(file) {
    const fileItem = document.createElement('div');
    fileItem.className = 'file-item';
    
    // Get file icon based on file type
    const fileIcon = getFileIcon(file);
    
    // Format file size
    const fileSize = formatFileSize(file.size);
    
    fileItem.innerHTML = `
        <div class="file-icon">
            <i class="${fileIcon}"></i>
        </div>
        <div class="file-info">
            <div class="file-name">${file.name}</div>
            <div class="file-size">${fileSize}</div>
        </div>
        <button class="remove-file" onclick="removeFile(this)">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    filesContainer.appendChild(fileItem);
}

// Get appropriate icon for file type
function getFileIcon(file) {
    const extension = file.name.split('.').pop().toLowerCase();
    
    if (['pdf'].includes(extension)) {
        return 'fas fa-file-pdf';
    } else if (['doc', 'docx'].includes(extension)) {
        return 'fas fa-file-word';
    } else if (['txt'].includes(extension)) {
        return 'fas fa-file-alt';
    } else if (['csv', 'xls', 'xlsx'].includes(extension)) {
        return 'fas fa-file-csv';
    } else {
        return 'fas fa-file';
    }
}

// Format file size to readable format
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Remove a file from the list
function removeFile(button) {
    const fileItem = button.closest('.file-item');
    fileItem.remove();
    
    // If no files left, hide the file list
    if (filesContainer.children.length === 0) {
        fileList.style.display = 'none';
        uploadArea.querySelector('.upload-text').textContent = 
            'Drag and drop your files here or click to browse';
    }
}

// Analyze button functionality
analyzeButton.addEventListener('click', () => {
    const text = textInput.value;
    const files = fileInput.files;

    if (text.trim() === '' && files.length === 0) {
        alert('Please enter text or select files to analyze.');
        return;
    }

    const formData = new FormData();
    if (text.trim() !== '') formData.append('text', text);
    for (let i = 0; i < files.length; i++) formData.append('files', files[i]);

    // Show spinner and disable button
    analyzeButton.disabled = true;
    spinner.style.display = 'inline-block';

    fetch('/analyze', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log('Analysis Result:', data);
        // Clear previous results
        resultsContainer.innerHTML = '<h2>Analysis Results</h2>';

        // Iterate over clusters and display
        for (const clusterId in data) {
            const clusterDiv = document.createElement('div');
            clusterDiv.classList.add('cluster');

            const clusterTitle = document.createElement('h3');
            clusterTitle.textContent = `Cluster ${clusterId}`;
            clusterDiv.appendChild(clusterTitle);

            const ul = document.createElement('ul');
            data[clusterId].forEach(sentence => {
                const li = document.createElement('li');
                li.textContent = sentence;
                ul.appendChild(li);
            });

            clusterDiv.appendChild(ul);
            resultsContainer.appendChild(clusterDiv);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error during analysis');
    })
    .finally(() => {
        // Hide spinner and enable button
        analyzeButton.disabled = false;
        spinner.style.display = 'none';
    });
});

// Initial load
window.addEventListener('DOMContentLoaded', () => {
    console.log('Ontology-based Semantic Clustering interface loaded');
});
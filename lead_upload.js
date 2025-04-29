/**
 * Lead Upload Modal Interactive Features
 * 
 * This script implements the interactive features for the lead upload modal, including:
 * - Drag and drop file upload
 * - File type validation
 * - Schema mapping interface
 * - Real-time feedback on upload status
 * - GPT insight generation visualization
 */

document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const uploadModal = document.getElementById('upload-modal');
    const uploadOverlay = document.getElementById('upload-overlay');
    const uploadDropzone = document.getElementById('upload-dropzone');
    const fileInput = document.getElementById('file-input');
    const uploadBtn = document.getElementById('upload-btn');
    const closeModalBtn = document.getElementById('close-modal');
    const uploadSteps = document.querySelectorAll('.upload-step');
    const nextStepBtn = document.getElementById('next-step');
    const prevStepBtn = document.getElementById('prev-step');
    const progressBar = document.getElementById('upload-progress-bar');
    const progressText = document.getElementById('upload-progress-text');
    const fileList = document.getElementById('file-list');
    const schemaMapping = document.getElementById('schema-mapping');
    const processingStatus = document.getElementById('processing-status');
    const insightStatus = document.getElementById('insight-status');
    
    let currentStep = 0;
    let uploadedFiles = [];
    let mappingComplete = false;
    let processingComplete = false;
    let insightsComplete = false;
    
    // Open modal
    function openModal() {
        uploadModal.classList.add('active');
        uploadOverlay.classList.add('active');
    }
    
    // Close modal
    function closeModal() {
        uploadModal.classList.remove('active');
        uploadOverlay.classList.remove('active');
        resetUpload();
    }
    
    // Show current step
    function showStep(stepIndex) {
        uploadSteps.forEach((step, index) => {
            step.classList.toggle('active', index === stepIndex);
        });
        
        // Update buttons
        prevStepBtn.disabled = stepIndex === 0;
        
        if (stepIndex === 0) {
            nextStepBtn.disabled = uploadedFiles.length === 0;
            nextStepBtn.textContent = 'Next';
        } else if (stepIndex === 1) {
            nextStepBtn.disabled = !mappingComplete;
            nextStepBtn.textContent = 'Process Leads';
        } else if (stepIndex === 2) {
            nextStepBtn.disabled = !processingComplete;
            nextStepBtn.textContent = 'Generate Insights';
        } else if (stepIndex === 3) {
            nextStepBtn.disabled = !insightsComplete;
            nextStepBtn.textContent = 'Finish';
        }
        
        currentStep = stepIndex;
    }
    
    // Next step
    function nextStep() {
        if (currentStep < uploadSteps.length - 1) {
            showStep(currentStep + 1);
            
            // Simulate processing for demo purposes
            if (currentStep === 2) {
                simulateProcessing();
            } else if (currentStep === 3) {
                simulateInsights();
            }
        } else {
            closeModal();
        }
    }
    
    // Previous step
    function prevStep() {
        if (currentStep > 0) {
            showStep(currentStep - 1);
        }
    }
    
    // Handle file upload
    function handleFiles(files) {
        uploadedFiles = Array.from(files);
        
        // Clear file list
        fileList.innerHTML = '';
        
        // Display uploaded files
        uploadedFiles.forEach(file => {
            const fileItem = document.createElement('div');
            fileItem.className = 'file-item';
            
            // Determine file type icon
            let fileIcon = '📄';
            if (file.name.endsWith('.csv')) {
                fileIcon = '📊';
            } else if (file.name.endsWith('.xlsx') || file.name.endsWith('.xls')) {
                fileIcon = '📈';
            } else if (file.name.endsWith('.json')) {
                fileIcon = '📋';
            }
            
            fileItem.innerHTML = `
                <div class="file-icon">${fileIcon}</div>
                <div class="file-info">
                    <div class="file-name">${file.name}</div>
                    <div class="file-size">${formatFileSize(file.size)}</div>
                </div>
                <button class="file-remove" data-name="${file.name}">✕</button>
            `;
            
            fileList.appendChild(fileItem);
        });
        
        // Enable next button if files are uploaded
        nextStepBtn.disabled = uploadedFiles.length === 0;
        
        // Generate schema mapping preview
        generateSchemaMapping();
    }
    
    // Format file size
    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
    
    // Generate schema mapping preview
    function generateSchemaMapping() {
        // Clear schema mapping
        schemaMapping.innerHTML = '';
        
        if (uploadedFiles.length === 0) return;
        
        // Sample fields for demo
        const sampleFields = [
            { source: 'First Name', target: 'first_name', matched: true },
            { source: 'Last Name', target: 'last_name', matched: true },
            { source: 'Email Address', target: 'email', matched: true },
            { source: 'Company', target: 'company_name', matched: true },
            { source: 'Job Title', target: 'job_title', matched: true },
            { source: 'Phone', target: 'phone', matched: true },
            { source: 'Lead Source', target: 'source', matched: false },
            { source: 'Industry', target: '', matched: false },
            { source: 'Annual Revenue', target: 'revenue', matched: true },
            { source: 'Employee Count', target: 'employee_count', matched: true }
        ];
        
        // Create mapping table
        const table = document.createElement('table');
        table.className = 'mapping-table';
        
        // Create header
        const thead = document.createElement('thead');
        thead.innerHTML = `
            <tr>
                <th>Source Field</th>
                <th>Target Field</th>
                <th>Status</th>
            </tr>
        `;
        table.appendChild(thead);
        
        // Create body
        const tbody = document.createElement('tbody');
        
        sampleFields.forEach(field => {
            const row = document.createElement('tr');
            
            const sourceCell = document.createElement('td');
            sourceCell.textContent = field.source;
            row.appendChild(sourceCell);
            
            const targetCell = document.createElement('td');
            const targetSelect = document.createElement('select');
            targetSelect.className = 'target-field-select';
            
            // Add options
            const targetFields = [
                { value: '', label: '-- Select Field --' },
                { value: 'first_name', label: 'First Name' },
                { value: 'last_name', label: 'Last Name' },
                { value: 'email', label: 'Email' },
                { value: 'company_name', label: 'Company Name' },
                { value: 'job_title', label: 'Job Title' },
                { value: 'phone', label: 'Phone Number' },
                { value: 'source', label: 'Lead Source' },
                { value: 'industry', label: 'Industry' },
                { value: 'revenue', label: 'Annual Revenue' },
                { value: 'employee_count', label: 'Employee Count' }
            ];
            
            targetFields.forEach(option => {
                const optionElement = document.createElement('option');
                optionElement.value = option.value;
                optionElement.textContent = option.label;
                
                if (option.value === field.target) {
                    optionElement.selected = true;
                }
                
                targetSelect.appendChild(optionElement);
            });
            
            targetCell.appendChild(targetSelect);
            row.appendChild(targetCell);
            
            const statusCell = document.createElement('td');
            statusCell.className = 'mapping-status';
            statusCell.innerHTML = field.matched ? 
                '<span class="status-matched">✓ Matched</span>' : 
                '<span class="status-unmatched">⚠ Unmatched</span>';
            row.appendChild(statusCell);
            
            tbody.appendChild(row);
        });
        
        table.appendChild(tbody);
        schemaMapping.appendChild(table);
        
        // Add mapping actions
        const actions = document.createElement('div');
        actions.className = 'mapping-actions';
        actions.innerHTML = `
            <button id="auto-map-btn" class="btn btn-outline">Auto-Map Fields</button>
            <button id="validate-map-btn" class="btn btn-primary">Validate Mapping</button>
        `;
        schemaMapping.appendChild(actions);
        
        // Add event listeners
        document.getElementById('auto-map-btn').addEventListener('click', autoMapFields);
        document.getElementById('validate-map-btn').addEventListener('click', validateMapping);
        
        // Add event listeners to select fields
        document.querySelectorAll('.target-field-select').forEach(select => {
            select.addEventListener('change', updateMappingStatus);
        });
    }
    
    // Auto-map fields
    function autoMapFields() {
        document.querySelectorAll('.mapping-table tbody tr').forEach(row => {
            const sourceField = row.cells[0].textContent.toLowerCase();
            const selectField = row.cells[1].querySelector('select');
            
            // Simple matching logic for demo
            const options = Array.from(selectField.options);
            
            for (const option of options) {
                if (option.text.toLowerCase().includes(sourceField) || 
                    sourceField.includes(option.text.toLowerCase())) {
                    selectField.value = option.value;
                    break;
                }
            }
        });
        
        updateMappingStatus();
    }
    
    // Update mapping status
    function updateMappingStatus() {
        let unmatchedCount = 0;
        
        document.querySelectorAll('.mapping-table tbody tr').forEach(row => {
            const selectField = row.cells[1].querySelector('select');
            const statusCell = row.cells[2];
            
            if (selectField.value === '') {
                statusCell.innerHTML = '<span class="status-unmatched">⚠ Unmatched</span>';
                unmatchedCount++;
            } else {
                statusCell.innerHTML = '<span class="status-matched">✓ Matched</span>';
            }
        });
        
        // Update mapping complete status
        mappingComplete = unmatchedCount === 0;
        
        // Update next button
        if (currentStep === 1) {
            nextStepBtn.disabled = !mappingComplete;
        }
    }
    
    // Validate mapping
    function validateMapping() {
        updateMappingStatus();
        
        if (mappingComplete) {
            showNotification('Mapping validated successfully!', 'success');
        } else {
            showNotification('Please map all fields before proceeding.', 'error');
        }
    }
    
    // Simulate processing
    function simulateProcessing() {
        processingComplete = false;
        nextStepBtn.disabled = true;
        
        // Update status
        processingStatus.innerHTML = `
            <div class="status-item">
                <div class="status-icon processing">⏳</div>
                <div class="status-info">
                    <div class="status-title">Validating data format...</div>
                    <div class="status-progress">
                        <div class="progress-bar" style="width: 0%"></div>
                    </div>
                </div>
            </div>
            <div class="status-item">
                <div class="status-icon waiting">⏳</div>
                <div class="status-info">
                    <div class="status-title">Checking for duplicates...</div>
                    <div class="status-progress">
                        <div class="progress-bar" style="width: 0%"></div>
                    </div>
                </div>
            </div>
            <div class="status-item">
                <div class="status-icon waiting">⏳</div>
                <div class="status-info">
                    <div class="status-title">Importing leads...</div>
                    <div class="status-progress">
                        <div class="progress-bar" style="width: 0%"></div>
                    </div>
                </div>
            </div>
        `;
        
        // Simulate progress
        const statusItems = processingStatus.querySelectorAll('.status-item');
        const progressBars = processingStatus.querySelectorAll('.progress-bar');
        const statusIcons = processingStatus.querySelectorAll('.status-icon');
        
        // Step 1: Validating data format
        setTimeout(() => {
            simulateProgressBar(progressBars[0], 100, 1000, () => {
                statusIcons[0].className = 'status-icon complete';
                statusIcons[0].textContent = '✓';
                statusIcons[1].className = 'status-icon processing';
                
                // Step 2: Checking for duplicates
                setTimeout(() => {
                    simulateProgressBar(progressBars[1], 100, 1500, () => {
                        statusIcons[1].className = 'status-icon complete';
                        statusIcons[1].textContent = '✓';
                        statusIcons[2].className = 'status-icon processing';
                        
                        // Step 3: Importing leads
                        setTimeout(() => {
                            simulateProgressBar(progressBars[2], 100, 2000, () => {
                                statusIcons[2].className = 'status-icon complete';
                                statusIcons[2].textContent = '✓';
                                
                                // Complete
                                processingComplete = true;
                                nextStepBtn.disabled = false;
                                
                                // Show summary
                                const summary = document.createElement('div');
                                summary.className = 'processing-summary';
                                summary.innerHTML = `
                                    <div class="summary-title">Import Complete</div>
                                    <div class="summary-stats">
                                        <div class="summary-stat">
                                            <div class="stat-value">247</div>
                                            <div class="stat-label">Leads Imported</div>
                                        </div>
                                        <div class="summary-stat">
                                            <div class="stat-value">12</div>
                                            <div class="stat-label">Duplicates Found</div>
                                        </div>
                                        <div class="summary-stat">
                                            <div class="stat-value">3</div>
                                            <
(Content truncated due to size limit. Use line ranges to read in chunks)
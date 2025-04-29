/**
 * Side Panel Assistant Interactive Features
 * 
 * This script implements the interactive features for the Side Panel Assistant,
 * including AI-powered chat, contextual suggestions, and quick actions.
 */

document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const sidePanel = document.getElementById('side-panel');
    const sidePanelToggle = document.getElementById('side-panel-toggle');
    const sidePanelClose = document.getElementById('side-panel-close');
    const chatInput = document.getElementById('assistant-input');
    const chatSubmit = document.getElementById('assistant-submit');
    const chatMessages = document.getElementById('assistant-messages');
    const quickActions = document.getElementById('quick-actions');
    
    // Initialize side panel
    if (sidePanel && sidePanelToggle && sidePanelClose) {
        // Toggle side panel
        sidePanelToggle.addEventListener('click', function() {
            sidePanel.classList.toggle('active');
            
            // If opening, focus input
            if (sidePanel.classList.contains('active') && chatInput) {
                setTimeout(() => {
                    chatInput.focus();
                }, 300);
            }
        });
        
        // Close side panel
        sidePanelClose.addEventListener('click', function() {
            sidePanel.classList.remove('active');
        });
        
        // Close when clicking outside
        document.addEventListener('click', function(e) {
            if (sidePanel.classList.contains('active') && 
                !sidePanel.contains(e.target) && 
                e.target !== sidePanelToggle) {
                sidePanel.classList.remove('active');
            }
        });
    }
    
    // Initialize chat functionality
    if (chatInput && chatSubmit && chatMessages) {
        // Submit message on button click
        chatSubmit.addEventListener('click', function() {
            sendMessage();
        });
        
        // Submit message on Enter key
        chatInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });
        
        // Send message function
        function sendMessage() {
            const message = chatInput.value.trim();
            
            if (message) {
                // Add user message
                addMessage('user', message);
                
                // Clear input
                chatInput.value = '';
                
                // Process message and get response
                processMessage(message);
            }
        }
        
        // Add message to chat
        function addMessage(type, content, isLoading = false) {
            const messageElement = document.createElement('div');
            messageElement.className = `message ${type}`;
            
            if (isLoading) {
                messageElement.classList.add('loading');
                content = '<div class="loading-dots"><span></span><span></span><span></span></div>';
            }
            
            messageElement.innerHTML = `
                <div class="message-avatar">
                    ${type === 'user' ? '👤' : '🤖'}
                </div>
                <div class="message-content">
                    ${content}
                </div>
            `;
            
            chatMessages.appendChild(messageElement);
            
            // Scroll to bottom
            chatMessages.scrollTop = chatMessages.scrollHeight;
            
            return messageElement;
        }
        
        // Process message and generate response
        function processMessage(message) {
            // Add loading message
            const loadingMessage = addMessage('assistant', '', true);
            
            // Simulate processing delay
            setTimeout(() => {
                // Remove loading message
                loadingMessage.remove();
                
                // Generate response based on message content
                let response;
                
                // Simple keyword-based responses for demo
                if (message.toLowerCase().includes('lead') && message.toLowerCase().includes('import')) {
                    response = `
                        <p>I can help you import leads. Here are some options:</p>
                        <div class="assistant-actions">
                            <button class="assistant-action" data-action="upload-csv">Upload CSV File</button>
                            <button class="assistant-action" data-action="import-crm">Import from CRM</button>
                            <button class="assistant-action" data-action="manual-entry">Manual Entry</button>
                        </div>
                    `;
                } else if (message.toLowerCase().includes('report') || message.toLowerCase().includes('analytics')) {
                    response = `
                        <p>Here are the reports and analytics you might be interested in:</p>
                        <div class="assistant-actions">
                            <button class="assistant-action" data-action="lead-conversion">Lead Conversion Report</button>
                            <button class="assistant-action" data-action="sales-forecast">Sales Forecast</button>
                            <button class="assistant-action" data-action="team-performance">Team Performance</button>
                        </div>
                    `;
                } else if (message.toLowerCase().includes('task') || message.toLowerCase().includes('reminder')) {
                    response = `
                        <p>I can help you manage tasks and reminders:</p>
                        <div class="assistant-actions">
                            <button class="assistant-action" data-action="create-task">Create New Task</button>
                            <button class="assistant-action" data-action="view-tasks">View All Tasks</button>
                            <button class="assistant-action" data-action="set-reminder">Set Reminder</button>
                        </div>
                    `;
                } else if (message.toLowerCase().includes('help') || message.toLowerCase().includes('guide')) {
                    response = `
                        <p>Here are some resources to help you get started:</p>
                        <div class="assistant-actions">
                            <button class="assistant-action" data-action="quick-tour">Quick Tour</button>
                            <button class="assistant-action" data-action="video-tutorials">Video Tutorials</button>
                            <button class="assistant-action" data-action="documentation">Documentation</button>
                        </div>
                    `;
                } else {
                    // Default response with contextual suggestions
                    response = `
                        <p>I'm here to help you manage your leads and sales process. Here are some things I can assist with:</p>
                        <div class="assistant-actions">
                            <button class="assistant-action" data-action="lead-insights">Lead Insights</button>
                            <button class="assistant-action" data-action="sales-tips">Sales Tips</button>
                            <button class="assistant-action" data-action="workflow-automation">Workflow Automation</button>
                        </div>
                    `;
                }
                
                // Add assistant response
                addMessage('assistant', response);
                
                // Add event listeners to action buttons
                document.querySelectorAll('.assistant-action').forEach(button => {
                    button.addEventListener('click', function() {
                        handleAssistantAction(this.dataset.action);
                    });
                });
            }, 1500);
        }
        
        // Handle assistant action button clicks
        function handleAssistantAction(action) {
            // Different actions based on button clicked
            switch (action) {
                case 'upload-csv':
                    // Trigger lead upload modal
                    const uploadBtn = document.getElementById('upload-btn');
                    if (uploadBtn) {
                        uploadBtn.click();
                    } else {
                        addMessage('assistant', 'The lead upload feature is currently unavailable. Please try again later.');
                    }
                    break;
                    
                case 'import-crm':
                    addMessage('assistant', `
                        <p>Select a CRM to import leads from:</p>
                        <div class="assistant-actions">
                            <button class="assistant-action" data-action="import-salesforce">Salesforce</button>
                            <button class="assistant-action" data-action="import-hubspot">HubSpot</button>
                            <button class="assistant-action" data-action="import-zoho">Zoho CRM</button>
                        </div>
                    `);
                    
                    // Add event listeners to new buttons
                    document.querySelectorAll('.assistant-action').forEach(button => {
                        button.addEventListener('click', function() {
                            handleAssistantAction(this.dataset.action);
                        });
                    });
                    break;
                    
                case 'import-salesforce':
                case 'import-hubspot':
                case 'import-zoho':
                    const crmName = action.replace('import-', '');
                    addMessage('assistant', `
                        <p>Connecting to ${crmName.charAt(0).toUpperCase() + crmName.slice(1)}...</p>
                        <p>This would typically open an authentication flow to connect to your ${crmName.charAt(0).toUpperCase() + crmName.slice(1)} account and import leads.</p>
                    `);
                    break;
                    
                case 'lead-insights':
                    addMessage('assistant', `
                        <p>Here are some insights about your leads:</p>
                        <ul>
                            <li>You have 247 active leads in your pipeline</li>
                            <li>42 leads require immediate follow-up</li>
                            <li>Your lead response time has improved by 15% this month</li>
                            <li>The Financial Services sector has the highest conversion rate at 28%</li>
                        </ul>
                        <p>Would you like more detailed analytics?</p>
                        <div class="assistant-actions">
                            <button class="assistant-action" data-action="lead-analytics">View Lead Analytics</button>
                        </div>
                    `);
                    
                    // Add event listeners to new buttons
                    document.querySelectorAll('.assistant-action').forEach(button => {
                        button.addEventListener('click', function() {
                            handleAssistantAction(this.dataset.action);
                        });
                    });
                    break;
                    
                case 'sales-tips':
                    addMessage('assistant', `
                        <p>Here are some personalized sales tips based on your data:</p>
                        <ul>
                            <li><strong>Follow-up Timing:</strong> Your data shows 35% higher response rates when following up within 4 hours</li>
                            <li><strong>Email Subject Lines:</strong> Personalized subject lines are generating 28% higher open rates</li>
                            <li><strong>Call Scheduling:</strong> Tuesday and Thursday mornings show the highest answer rates</li>
                            <li><strong>Proposal Strategy:</strong> Including case studies relevant to the prospect's industry increases close rates by 22%</li>
                        </ul>
                    `);
                    break;
                    
                case 'workflow-automation':
                    addMessage('assistant', `
                        <p>Here are some workflow automation suggestions:</p>
                        <div class="assistant-actions">
                            <button class="assistant-action" data-action="auto-followup">Auto Follow-up Sequence</button>
                            <button class="assistant-action" data-action="lead-scoring">Lead Scoring Model</button>
                            <button class="assistant-action" data-action="task-automation">Task Automation</button>
                        </div>
                    `);
                    
                    // Add event listeners to new buttons
                    document.querySelectorAll('.assistant-action').forEach(button => {
                        button.addEventListener('click', function() {
                            handleAssistantAction(this.dataset.action);
                        });
                    });
                    break;
                    
                default:
                    addMessage('assistant', `I'll help you with "${action}". This feature would typically open the corresponding section of the application.`);
            }
        }
        
        // Add initial welcome message
        setTimeout(() => {
            addMessage('assistant', `
                <p>👋 Hi there! I'm your Lead Intelligence Assistant. I can help you with lead management, provide insights, and automate your workflow.</p>
                <p>What can I help you with today?</p>
            `);
        }, 500);
    }
    
    // Initialize quick actions
    if (quickActions) {
        // Add event listeners to quick action buttons
        const actionButtons = quickActions.querySelectorAll('.quick-action');
        
        actionButtons.forEach(button => {
            button.addEventListener('click', function() {
                const action = this.dataset.action;
                
                // Add message to chat
                if (chatMessages) {
                    addMessage('assistant', `I'll help you with "${this.textContent.trim()}". This feature would typically open the corresponding section of the application.`);
                }
                
                // Show notification
                showNotification(`Quick action: ${this.textContent.trim()}`, 'info');
            });
        });
    }
    
    // Show notification
    function showNotification(message, type) {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.classList.add('show');
        }, 10);
        
        setTimeout(() => {
            notification.classList.remove('show');
            
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, 3000);
    }
});

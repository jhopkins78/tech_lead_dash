/**
 * Lead Commander API Client
 * 
 * This module provides functions to interact with the Lead Commander backend API.
 */

const API = {
    /**
     * Base URL for API requests
     */
    baseUrl: '/api',

    /**
     * Make a request to the API
     * 
     * @param {string} endpoint - API endpoint
     * @param {Object} options - Fetch options
     * @returns {Promise<any>} - Response data
     */
    async request(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        
        // Set default headers
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers
        };
        
        try {
            const response = await fetch(url, {
                ...options,
                headers,
                credentials: 'same-origin' // Include cookies for authentication
            });
            
            // Handle non-JSON responses
            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('application/json')) {
                const data = await response.json();
                
                if (!response.ok) {
                    throw new Error(data.message || 'API request failed');
                }
                
                return data;
            } else {
                if (!response.ok) {
                    const text = await response.text();
                    throw new Error(text || 'API request failed');
                }
                
                return await response.text();
            }
        } catch (error) {
            console.error('API request error:', error);
            throw error;
        }
    },
    
    /**
     * Authentication
     */
    auth: {
        /**
         * Log in a user
         * 
         * @param {string} username - Username
         * @param {string} password - Password
         * @returns {Promise<Object>} - Response data
         */
        async login(username, password) {
            return API.request('/login', {
                method: 'POST',
                body: JSON.stringify({ username, password })
            });
        },
        
        /**
         * Register a new user
         * 
         * @param {string} username - Username
         * @param {string} email - Email
         * @param {string} password - Password
         * @returns {Promise<Object>} - Response data
         */
        async register(username, email, password) {
            return API.request('/register', {
                method: 'POST',
                body: JSON.stringify({ username, email, password })
            });
        },
        
        /**
         * Log out the current user
         * 
         * @returns {Promise<void>}
         */
        async logout() {
            return API.request('/logout');
        }
    },
    
    /**
     * Leads
     */
    leads: {
        /**
         * Get all leads with optional filtering
         * 
         * @param {Object} filters - Optional filters
         * @returns {Promise<Array>} - Leads data
         */
        async getAll(filters = {}) {
            // Convert filters to query string
            const queryParams = new URLSearchParams();
            Object.entries(filters).forEach(([key, value]) => {
                if (value !== undefined && value !== null) {
                    queryParams.append(key, value);
                }
            });
            
            const queryString = queryParams.toString();
            const endpoint = `/leads${queryString ? `?${queryString}` : ''}`;
            
            return API.request(endpoint);
        },
        
        /**
         * Get a single lead by ID
         * 
         * @param {string} id - Lead ID
         * @returns {Promise<Object>} - Lead data
         */
        async getById(id) {
            return API.request(`/leads/${id}`);
        },
        
        /**
         * Create a new lead
         * 
         * @param {Object} leadData - Lead data
         * @returns {Promise<Object>} - Response data
         */
        async create(leadData) {
            return API.request('/leads', {
                method: 'POST',
                body: JSON.stringify(leadData)
            });
        },
        
        /**
         * Update an existing lead
         * 
         * @param {string} id - Lead ID
         * @param {Object} leadData - Updated lead data
         * @returns {Promise<Object>} - Response data
         */
        async update(id, leadData) {
            return API.request(`/leads/${id}`, {
                method: 'PUT',
                body: JSON.stringify(leadData)
            });
        },
        
        /**
         * Delete a lead
         * 
         * @param {string} id - Lead ID
         * @returns {Promise<Object>} - Response data
         */
        async delete(id) {
            return API.request(`/leads/${id}`, {
                method: 'DELETE'
            });
        },
        
        /**
         * Upload leads from a file
         * 
         * @param {File} file - File to upload
         * @param {Object} mapping - Column mapping
         * @returns {Promise<Object>} - Response data
         */
        async upload(file, mapping = null) {
            const formData = new FormData();
            formData.append('file', file);
            
            if (mapping) {
                formData.append('mapping', JSON.stringify(mapping));
            }
            
            return API.request('/leads/upload', {
                method: 'POST',
                body: formData,
                headers: {} // Let the browser set the content type for FormData
            });
        }
    },
    
    /**
     * Tasks
     */
    tasks: {
        /**
         * Get all tasks with optional filtering
         * 
         * @param {Object} filters - Optional filters
         * @returns {Promise<Array>} - Tasks data
         */
        async getAll(filters = {}) {
            // Convert filters to query string
            const queryParams = new URLSearchParams();
            Object.entries(filters).forEach(([key, value]) => {
                if (value !== undefined && value !== null) {
                    queryParams.append(key, value);
                }
            });
            
            const queryString = queryParams.toString();
            const endpoint = `/tasks${queryString ? `?${queryString}` : ''}`;
            
            return API.request(endpoint);
        },
        
        /**
         * Create a new task
         * 
         * @param {Object} taskData - Task data
         * @returns {Promise<Object>} - Response data
         */
        async create(taskData) {
            return API.request('/tasks', {
                method: 'POST',
                body: JSON.stringify(taskData)
            });
        },
        
        /**
         * Update an existing task
         * 
         * @param {number} id - Task ID
         * @param {Object} taskData - Updated task data
         * @returns {Promise<Object>} - Response data
         */
        async update(id, taskData) {
            return API.request(`/tasks/${id}`, {
                method: 'PUT',
                body: JSON.stringify(taskData)
            });
        },
        
        /**
         * Delete a task
         * 
         * @param {number} id - Task ID
         * @returns {Promise<Object>} - Response data
         */
        async delete(id) {
            return API.request(`/tasks/${id}`, {
                method: 'DELETE'
            });
        }
    },
    
    /**
     * Workflows
     */
    workflows: {
        /**
         * Get all workflows
         * 
         * @returns {Promise<Array>} - Workflows data
         */
        async getAll() {
            return API.request('/workflows');
        },
        
        /**
         * Get a single workflow by ID
         * 
         * @param {number} id - Workflow ID
         * @returns {Promise<Object>} - Workflow data
         */
        async getById(id) {
            return API.request(`/workflows/${id}`);
        },
        
        /**
         * Create a new workflow
         * 
         * @param {Object} workflowData - Workflow data
         * @returns {Promise<Object>} - Response data
         */
        async create(workflowData) {
            return API.request('/workflows', {
                method: 'POST',
                body: JSON.stringify(workflowData)
            });
        },
        
        /**
         * Update an existing workflow
         * 
         * @param {number} id - Workflow ID
         * @param {Object} workflowData - Updated workflow data
         * @returns {Promise<Object>} - Response data
         */
        async update(id, workflowData) {
            return API.request(`/workflows/${id}`, {
                method: 'PUT',
                body: JSON.stringify(workflowData)
            });
        },
        
        /**
         * Delete a workflow
         * 
         * @param {number} id - Workflow ID
         * @returns {Promise<Object>} - Response data
         */
        async delete(id) {
            return API.request(`/workflows/${id}`, {
                method: 'DELETE'
            });
        },
        
        /**
         * Execute a workflow
         * 
         * @param {number} id - Workflow ID
         * @param {Object} data - Execution data
         * @returns {Promise<Object>} - Response data
         */
        async execute(id, data = {}) {
            return API.request(`/workflows/${id}/execute`, {
                method: 'POST',
                body: JSON.stringify(data)
            });
        }
    },
    
    /**
     * Analytics
     */
    analytics: {
        /**
         * Get lead sources analytics
         * 
         * @returns {Promise<Array>} - Lead sources data
         */
        async getLeadSources() {
            return API.request('/analytics/lead_sources');
        },
        
        /**
         * Get lead statuses analytics
         * 
         * @returns {Promise<Array>} - Lead statuses data
         */
        async getLeadStatuses() {
            return API.request('/analytics/lead_statuses');
        },
        
        /**
         * Get lead scores analytics
         * 
         * @returns {Promise<Object>} - Lead scores data
         */
        async getLeadScores() {
            return API.request('/analytics/lead_scores');
        },
        
        /**
         * Get conversion rates analytics
         * 
         * @returns {Promise<Array>} - Conversion rates data
         */
        async getConversionRates() {
            return API.request('/analytics/conversion_rates');
        },
        
        /**
         * Get activity timeline analytics
         * 
         * @returns {Promise<Array>} - Activity timeline data
         */
        async getActivityTimeline() {
            return API.request('/analytics/activity_timeline');
        }
    }
};

// Export the API client
window.API = API;

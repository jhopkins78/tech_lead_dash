/**
 * Dashboard Interactive Features
 * 
 * This script implements the core interactive features for the Lead Intelligence Dashboard,
 * including navigation, data visualization, and interactive elements.
 */

document.addEventListener('DOMContentLoaded', function() {
    // Global elements
    const sidePanel = document.getElementById('side-panel');
    const sidePanelToggle = document.getElementById('side-panel-toggle');
    const sidePanelClose = document.getElementById('side-panel-close');
    const notificationBell = document.querySelector('.notification-btn');
    const notificationPanel = document.getElementById('notification-panel');
    const searchInput = document.querySelector('.search-input');
    const searchResults = document.getElementById('search-results');
    const dateFilters = document.querySelectorAll('.date-filter-btn');
    const themeToggle = document.getElementById('theme-toggle');
    
    // Initialize charts if they exist
    initializeCharts();
    
    // Side Panel Toggle
    if (sidePanelToggle && sidePanel) {
        sidePanelToggle.addEventListener('click', function() {
            sidePanel.classList.toggle('active');
        });
    }
    
    if (sidePanelClose && sidePanel) {
        sidePanelClose.addEventListener('click', function() {
            sidePanel.classList.remove('active');
        });
    }
    
    // Notification Panel Toggle
    if (notificationBell && notificationPanel) {
        notificationBell.addEventListener('click', function(e) {
            e.stopPropagation();
            notificationPanel.classList.toggle('active');
            
            // Mark as read when opened
            const badge = notificationBell.querySelector('.notification-badge');
            if (badge) {
                badge.style.display = 'none';
            }
        });
        
        // Close notification panel when clicking outside
        document.addEventListener('click', function(e) {
            if (notificationPanel.classList.contains('active') && 
                !notificationPanel.contains(e.target) && 
                e.target !== notificationBell) {
                notificationPanel.classList.remove('active');
            }
        });
    }
    
    // Search functionality
    if (searchInput && searchResults) {
        searchInput.addEventListener('focus', function() {
            searchResults.classList.add('active');
        });
        
        searchInput.addEventListener('blur', function() {
            setTimeout(() => {
                searchResults.classList.remove('active');
            }, 200);
        });
        
        searchInput.addEventListener('input', function() {
            if (this.value.length > 2) {
                // Simulate search results
                searchResults.innerHTML = `
                    <div class="search-category">
                        <div class="category-title">Leads</div>
                        <div class="search-item">
                            <div class="item-icon">👤</div>
                            <div class="item-content">
                                <div class="item-title">John Smith</div>
                                <div class="item-subtitle">Acme Corporation</div>
                            </div>
                        </div>
                        <div class="search-item">
                            <div class="item-icon">👤</div>
                            <div class="item-content">
                                <div class="item-title">Sarah Johnson</div>
                                <div class="item-subtitle">TechGiant Solutions</div>
                            </div>
                        </div>
                    </div>
                    <div class="search-category">
                        <div class="category-title">Companies</div>
                        <div class="search-item">
                            <div class="item-icon">🏢</div>
                            <div class="item-content">
                                <div class="item-title">Acme Corporation</div>
                                <div class="item-subtitle">Technology</div>
                            </div>
                        </div>
                    </div>
                    <div class="search-category">
                        <div class="category-title">Tasks</div>
                        <div class="search-item">
                            <div class="item-icon">📋</div>
                            <div class="item-content">
                                <div class="item-title">Follow up with John Smith</div>
                                <div class="item-subtitle">Due tomorrow</div>
                            </div>
                        </div>
                    </div>
                `;
                searchResults.classList.add('active');
            } else {
                searchResults.innerHTML = '';
                searchResults.classList.remove('active');
            }
        });
    }
    
    // Date filter functionality
    if (dateFilters.length > 0) {
        dateFilters.forEach(filter => {
            filter.addEventListener('click', function() {
                dateFilters.forEach(f => f.classList.remove('active'));
                this.classList.add('active');
                
                // Trigger data refresh based on selected date range
                refreshDashboardData(this.textContent.trim());
            });
        });
    }
    
    // Theme toggle
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            document.body.classList.toggle('dark-mode');
            
            // Save preference
            const isDarkMode = document.body.classList.contains('dark-mode');
            localStorage.setItem('darkMode', isDarkMode);
            
            // Update icon
            this.textContent = isDarkMode ? '☀️' : '🌙';
        });
        
        // Check saved preference
        const savedDarkMode = localStorage.getItem('darkMode') === 'true';
        if (savedDarkMode) {
            document.body.classList.add('dark-mode');
            themeToggle.textContent = '☀️';
        }
    }
    
    // Initialize interactive tables
    initializeTables();
    
    // Initialize lead cards
    initializeLeadCards();
    
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize drag and drop for kanban boards if they exist
    initializeKanban();
});

/**
 * Initialize data visualization charts
 */
function initializeCharts() {
    // Check if Chart.js is loaded
    if (typeof Chart === 'undefined') {
        console.warn('Chart.js not loaded. Skipping chart initialization.');
        return;
    }
    
    // Sample chart configurations
    
    // Lead Funnel Chart
    const funnelCanvas = document.getElementById('lead-funnel-chart');
    if (funnelCanvas) {
        const funnelChart = new Chart(funnelCanvas, {
            type: 'bar',
            data: {
                labels: ['Leads', 'Qualified', 'Meeting', 'Proposal', 'Negotiation', 'Closed'],
                datasets: [{
                    label: 'Lead Funnel',
                    data: [247, 186, 124, 78, 42, 18],
                    backgroundColor: [
                        'rgba(72, 149, 239, 0.8)',
                        'rgba(72, 149, 239, 0.7)',
                        'rgba(72, 149, 239, 0.6)',
                        'rgba(72, 149, 239, 0.5)',
                        'rgba(72, 149, 239, 0.4)',
                        'rgba(72, 149, 239, 0.3)'
                    ],
                    borderColor: [
                        'rgba(72, 149, 239, 1)',
                        'rgba(72, 149, 239, 1)',
                        'rgba(72, 149, 239, 1)',
                        'rgba(72, 149, 239, 1)',
                        'rgba(72, 149, 239, 1)',
                        'rgba(72, 149, 239, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                indexAxis: 'y',
                scales: {
                    x: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
    
    // Lead Source Chart
    const sourceCanvas = document.getElementById('lead-source-chart');
    if (sourceCanvas) {
        const sourceChart = new Chart(sourceCanvas, {
            type: 'doughnut',
            data: {
                labels: ['Website', 'Referral', 'Social Media', 'Event', 'Email', 'Other'],
                datasets: [{
                    label: 'Lead Sources',
                    data: [35, 25, 15, 10, 10, 5],
                    backgroundColor: [
                        'rgba(67, 97, 238, 0.8)',
                        'rgba(72, 149, 239, 0.8)',
                        'rgba(76, 201, 240, 0.8)',
                        'rgba(247, 37, 133, 0.8)',
                        'rgba(248, 150, 30, 0.8)',
                        'rgba(108, 117, 125, 0.8)'
                    ],
                    borderColor: [
                        'rgba(67, 97, 238, 1)',
                        'rgba(72, 149, 239, 1)',
                        'rgba(76, 201, 240, 1)',
                        'rgba(247, 37, 133, 1)',
                        'rgba(248, 150, 30, 1)',
                        'rgba(108, 117, 125, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'right',
                    }
                }
            }
        });
    }
    
    // Lead Activity Chart
    const activityCanvas = document.getElementById('lead-activity-chart');
    if (activityCanvas) {
        const activityChart = new Chart(activityCanvas, {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                datasets: [{
                    label: 'New Leads',
                    data: [65, 78, 52, 91, 85, 107],
                    borderColor: 'rgba(67, 97, 238, 1)',
                    backgroundColor: 'rgba(67, 97, 238, 0.1)',
                    tension: 0.3,
                    fill: true
                }, {
                    label: 'Conversions',
                    data: [28, 32, 21, 37, 43, 52],
                    borderColor: 'rgba(76, 201, 240, 1)',
                    backgroundColor: 'rgba(76, 201, 240, 0.1)',
                    tension: 0.3,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
    
    // Revenue Forecast Chart
    const forecastCanvas = document.getElementById('revenue-forecast-chart');
    if (forecastCanvas) {
        const forecastChart = new Chart(forecastCanvas, {
            type: 'line',
            data: {
                labels: ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                datasets: [{
                    label: 'Projected Revenue',
                    data: [250000, 320000, 380000, 410000, 390000, 450000],
                    borderColor: 'rgba(67, 97, 238, 1)',
                    backgroundColor: 'rgba(67, 97, 238, 0.1)',
                    tension: 0.3,
                    fill: true
                }, {
                    label: 'Actual Revenue',
                    data: [240000, 310000, 360000, null, null, null],
                    borderColor: 'rgba(76, 201, 240, 1)',
                    backgroundColor: 'rgba(76, 201, 240, 0.1)',
                    tension: 0.3,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return '$' + value.toLocaleString();
                            }
                        }
                    }
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return context.dataset.label + ': $' + context.raw.toLocaleString();
                            }
                        }
                    }
                }
            }
        });
    }
    
    // Team Performance Chart
    const teamCanvas = document.getElementById('team-performance-chart');
    if (teamCanvas) {
        const teamChart = new Chart(teamCanvas, {
            type: 'radar',
            data: {
                labels: ['Lead Response', 'Follow-up', 'Qualification', 'Meetings', 'Proposals', 'Closing'],
                datasets: [{
                    label: 'Team Average',
                    data: [75, 85, 70, 80, 65, 60],
                    backgroundColor: 'rgba(67, 97, 238, 0.2)',
                    borderColor: 'rgba(67, 97, 238, 1)',
                    pointBackgroundColor: 'rgba(67, 97, 238, 1)',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'rgba(67, 97, 238, 1)'
                }, {
                    label: 'Top Performer',
                    data: [90, 95, 85, 92, 88, 80],
                    backgroundColor: 'rgba(76, 201, 240, 0.2)',
                    borderColor: 'rgba(76, 201, 240, 1)',
                    pointBackgroundColor: 'rgba(76, 201, 240, 1)',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'rgba(76, 201, 240, 1)'
                }]
            },
            options: {
                responsive: true,
                scales: {
                    r: {
                        angleLines: {
                            display: true
                        },
                        suggestedMin: 0,
                        suggestedMax: 100
                    }
                }
            }
        });
    }
    
    // Automation Performance Chart
    const automationCanvas = document.getElementById('automation-performance-chart');
    if (automationCanvas) {
        const automationChart = new Chart(automationCanvas, {
            type: 'line',
            data: {
                labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
                datasets: [{
                    label: 'Tasks Automated',
                    data: [850, 920, 1050, 1180],
                    borderColor: 'rgba(67, 97, 238, 1)',
                    backgroundColor: 'rgba(67, 97, 238, 0.1)',
                    tension: 0.3,
                    fill: true,
                    yAxisID: 'y'
                }, {
                    label: 'Time Saved (hours)',
                    data: [8.5, 9.2, 10.5, 11.8],
                    borderColor: 'rgba(76, 201, 240, 1)',
                    backgroundColor: 'rgba(76, 201, 240, 0.1)',
                    tension: 0.3,
                    fill: true,
                    yAxisID: 'y1'
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        type: 'linear',
                        display: true,
                        position: 'left',
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Tasks Automated'
                        }
                    },
                    y1: {
                        type: 'linear',
                        display: true,
                        position: 'right',
    
(Content truncated due to size limit. Use line ranges to read in chunks)
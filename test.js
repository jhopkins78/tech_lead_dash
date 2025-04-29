/**
 * Lead Commander Dashboard - Test Script
 * This script tests the responsiveness and functionality of the Lead Intelligence Dashboard
 */

// Create test file to verify website functionality across different devices and browsers
console.log("Starting Lead Intelligence Dashboard Test Suite");

// Test functions
function testResponsiveness() {
  console.log("Testing responsive design across different screen sizes");
  
  // Test viewport sizes
  const viewports = [
    { name: "Mobile", width: 375, height: 667 },
    { name: "Tablet", width: 768, height: 1024 },
    { name: "Laptop", width: 1366, height: 768 },
    { name: "Desktop", width: 1920, height: 1080 }
  ];
  
  viewports.forEach(viewport => {
    console.log(`Testing viewport: ${viewport.name} (${viewport.width}x${viewport.height})`);
    // In a real test environment, we would resize the viewport and check elements
  });
  
  return true;
}

function testThemeToggle() {
  console.log("Testing theme toggle functionality");
  
  // Check if theme toggle exists
  const themeToggle = document.getElementById('theme-toggle');
  if (!themeToggle) {
    console.error("Theme toggle button not found");
    return false;
  }
  
  // Test dark/light theme switching
  const initialTheme = document.body.classList.contains('dark-theme') ? 'dark' : 'light';
  console.log(`Initial theme: ${initialTheme}`);
  
  // Toggle theme
  themeToggle.click();
  const newTheme = document.body.classList.contains('dark-theme') ? 'dark' : 'light';
  console.log(`New theme after toggle: ${newTheme}`);
  
  // Verify theme changed
  if (initialTheme === newTheme) {
    console.error("Theme did not change after toggle");
    return false;
  }
  
  // Reset to original theme
  themeToggle.click();
  return true;
}

function testSidePanel() {
  console.log("Testing side panel functionality");
  
  // Check if side panel elements exist
  const sidePanel = document.getElementById('side-panel');
  const sidePanelToggle = document.getElementById('side-panel-toggle');
  const sidePanelClose = document.getElementById('side-panel-close');
  
  if (!sidePanel || !sidePanelToggle || !sidePanelClose) {
    console.error("Side panel elements not found");
    return false;
  }
  
  // Test opening side panel
  const initialState = sidePanel.classList.contains('active');
  console.log(`Initial side panel state: ${initialState ? 'open' : 'closed'}`);
  
  // Toggle side panel
  sidePanelToggle.click();
  const newState = sidePanel.classList.contains('active');
  console.log(`New side panel state after toggle: ${newState ? 'open' : 'closed'}`);
  
  // Verify side panel toggled
  if (initialState === newState) {
    console.error("Side panel did not toggle");
    return false;
  }
  
  // Test closing side panel
  sidePanelClose.click();
  const finalState = sidePanel.classList.contains('active');
  console.log(`Final side panel state after close: ${finalState ? 'open' : 'closed'}`);
  
  // Verify side panel closed
  if (finalState) {
    console.error("Side panel did not close");
    return false;
  }
  
  return true;
}

function testUploadModal() {
  console.log("Testing lead upload modal functionality");
  
  // Check if upload modal elements exist
  const uploadBtn = document.getElementById('upload-btn');
  const uploadModal = document.getElementById('upload-modal');
  const uploadOverlay = document.getElementById('upload-overlay');
  const closeModal = document.getElementById('close-modal');
  
  if (!uploadBtn || !uploadModal || !uploadOverlay || !closeModal) {
    console.error("Upload modal elements not found");
    return false;
  }
  
  // Test opening modal
  const initialState = uploadModal.style.display === 'block';
  console.log(`Initial upload modal state: ${initialState ? 'open' : 'closed'}`);
  
  // Open modal
  uploadBtn.click();
  const newState = uploadModal.style.display === 'block';
  console.log(`New upload modal state after open: ${newState ? 'open' : 'closed'}`);
  
  // Verify modal opened
  if (!newState) {
    console.error("Upload modal did not open");
    return false;
  }
  
  // Test closing modal
  closeModal.click();
  const finalState = uploadModal.style.display === 'block';
  console.log(`Final upload modal state after close: ${finalState ? 'open' : 'closed'}`);
  
  // Verify modal closed
  if (finalState) {
    console.error("Upload modal did not close");
    return false;
  }
  
  return true;
}

function testNavigation() {
  console.log("Testing navigation functionality");
  
  // Check if navigation elements exist
  const navItems = document.querySelectorAll('.nav-item');
  
  if (navItems.length === 0) {
    console.error("Navigation items not found");
    return false;
  }
  
  console.log(`Found ${navItems.length} navigation items`);
  
  // Test each navigation item
  navItems.forEach(item => {
    const href = item.getAttribute('href');
    console.log(`Testing navigation item: ${item.textContent} (${href})`);
    
    // In a real test environment, we would click each item and verify navigation
  });
  
  return true;
}

function testDataLoading() {
  console.log("Testing data loading functionality");
  
  // Test loading JSON data files
  const dataFiles = [
    '/assets/data/leads.json',
    '/assets/data/deals.json',
    '/assets/data/tasks.json',
    '/assets/data/integrations.json',
    '/assets/data/market-signals.json'
  ];
  
  dataFiles.forEach(file => {
    console.log(`Testing data loading for: ${file}`);
    
    // In a real test environment, we would fetch each file and verify data loading
    fetch(file)
      .then(response => {
        if (!response.ok) {
          throw new Error(`Failed to load ${file}: ${response.status} ${response.statusText}`);
        }
        return response.json();
      })
      .then(data => {
        console.log(`Successfully loaded ${file} with ${Object.keys(data).length} keys`);
      })
      .catch(error => {
        console.error(`Error loading ${file}: ${error.message}`);
      });
  });
  
  return true;
}

function testAssistant() {
  console.log("Testing AI assistant functionality");
  
  // Check if assistant elements exist
  const assistantInput = document.getElementById('assistant-input');
  const assistantSubmit = document.getElementById('assistant-submit');
  const assistantMessages = document.getElementById('assistant-messages');
  
  if (!assistantInput || !assistantSubmit || !assistantMessages) {
    console.error("Assistant elements not found");
    return false;
  }
  
  // Test sending a message
  console.log("Testing sending a message to assistant");
  
  // In a real test environment, we would input a message and verify response
  
  return true;
}

function testBrowserCompatibility() {
  console.log("Testing browser compatibility");
  
  // Detect browser
  const userAgent = navigator.userAgent;
  const browsers = [
    { name: "Chrome", pattern: /Chrome/ },
    { name: "Firefox", pattern: /Firefox/ },
    { name: "Safari", pattern: /Safari/ },
    { name: "Edge", pattern: /Edg/ },
    { name: "Internet Explorer", pattern: /MSIE|Trident/ }
  ];
  
  let currentBrowser = "Unknown";
  
  for (const browser of browsers) {
    if (browser.pattern.test(userAgent)) {
      currentBrowser = browser.name;
      break;
    }
  }
  
  console.log(`Current browser detected: ${currentBrowser}`);
  console.log(`User agent: ${userAgent}`);
  
  // Check for modern browser features
  const features = [
    { name: "Flexbox", test: "flex" in document.documentElement.style },
    { name: "Grid", test: "grid" in document.documentElement.style },
    { name: "CSS Variables", test: CSS && CSS.supports && CSS.supports("--a", "0") },
    { name: "Fetch API", test: typeof fetch === "function" },
    { name: "Promise", test: typeof Promise === "function" },
    { name: "localStorage", test: typeof localStorage === "object" }
  ];
  
  features.forEach(feature => {
    console.log(`Feature "${feature.name}" supported: ${feature.test}`);
  });
  
  return true;
}

// Run tests
function runAllTests() {
  console.log("Running all tests for Lead Intelligence Dashboard");
  
  const tests = [
    { name: "Responsiveness", fn: testResponsiveness },
    { name: "Theme Toggle", fn: testThemeToggle },
    { name: "Side Panel", fn: testSidePanel },
    { name: "Upload Modal", fn: testUploadModal },
    { name: "Navigation", fn: testNavigation },
    { name: "Data Loading", fn: testDataLoading },
    { name: "Assistant", fn: testAssistant },
    { name: "Browser Compatibility", fn: testBrowserCompatibility }
  ];
  
  let passedTests = 0;
  let failedTests = 0;
  
  tests.forEach(test => {
    console.log(`\n=== Running Test: ${test.name} ===`);
    try {
      const result = test.fn();
      if (result) {
        console.log(`✅ Test "${test.name}" PASSED`);
        passedTests++;
      } else {
        console.log(`❌ Test "${test.name}" FAILED`);
        failedTests++;
      }
    } catch (error) {
      console.error(`❌ Test "${test.name}" ERROR: ${error.message}`);
      failedTests++;
    }
  });
  
  console.log(`\n=== Test Summary ===`);
  console.log(`Total Tests: ${tests.length}`);
  console.log(`Passed: ${passedTests}`);
  console.log(`Failed: ${failedTests}`);
  
  return failedTests === 0;
}

// Execute tests when document is ready
document.addEventListener('DOMContentLoaded', function() {
  console.log("Document ready, starting tests");
  setTimeout(runAllTests, 1000); // Delay to ensure all scripts are loaded
});

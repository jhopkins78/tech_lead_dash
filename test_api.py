"""
Test script for the Lead Commander API

This script tests the basic functionality of the Lead Commander API.
It assumes the Flask application is running on http://localhost:5000.
"""

import requests
import json
import sys

BASE_URL = 'http://localhost:5000/api'
SESSION = requests.Session()

def print_separator():
    print('-' * 80)

def test_auth():
    """Test authentication endpoints"""
    print("Testing authentication...")
    
    # Test login
    login_data = {
        'username': 'admin',
        'password': 'admin123'
    }
    
    response = SESSION.post(f'{BASE_URL}/login', json=login_data)
    print(f"Login response: {response.status_code}")
    print(response.json())
    
    if response.status_code != 200:
        print("Login failed. Exiting.")
        sys.exit(1)
    
    print_separator()

def test_leads():
    """Test lead endpoints"""
    print("Testing lead endpoints...")
    
    # Get all leads
    response = SESSION.get(f'{BASE_URL}/leads')
    print(f"Get all leads response: {response.status_code}")
    leads = response.json()
    print(f"Found {len(leads)} leads")
    
    if len(leads) > 0:
        lead_id = leads[0]['id']
        
        # Get a specific lead
        response = SESSION.get(f'{BASE_URL}/leads/{lead_id}')
        print(f"Get lead {lead_id} response: {response.status_code}")
        lead = response.json()
        print(f"Lead details: {lead['firstName']} {lead['lastName']} ({lead['email']})")
        
        # Update a lead
        update_data = {
            'score': 95,
            'notes': 'Updated via test script'
        }
        response = SESSION.put(f'{BASE_URL}/leads/{lead_id}', json=update_data)
        print(f"Update lead response: {response.status_code}")
        
        # Verify update
        response = SESSION.get(f'{BASE_URL}/leads/{lead_id}')
        lead = response.json()
        print(f"Updated lead score: {lead['score']}, notes: {lead['notes']}")
    
    # Create a new lead
    new_lead = {
        'firstName': 'Test',
        'lastName': 'User',
        'email': 'test.user@example.com',
        'company': 'Test Company',
        'position': 'Tester',
        'phone': '(555) 123-4567',
        'status': 'New',
        'score': 50,
        'source': 'Test Script',
        'notes': 'Created via test script',
        'tags': ['Test']
    }
    
    response = SESSION.post(f'{BASE_URL}/leads', json=new_lead)
    print(f"Create lead response: {response.status_code}")
    if response.status_code == 201:
        result = response.json()
        print(f"Created lead with ID: {result['id']}")
        
        # Delete the test lead
        response = SESSION.delete(f'{BASE_URL}/leads/{result["id"]}')
        print(f"Delete lead response: {response.status_code}")
    
    print_separator()

def test_tasks():
    """Test task endpoints"""
    print("Testing task endpoints...")
    
    # Get all tasks
    response = SESSION.get(f'{BASE_URL}/tasks')
    print(f"Get all tasks response: {response.status_code}")
    tasks = response.json()
    print(f"Found {len(tasks)} tasks")
    
    # Create a new task
    new_task = {
        'title': 'Test Task',
        'description': 'This is a test task created via the test script',
        'priority': 'Medium',
        'status': 'Pending',
        'dueDate': '2025-05-15T12:00:00'
    }
    
    response = SESSION.post(f'{BASE_URL}/tasks', json=new_task)
    print(f"Create task response: {response.status_code}")
    if response.status_code == 201:
        result = response.json()
        task_id = result['id']
        print(f"Created task with ID: {task_id}")
        
        # Update the task
        update_data = {
            'status': 'Completed',
            'priority': 'High'
        }
        response = SESSION.put(f'{BASE_URL}/tasks/{task_id}', json=update_data)
        print(f"Update task response: {response.status_code}")
        
        # Delete the task
        response = SESSION.delete(f'{BASE_URL}/tasks/{task_id}')
        print(f"Delete task response: {response.status_code}")
    
    print_separator()

def test_workflows():
    """Test workflow endpoints"""
    print("Testing workflow endpoints...")
    
    # Get all workflows
    response = SESSION.get(f'{BASE_URL}/workflows')
    print(f"Get all workflows response: {response.status_code}")
    workflows = response.json()
    print(f"Found {len(workflows)} workflows")
    
    if len(workflows) > 0:
        workflow_id = workflows[0]['id']
        
        # Get a specific workflow
        response = SESSION.get(f'{BASE_URL}/workflows/{workflow_id}')
        print(f"Get workflow {workflow_id} response: {response.status_code}")
        workflow = response.json()
        print(f"Workflow details: {workflow['name']} ({workflow['status']})")
        
        # Execute a workflow
        if workflow['status'] == 'Active':
            response = SESSION.post(f'{BASE_URL}/workflows/{workflow_id}/execute', json={})
            print(f"Execute workflow response: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print(f"Workflow execution ID: {result['executionId']}")
    
    print_separator()

def test_analytics():
    """Test analytics endpoints"""
    print("Testing analytics endpoints...")
    
    # Test lead sources analytics
    response = SESSION.get(f'{BASE_URL}/analytics/lead_sources')
    print(f"Lead sources analytics response: {response.status_code}")
    if response.status_code == 200:
        sources = response.json()
        print(f"Lead sources: {sources}")
    
    # Test lead statuses analytics
    response = SESSION.get(f'{BASE_URL}/analytics/lead_statuses')
    print(f"Lead statuses analytics response: {response.status_code}")
    if response.status_code == 200:
        statuses = response.json()
        print(f"Lead statuses: {statuses}")
    
    # Test lead scores analytics
    response = SESSION.get(f'{BASE_URL}/analytics/lead_scores')
    print(f"Lead scores analytics response: {response.status_code}")
    if response.status_code == 200:
        scores = response.json()
        print(f"Average lead score: {scores['averageScore']}")
    
    print_separator()

def test_logout():
    """Test logout endpoint"""
    print("Testing logout...")
    
    response = SESSION.get(f'{BASE_URL}/logout')
    print(f"Logout response: {response.status_code}")
    
    print_separator()

def main():
    """Run all tests"""
    print("Starting Lead Commander API tests...")
    print_separator()
    
    try:
        test_auth()
        test_leads()
        test_tasks()
        test_workflows()
        test_analytics()
        test_logout()
        
        print("All tests completed successfully!")
    except Exception as e:
        print(f"Error during tests: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()

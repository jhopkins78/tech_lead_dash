import os
import sys
import platform
from datetime import datetime, timedelta
import random
from werkzeug.security import generate_password_hash
import sqlite3
import json

# Check Python version
if sys.version_info < (3, 10):
    print("Error: Python 3.10 or higher is required.")
    print(f"Current Python version: {platform.python_version()}")
    sys.exit(1)

# Add the current directory to the path so we can import the app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, User, Lead, Tag, LeadTag, Activity, Task, Workflow, WorkflowStep

def init_db():
    """Initialize the database with sample data"""
    print("Creating database tables...")
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Check if admin user exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            print("Creating admin user...")
            admin = User(
                username='admin',
                email='admin@example.com',
                role='admin'
            )
            admin.set_password('admin123')  # Change this in production!
            db.session.add(admin)
            
            # Create a regular user
            user = User(
                username='user',
                email='user@example.com',
                role='user'
            )
            user.set_password('user123')  # Change this in production!
            db.session.add(user)
            
            db.session.commit()
            print("Admin user created successfully.")
        else:
            print("Admin user already exists.")
        
        # Check if we have any leads
        if Lead.query.count() == 0:
            print("Creating sample leads...")
            create_sample_leads()
            print("Sample leads created successfully.")
        else:
            print("Leads already exist in the database.")
        
        # Check if we have any workflows
        if Workflow.query.count() == 0:
            print("Creating sample workflows...")
            create_sample_workflows()
            print("Sample workflows created successfully.")
        else:
            print("Workflows already exist in the database.")

def create_sample_leads():
    """Create sample leads data"""
    with app.app_context():
        # Create tags
        tags = [
            "High Value", "Enterprise", "SMB", "Tech", "Finance", 
            "Healthcare", "Education", "Manufacturing", "Retail",
            "Hot Lead", "Cold Lead", "Nurturing", "Decision Maker"
        ]
        
        for tag_name in tags:
            tag = Tag(name=tag_name)
            db.session.add(tag)
        
        db.session.commit()
        
        # Get tag IDs
        tag_ids = {tag.name: tag.id for tag in Tag.query.all()}
        
        # Create leads
        leads_data = []
        
        # Try to load from leads.json if it exists
        try:
            with open('leads.json', 'r') as f:
                data = json.load(f)
                leads_data = data.get('leads', [])
        except (FileNotFoundError, json.JSONDecodeError):
            # Use default sample data if file doesn't exist or is invalid
            leads_data = [
                {
                    "firstName": "John",
                    "lastName": "Smith",
                    "company": "Acme Corporation",
                    "position": "CTO",
                    "email": "john.smith@acmecorp.com",
                    "phone": "(555) 123-4567",
                    "status": "Qualified",
                    "score": 85,
                    "source": "Website",
                    "notes": "Interested in enterprise solution",
                    "tags": ["Tech", "Enterprise", "High Value"]
                },
                {
                    "firstName": "Sarah",
                    "lastName": "Johnson",
                    "company": "Globex Inc",
                    "position": "Marketing Director",
                    "email": "sarah.j@globexinc.com",
                    "phone": "(555) 234-5678",
                    "status": "New",
                    "score": 65,
                    "source": "Trade Show",
                    "notes": "Requested product demo",
                    "tags": ["Marketing", "Mid-Market"]
                },
                {
                    "firstName": "Michael",
                    "lastName": "Brown",
                    "company": "Initech",
                    "position": "CEO",
                    "email": "michael.brown@initech.com",
                    "phone": "(555) 345-6789",
                    "status": "Contacted",
                    "score": 92,
                    "source": "Referral",
                    "notes": "Follow up next week",
                    "tags": ["Decision Maker", "High Value"]
                },
                {
                    "firstName": "Emily",
                    "lastName": "Davis",
                    "company": "Umbrella Corp",
                    "position": "Sales Manager",
                    "email": "emily.davis@umbrellacorp.com",
                    "phone": "(555) 456-7890",
                    "status": "Proposal",
                    "score": 78,
                    "source": "LinkedIn",
                    "notes": "Sent proposal on 04/17",
                    "tags": ["Sales", "Enterprise"]
                },
                {
                    "firstName": "David",
                    "lastName": "Wilson",
                    "company": "Stark Industries",
                    "position": "IT Director",
                    "email": "david.wilson@stark.com",
                    "phone": "(555) 567-8901",
                    "status": "Negotiation",
                    "score": 88,
                    "source": "Webinar",
                    "notes": "Discussing contract terms",
                    "tags": ["Tech", "Enterprise", "Hot Lead"]
                }
            ]
        
        # Add leads to database
        for lead_data in leads_data:
            lead_id = f"LD{random.randint(100000, 999999)}"
            
            # Create lead
            lead = Lead(
                id=lead_id,
                first_name=lead_data.get("firstName"),
                last_name=lead_data.get("lastName"),
                company=lead_data.get("company"),
                position=lead_data.get("position"),
                email=lead_data.get("email"),
                phone=lead_data.get("phone"),
                status=lead_data.get("status", "New"),
                score=lead_data.get("score", 0),
                source=lead_data.get("source"),
                notes=lead_data.get("notes"),
                last_contact=datetime.utcnow() - timedelta(days=random.randint(0, 30))
            )
            
            db.session.add(lead)
            db.session.flush()  # Flush to get the lead ID
            
            # Add tags
            for tag_name in lead_data.get("tags", []):
                # Skip tags that don't exist in our predefined list
                if tag_name in tag_ids:
                    lead_tag = LeadTag(lead_id=lead_id, tag_id=tag_ids[tag_name])
                    db.session.add(lead_tag)
            
            # Add activity
            activity = Activity(
                lead_id=lead_id,
                activity_type="Created",
                description="Lead created during system initialization",
                created_at=datetime.utcnow() - timedelta(days=random.randint(0, 30))
            )
            db.session.add(activity)
            
            # Add a task for some leads
            if random.random() > 0.5:
                task = Task(
                    title=f"Follow up with {lead_data.get('firstName')} {lead_data.get('lastName')}",
                    description=f"Discuss their interest in our products",
                    due_date=datetime.utcnow() + timedelta(days=random.randint(1, 14)),
                    priority=random.choice(["High", "Medium", "Low"]),
                    status="Pending",
                    lead_id=lead_id,
                    assigned_to=1,  # Assign to admin
                    created_by=1
                )
                db.session.add(task)
        
        db.session.commit()

def create_sample_workflows():
    """Create sample workflows"""
    with app.app_context():
        # Create a lead qualification workflow
        workflow = Workflow(
            name="Lead Qualification Automation",
            description="Automatically scores and qualifies new leads based on predefined criteria",
            status="Active",
            created_by=1  # Admin user
        )
        db.session.add(workflow)
        db.session.flush()  # Flush to get the workflow ID
        
        # Add steps
        steps = [
            {
                "type": "Trigger",
                "config": json.dumps({
                    "event": "new_lead",
                    "description": "Triggered when a new lead is created"
                }),
                "position": 0
            },
            {
                "type": "Condition",
                "config": json.dumps({
                    "field": "email",
                    "operator": "contains",
                    "value": "@",
                    "description": "Check if email is valid"
                }),
                "position": 1
            },
            {
                "type": "Action",
                "config": json.dumps({
                    "action": "score_lead",
                    "parameters": {
                        "rules": [
                            {"field": "company", "points": 10, "description": "Has company information"},
                            {"field": "phone", "points": 5, "description": "Has phone number"},
                            {"field": "position", "points": 5, "description": "Has job position"}
                        ]
                    },
                    "description": "Score lead based on available information"
                }),
                "position": 2
            },
            {
                "type": "Condition",
                "config": json.dumps({
                    "field": "score",
                    "operator": ">=",
                    "value": 15,
                    "description": "Check if lead score is high enough"
                }),
                "position": 3
            },
            {
                "type": "Action",
                "config": json.dumps({
                    "action": "update_lead",
                    "parameters": {
                        "status": "Qualified"
                    },
                    "description": "Mark lead as qualified"
                }),
                "position": 4
            },
            {
                "type": "Action",
                "config": json.dumps({
                    "action": "create_task",
                    "parameters": {
                        "title": "Follow up with qualified lead",
                        "description": "Contact the lead to discuss their needs",
                        "priority": "High",
                        "assignTo": "user"
                    },
                    "description": "Create follow-up task"
                }),
                "position": 5
            }
        ]
        
        for step_data in steps:
            step = WorkflowStep(
                workflow_id=workflow.id,
                step_type=step_data["type"],
                step_config=step_data["config"],
                position=step_data["position"]
            )
            db.session.add(step)
        
        db.session.commit()
        
        # Update next_step_id for each step
        steps = WorkflowStep.query.filter_by(workflow_id=workflow.id).order_by(WorkflowStep.position).all()
        for i in range(len(steps) - 1):
            steps[i].next_step_id = steps[i + 1].id
        
        # Create a follow-up sequence workflow
        workflow = Workflow(
            name="Follow-up Sequence",
            description="Sends personalized follow-up emails based on lead engagement and response",
            status="Active",
            created_by=1  # Admin user
        )
        db.session.add(workflow)
        db.session.flush()  # Flush to get the workflow ID
        
        # Add steps
        steps = [
            {
                "type": "Trigger",
                "config": json.dumps({
                    "event": "status_change",
                    "parameters": {
                        "status": "Contacted"
                    },
                    "description": "Triggered when a lead status changes to Contacted"
                }),
                "position": 0
            },
            {
                "type": "Action",
                "config": json.dumps({
                    "action": "wait",
                    "parameters": {
                        "days": 3
                    },
                    "description": "Wait for 3 days"
                }),
                "position": 1
            },
            {
                "type": "Condition",
                "config": json.dumps({
                    "field": "status",
                    "operator": "==",
                    "value": "Contacted",
                    "description": "Check if lead is still in Contacted status"
                }),
                "position": 2
            },
            {
                "type": "Action",
                "config": json.dumps({
                    "action": "send_email",
                    "parameters": {
                        "template": "follow_up_1",
                        "subject": "Following up on our conversation"
                    },
                    "description": "Send first follow-up email"
                }),
                "position": 3
            },
            {
                "type": "Action",
                "config": json.dumps({
                    "action": "wait",
                    "parameters": {
                        "days": 5
                    },
                    "description": "Wait for 5 days"
                }),
                "position": 4
            },
            {
                "type": "Condition",
                "config": json.dumps({
                    "field": "status",
                    "operator": "==",
                    "value": "Contacted",
                    "description": "Check if lead is still in Contacted status"
                }),
                "position": 5
            },
            {
                "type": "Action",
                "config": json.dumps({
                    "action": "send_email",
                    "parameters": {
                        "template": "follow_up_2",
                        "subject": "Are you still interested?"
                    },
                    "description": "Send second follow-up email"
                }),
                "position": 6
            }
        ]
        
        for step_data in steps:
            step = WorkflowStep(
                workflow_id=workflow.id,
                step_type=step_data["type"],
                step_config=step_data["config"],
                position=step_data["position"]
            )
            db.session.add(step)
        
        db.session.commit()
        
        # Update next_step_id for each step
        steps = WorkflowStep.query.filter_by(workflow_id=workflow.id).order_by(WorkflowStep.position).all()
        for i in range(len(steps) - 1):
            steps[i].next_step_id = steps[i + 1].id
        
        db.session.commit()

if __name__ == "__main__":
    init_db()
    print("Database initialization complete.")

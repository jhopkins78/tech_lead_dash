from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import json
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
import uuid
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Change this to a random secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lead_commander.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Define models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Lead(db.Model):
    id = db.Column(db.String(10), primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100))
    position = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    status = db.Column(db.String(50), default='New')
    score = db.Column(db.Integer, default=0)
    last_contact = db.Column(db.DateTime)
    source = db.Column(db.String(50))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tags = db.relationship('LeadTag', backref='lead', lazy=True, cascade="all, delete-orphan")
    activities = db.relationship('Activity', backref='lead', lazy=True, cascade="all, delete-orphan")
    tasks = db.relationship('Task', backref='lead', lazy=True, cascade="all, delete-orphan")

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

class LeadTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lead_id = db.Column(db.String(10), db.ForeignKey('lead.id', ondelete='CASCADE'), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id', ondelete='CASCADE'), nullable=False)

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lead_id = db.Column(db.String(10), db.ForeignKey('lead.id', ondelete='CASCADE'), nullable=False)
    activity_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    user = db.relationship('User', backref='activities')

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.DateTime)
    priority = db.Column(db.String(20), default='Medium')
    status = db.Column(db.String(20), default='Pending')
    lead_id = db.Column(db.String(10), db.ForeignKey('lead.id', ondelete='SET NULL'))
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    assignee = db.relationship('User', foreign_keys=[assigned_to], backref='assigned_tasks')
    creator = db.relationship('User', foreign_keys=[created_by], backref='created_tasks')

class Workflow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='Draft')  # Draft, Active, Paused
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    creator = db.relationship('User', backref='workflows')
    steps = db.relationship('WorkflowStep', backref='workflow', lazy=True, cascade="all, delete-orphan")
    executions = db.relationship('WorkflowExecution', backref='workflow', lazy=True)

class WorkflowStep(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    workflow_id = db.Column(db.Integer, db.ForeignKey('workflow.id', ondelete='CASCADE'), nullable=False)
    step_type = db.Column(db.String(50), nullable=False)  # Trigger, Action, Condition
    step_config = db.Column(db.Text)  # JSON configuration
    position = db.Column(db.Integer)
    next_step_id = db.Column(db.Integer, db.ForeignKey('workflow_step.id'))

class WorkflowExecution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    workflow_id = db.Column(db.Integer, db.ForeignKey('workflow.id', ondelete='CASCADE'), nullable=False)
    lead_id = db.Column(db.String(10), db.ForeignKey('lead.id'))
    status = db.Column(db.String(20), default='Running')  # Running, Completed, Failed
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    result = db.Column(db.Text)  # JSON result data

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes for authentication
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        username = data.get('username')
        password = data.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            if request.is_json:
                return jsonify({'success': True, 'redirect': url_for('dashboard')})
            return redirect(url_for('dashboard'))
        
        if request.is_json:
            return jsonify({'success': False, 'message': 'Invalid username or password'})
        flash('Invalid username or password')
        return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        # Check if username or email already exists
        if User.query.filter_by(username=username).first():
            if request.is_json:
                return jsonify({'success': False, 'message': 'Username already exists'})
            flash('Username already exists')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            if request.is_json:
                return jsonify({'success': False, 'message': 'Email already exists'})
            flash('Email already exists')
            return redirect(url_for('register'))
        
        # Create new user
        user = User(username=username, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        if request.is_json:
            return jsonify({'success': True, 'redirect': url_for('login')})
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    
    return render_template('register.html')

# Main routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('index.html')

@app.route('/lead_intelligence')
@login_required
def lead_intelligence():
    return render_template('lead_intelligence_center.html')

@app.route('/automation')
@login_required
def automation():
    return render_template('automation_control_room.html')

# API routes for leads
@app.route('/api/leads', methods=['GET'])
@login_required
def get_leads():
    # Get query parameters for filtering
    status = request.args.get('status')
    source = request.args.get('source')
    min_score = request.args.get('min_score')
    max_score = request.args.get('max_score')
    tag = request.args.get('tag')
    
    # Start with base query
    query = Lead.query
    
    # Apply filters if provided
    if status:
        query = query.filter(Lead.status == status)
    if source:
        query = query.filter(Lead.source == source)
    if min_score:
        query = query.filter(Lead.score >= int(min_score))
    if max_score:
        query = query.filter(Lead.score <= int(max_score))
    if tag:
        query = query.join(LeadTag).join(Tag).filter(Tag.name == tag)
    
    # Get leads
    leads = query.order_by(Lead.created_at.desc()).all()
    
    # Convert to JSON
    result = []
    for lead in leads:
        lead_tags = [tag.tag_id for tag in lead.tags]
        tag_names = [Tag.query.get(tag_id).name for tag_id in lead_tags]
        
        result.append({
            'id': lead.id,
            'firstName': lead.first_name,
            'lastName': lead.last_name,
            'company': lead.company,
            'position': lead.position,
            'email': lead.email,
            'phone': lead.phone,
            'status': lead.status,
            'score': lead.score,
            'lastContact': lead.last_contact.isoformat() if lead.last_contact else None,
            'source': lead.source,
            'notes': lead.notes,
            'tags': tag_names,
            'createdAt': lead.created_at.isoformat(),
            'updatedAt': lead.updated_at.isoformat()
        })
    
    return jsonify(result)

@app.route('/api/leads/<lead_id>', methods=['GET'])
@login_required
def get_lead(lead_id):
    lead = Lead.query.get_or_404(lead_id)
    
    lead_tags = [tag.tag_id for tag in lead.tags]
    tag_names = [Tag.query.get(tag_id).name for tag_id in lead_tags]
    
    # Get activities
    activities = []
    for activity in lead.activities:
        activities.append({
            'id': activity.id,
            'type': activity.activity_type,
            'description': activity.description,
            'createdAt': activity.created_at.isoformat(),
            'user': activity.user.username if activity.user else None
        })
    
    # Get tasks
    tasks = []
    for task in lead.tasks:
        tasks.append({
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'dueDate': task.due_date.isoformat() if task.due_date else None,
            'priority': task.priority,
            'status': task.status,
            'assignee': task.assignee.username if task.assignee else None
        })
    
    result = {
        'id': lead.id,
        'firstName': lead.first_name,
        'lastName': lead.last_name,
        'company': lead.company,
        'position': lead.position,
        'email': lead.email,
        'phone': lead.phone,
        'status': lead.status,
        'score': lead.score,
        'lastContact': lead.last_contact.isoformat() if lead.last_contact else None,
        'source': lead.source,
        'notes': lead.notes,
        'tags': tag_names,
        'activities': activities,
        'tasks': tasks,
        'createdAt': lead.created_at.isoformat(),
        'updatedAt': lead.updated_at.isoformat()
    }
    
    return jsonify(result)

@app.route('/api/leads', methods=['POST'])
@login_required
def create_lead():
    data = request.get_json()
    
    # Generate a unique ID
    lead_id = f"LD{str(uuid.uuid4())[:6].upper()}"
    
    # Create new lead
    lead = Lead(
        id=lead_id,
        first_name=data['firstName'],
        last_name=data['lastName'],
        company=data.get('company'),
        position=data.get('position'),
        email=data['email'],
        phone=data.get('phone'),
        status=data.get('status', 'New'),
        score=data.get('score', 0),
        source=data.get('source'),
        notes=data.get('notes')
    )
    
    if data.get('lastContact'):
        lead.last_contact = datetime.fromisoformat(data['lastContact'])
    
    db.session.add(lead)
    
    # Add tags
    if data.get('tags'):
        for tag_name in data['tags']:
            # Check if tag exists, create if not
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                db.session.add(tag)
                db.session.flush()
            
            # Create lead-tag association
            lead_tag = LeadTag(lead_id=lead_id, tag_id=tag.id)
            db.session.add(lead_tag)
    
    # Add activity
    activity = Activity(
        lead_id=lead_id,
        activity_type='Created',
        description=f"Lead created by {current_user.username}",
        user_id=current_user.id
    )
    db.session.add(activity)
    
    db.session.commit()
    
    return jsonify({'success': True, 'id': lead_id}), 201

@app.route('/api/leads/<lead_id>', methods=['PUT'])
@login_required
def update_lead(lead_id):
    lead = Lead.query.get_or_404(lead_id)
    data = request.get_json()
    
    # Update lead fields
    if 'firstName' in data:
        lead.first_name = data['firstName']
    if 'lastName' in data:
        lead.last_name = data['lastName']
    if 'company' in data:
        lead.company = data['company']
    if 'position' in data:
        lead.position = data['position']
    if 'email' in data:
        lead.email = data['email']
    if 'phone' in data:
        lead.phone = data['phone']
    if 'status' in data:
        old_status = lead.status
        lead.status = data['status']
        
        # Add status change activity
        if old_status != data['status']:
            activity = Activity(
                lead_id=lead_id,
                activity_type='Status Change',
                description=f"Status changed from {old_status} to {data['status']} by {current_user.username}",
                user_id=current_user.id
            )
            db.session.add(activity)
    
    if 'score' in data:
        lead.score = data['score']
    if 'lastContact' in data and data['lastContact']:
        lead.last_contact = datetime.fromisoformat(data['lastContact'])
    if 'source' in data:
        lead.source = data['source']
    if 'notes' in data:
        lead.notes = data['notes']
    
    # Update tags
    if 'tags' in data:
        # Remove existing tags
        LeadTag.query.filter_by(lead_id=lead_id).delete()
        
        # Add new tags
        for tag_name in data['tags']:
            # Check if tag exists, create if not
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                db.session.add(tag)
                db.session.flush()
            
            # Create lead-tag association
            lead_tag = LeadTag(lead_id=lead_id, tag_id=tag.id)
            db.session.add(lead_tag)
    
    # Add update activity
    activity = Activity(
        lead_id=lead_id,
        activity_type='Updated',
        description=f"Lead updated by {current_user.username}",
        user_id=current_user.id
    )
    db.session.add(activity)
    
    db.session.commit()
    
    return jsonify({'success': True})

@app.route('/api/leads/<lead_id>', methods=['DELETE'])
@login_required
def delete_lead(lead_id):
    lead = Lead.query.get_or_404(lead_id)
    
    db.session.delete(lead)
    db.session.commit()
    
    return jsonify({'success': True})

# API routes for lead uploads
@app.route('/api/leads/upload', methods=['POST'])
@login_required
def upload_leads():
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No selected file'}), 400
    
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Process file based on extension
        try:
            if filename.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif filename.endswith(('.xls', '.xlsx')):
                df = pd.read_excel(file_path)
            else:
                return jsonify({'success': False, 'message': 'Unsupported file format'}), 400
            
            # Get column mapping from request
            mapping = request.form.get('mapping')
            if mapping:
                mapping = json.loads(mapping)
            else:
                # Default mapping (assuming standard column names)
                mapping = {
                    'firstName': 'firstName',
                    'lastName': 'lastName',
                    'email': 'email',
                    'company': 'company',
                    'position': 'position',
                    'phone': 'phone',
                    'status': 'status',
                    'source': 'source',
                    'notes': 'notes'
                }
            
            # Process leads
            leads_added = 0
            leads_updated = 0
            leads_failed = 0
            
            for _, row in df.iterrows():
                try:
                    # Map columns
                    lead_data = {}
                    for target_field, source_field in mapping.items():
                        if source_field in row and not pd.isna(row[source_field]):
                            lead_data[target_field] = row[source_field]
                    
                    # Check if lead exists (by email)
                    if 'email' not in lead_data:
                        leads_failed += 1
                        continue
                    
                    existing_lead = Lead.query.filter_by(email=lead_data['email']).first()
                    
                    if existing_lead:
                        # Update existing lead
                        if 'firstName' in lead_data:
                            existing_lead.first_name = lead_data['firstName']
                        if 'lastName' in lead_data:
                            existing_lead.last_name = lead_data['lastName']
                        if 'company' in lead_data:
                            existing_lead.company = lead_data['company']
                        if 'position' in lead_data:
                            existing_lead.position = lead_data['position']
                        if 'phone' in lead_data:
                            existing_lead.phone = lead_data['phone']
                        if 'status' in lead_data:
                            existing_lead.status = lead_data['status']
                        if 'source' in lead_data:
                            existing_lead.source = lead_data['source']
                        if 'notes' in lead_data:
                            existing_lead.notes = lead_data['notes']
                        
                        leads_updated += 1
                    else:
                        # Create new lead
                        if 'firstName' not in lead_data or 'lastName' not in lead_data:
                            leads_failed += 1
                            continue
                        
                        # Generate a unique ID
                        lead_id = f"LD{str(uuid.uuid4())[:6].upper()}"
                        
                        new_lead = Lead(
                            id=lead_id,
                            first_name=lead_data['firstName'],
                            last_name=lead_data['lastName'],
                            email=lead_data['email'],
                            company=lead_data.get('company'),
                            position=lead_data.get('position'),
                            phone=lead_data.get('phone'),
                            status=lead_data.get('status', 'New'),
                            source=lead_data.get('source', 'Import'),
                            notes=lead_data.get('notes')
                        )
                        
                        db.session.add(new_lead)
                        
                        # Add activity
                        activity = Activity(
                            lead_id=lead_id,
                            activity_type='Created',
                            description=f"Lead created from import by {current_user.username}",
                            user_id=current_user.id
                        )
                        db.session.add(activity)
                        
                        leads_added += 1
                
                except Exception as e:
                    logger.error(f"Error processing lead: {str(e)}")
                    leads_failed += 1
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'added': leads_added,
                'updated': leads_updated,
                'failed': leads_failed
            })
        
        except Exception as e:
            logger.error(f"Error processing file: {str(e)}")
            return jsonify({'success': False, 'message': f'Error processing file: {str(e)}'}), 500
        
        finally:
            # Clean up the uploaded file
            if os.path.exists(file_path):
                os.remove(file_path)
    
    return jsonify({'success': False, 'message': 'Unknown error'}), 500

# API routes for tasks
@app.route('/api/tasks', methods=['GET'])
@login_required
def get_tasks():
    # Get query parameters for filtering
    status = request.args.get('status')
    priority = request.args.get('priority')
    assigned_to = request.args.get('assigned_to')
    lead_id = request.args.get('lead_id')
    
    # Start with base query
    query = Task.query
    
    # Apply filters if provided
    if status:
        query = query.filter(Task.status == status)
    if priority:
        query = query.filter(Task.priority == priority)
    if assigned_to:
        query = query.filter(Task.assigned_to == assigned_to)
    if lead_id:
        query = query.filter(Task.lead_id == lead_id)
    
    # Get tasks
    tasks = query.order_by(Task.due_date).all()
    
    # Convert to JSON
    result = []
    for task in tasks:
        result.append({
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'dueDate': task.due_date.isoformat() if task.due_date else None,
            'priority': task.priority,
            'status': task.status,
            'leadId': task.lead_id,
            'leadName': f"{task.lead.first_name} {task.lead.last_name}" if task.lead else None,
            'assignedTo': task.assignee.username if task.assignee else None,
            'createdBy': task.creator.username if task.creator else None,
            'createdAt': task.created_at.isoformat(),
            'updatedAt': task.updated_at.isoformat()
        })
    
    return jsonify(result)

@app.route('/api/tasks', methods=['POST'])
@login_required
def create_task():
    data = request.get_json()
    
    # Create new task
    task = Task(
        title=data['title'],
        description=data.get('description'),
        priority=data.get('priority', 'Medium'),
        status=data.get('status', 'Pending'),
        lead_id=data.get('leadId'),
        assigned_to=data.get('assignedTo'),
        created_by=current_user.id
    )
    
    if data.get('dueDate'):
        task.due_date = datetime.fromisoformat(data['dueDate'])
    
    db.session.add(task)
    db.session.commit()
    
    return jsonify({'success': True, 'id': task.id}), 201

@app.route('/api/tasks/<task_id>', methods=['PUT'])
@login_required
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    
    # Update task fields
    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'dueDate' in data and data['dueDate']:
        task.due_date = datetime.fromisoformat(data['dueDate'])
    if 'priority' in data:
        task.priority = data['priority']
    if 'status' in data:
        task.status = data['status']
    if 'leadId' in data:
        task.lead_id = data['leadId']
    if 'assignedTo' in data:
        task.assigned_to = data['assignedTo']
    
    db.session.commit()
    
    return jsonify({'success': True})

@app.route('/api/tasks/<task_id>', methods=['DELETE'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    
    db.session.delete(task)
    db.session.commit()
    
    return jsonify({'success': True})

# API routes for workflows
@app.route('/api/workflows', methods=['GET'])
@login_required
def get_workflows():
    workflows = Workflow.query.all()
    
    result = []
    for workflow in workflows:
        # Count executions
        total_executions = WorkflowExecution.query.filter_by(workflow_id=workflow.id).count()
        successful_executions = WorkflowExecution.query.filter_by(workflow_id=workflow.id, status='Completed').count()
        
        result.append({
            'id': workflow.id,
            'name': workflow.name,
            'description': workflow.description,
            'status': workflow.status,
            'createdBy': workflow.creator.username if workflow.creator else None,
            'createdAt': workflow.created_at.isoformat(),
            'updatedAt': workflow.updated_at.isoformat(),
            'executionStats': {
                'total': total_executions,
                'successful': successful_executions,
                'successRate': (successful_executions / total_executions * 100) if total_executions > 0 else 0
            }
        })
    
    return jsonify(result)

@app.route('/api/workflows', methods=['POST'])
@login_required
def create_workflow():
    data = request.get_json()
    
    # Create new workflow
    workflow = Workflow(
        name=data['name'],
        description=data.get('description'),
        status=data.get('status', 'Draft'),
        created_by=current_user.id
    )
    
    db.session.add(workflow)
    db.session.commit()
    
    # Add steps if provided
    if data.get('steps'):
        for i, step_data in enumerate(data['steps']):
            step = WorkflowStep(
                workflow_id=workflow.id,
                step_type=step_data['type'],
                step_config=json.dumps(step_data.get('config', {})),
                position=i
            )
            db.session.add(step)
        
        db.session.commit()
        
        # Update next_step_id for each step
        steps = WorkflowStep.query.filter_by(workflow_id=workflow.id).order_by(WorkflowStep.position).all()
        for i in range(len(steps) - 1):
            steps[i].next_step_id = steps[i + 1].id
        
        db.session.commit()
    
    return jsonify({'success': True, 'id': workflow.id}), 201

@app.route('/api/workflows/<workflow_id>', methods=['GET'])
@login_required
def get_workflow(workflow_id):
    workflow = Workflow.query.get_or_404(workflow_id)
    
    # Get steps
    steps = []
    for step in workflow.steps:
        steps.append({
            'id': step.id,
            'type': step.step_type,
            'config': json.loads(step.step_config) if step.step_config else {},
            'position': step.position,
            'nextStepId': step.next_step_id
        })
    
    # Get execution stats
    total_executions = WorkflowExecution.query.filter_by(workflow_id=workflow.id).count()
    successful_executions = WorkflowExecution.query.filter_by(workflow_id=workflow.id, status='Completed').count()
    
    result = {
        'id': workflow.id,
        'name': workflow.name,
        'description': workflow.description,
        'status': workflow.status,
        'steps': steps,
        'createdBy': workflow.creator.username if workflow.creator else None,
        'createdAt': workflow.created_at.isoformat(),
        'updatedAt': workflow.updated_at.isoformat(),
        'executionStats': {
            'total': total_executions,
            'successful': successful_executions,
            'successRate': (successful_executions / total_executions * 100) if total_executions > 0 else 0
        }
    }
    
    return jsonify(result)

@app.route('/api/workflows/<workflow_id>', methods=['PUT'])
@login_required
def update_workflow(workflow_id):
    workflow = Workflow.query.get_or_404(workflow_id)
    data = request.get_json()
    
    # Update workflow fields
    if 'name' in data:
        workflow.name = data['name']
    if 'description' in data:
        workflow.description = data['description']
    if 'status' in data:
        workflow.status = data['status']
    
    # Update steps if provided
    if 'steps' in data:
        # Remove existing steps
        WorkflowStep.query.filter_by(workflow_id=workflow.id).delete()
        
        # Add new steps
        for i, step_data in enumerate(data['steps']):
            step = WorkflowStep(
                workflow_id=workflow.id,
                step_type=step_data['type'],
                step_config=json.dumps(step_data.get('config', {})),
                position=i
            )
            db.session.add(step)
        
        db.session.commit()
        
        # Update next_step_id for each step
        steps = WorkflowStep.query.filter_by(workflow_id=workflow.id).order_by(WorkflowStep.position).all()
        for i in range(len(steps) - 1):
            steps[i].next_step_id = steps[i + 1].id
        
        db.session.commit()
    
    db.session.commit()
    
    return jsonify({'success': True})

@app.route('/api/workflows/<workflow_id>', methods=['DELETE'])
@login_required
def delete_workflow(workflow_id):
    workflow = Workflow.query.get_or_404(workflow_id)
    
    db.session.delete(workflow)
    db.session.commit()
    
    return jsonify({'success': True})

@app.route('/api/workflows/<workflow_id>/execute', methods=['POST'])
@login_required
def execute_workflow(workflow_id):
    workflow = Workflow.query.get_or_404(workflow_id)
    data = request.get_json()
    
    # Check if workflow is active
    if workflow.status != 'Active':
        return jsonify({'success': False, 'message': 'Workflow is not active'}), 400
    
    # Create execution record
    execution = WorkflowExecution(
        workflow_id=workflow.id,
        lead_id=data.get('leadId'),
        status='Running'
    )
    
    db.session.add(execution)
    db.session.commit()
    
    # In a real application, you would start the workflow execution in a background task
    # For this example, we'll just mark it as completed
    execution.status = 'Completed'
    execution.completed_at = datetime.utcnow()
    execution.result = json.dumps({'message': 'Workflow executed successfully'})
    
    db.session.commit()
    
    return jsonify({'success': True, 'executionId': execution.id})

# API routes for analytics
@app.route('/api/analytics/lead_sources', methods=['GET'])
@login_required
def lead_sources_analytics():
    # Get lead counts by source
    sources = db.session.query(Lead.source, db.func.count(Lead.id)).group_by(Lead.source).all()
    
    result = [{'source': source, 'count': count} for source, count in sources]
    
    return jsonify(result)

@app.route('/api/analytics/lead_statuses', methods=['GET'])
@login_required
def lead_statuses_analytics():
    # Get lead counts by status
    statuses = db.session.query(Lead.status, db.func.count(Lead.id)).group_by(Lead.status).all()
    
    result = [{'status': status, 'count': count} for status, count in statuses]
    
    return jsonify(result)

@app.route('/api/analytics/lead_scores', methods=['GET'])
@login_required
def lead_scores_analytics():
    # Get average lead score
    avg_score = db.session.query(db.func.avg(Lead.score)).scalar()
    
    # Get lead score distribution
    score_ranges = [
        {'min': 0, 'max': 20, 'label': '0-20'},
        {'min': 21, 'max': 40, 'label': '21-40'},
        {'min': 41, 'max': 60, 'label': '41-60'},
        {'min': 61, 'max': 80, 'label': '61-80'},
        {'min': 81, 'max': 100, 'label': '81-100'}
    ]
    
    distribution = []
    for range_data in score_ranges:
        count = Lead.query.filter(Lead.score >= range_data['min'], Lead.score <= range_data['max']).count()
        distribution.append({
            'range': range_data['label'],
            'count': count
        })
    
    result = {
        'averageScore': float(avg_score) if avg_score else 0,
        'distribution': distribution
    }
    
    return jsonify(result)

@app.route('/api/analytics/conversion_rates', methods=['GET'])
@login_required
def conversion_rates_analytics():
    # Calculate conversion rates between stages
    stages = ['New', 'Contacted', 'Qualified', 'Proposal', 'Negotiation', 'Closed Won', 'Closed Lost']
    
    stage_counts = {}
    for stage in stages:
        stage_counts[stage] = Lead.query.filter_by(status=stage).count()
    
    conversion_rates = []
    for i in range(len(stages) - 1):
        if stage_counts[stages[i]] > 0:
            rate = (stage_counts[stages[i+1]] / stage_counts[stages[i]]) * 100
        else:
            rate = 0
        
        conversion_rates.append({
            'fromStage': stages[i],
            'toStage': stages[i+1],
            'rate': rate
        })
    
    return jsonify(conversion_rates)

@app.route('/api/analytics/activity_timeline', methods=['GET'])
@login_required
def activity_timeline_analytics():
    # Get activity counts by day for the last 30 days
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    
    activities = db.session.query(
        db.func.date(Activity.created_at),
        db.func.count(Activity.id)
    ).filter(Activity.created_at >= thirty_days_ago).group_by(db.func.date(Activity.created_at)).all()
    
    result = [{'date': date.isoformat(), 'count': count} for date, count in activities]
    
    return jsonify(result)

# Run the app
if __name__ == '__main__':
    # Create database tables
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)

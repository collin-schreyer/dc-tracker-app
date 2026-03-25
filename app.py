from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from models import Project, Company, get_session, init_db
from sqlalchemy import or_, and_
import os
from dotenv import load_dotenv

load_dotenv()

# --- Serverless SQLite Bridge (Vercel Fix) ---
# Vercel wipes the /tmp/ directory constantly. If the DB is missing, auto-seed it on cold boot.
db_url = os.getenv('DATABASE_URL', '')
if db_url.startswith('sqlite:////tmp/'):
    tmp_path = db_url.replace('sqlite:///', '')
    if not os.path.exists(tmp_path):
        from seed_data import seed_database
        # seed_database() internally calls init_db() and commits the 40 projects
        seed_database()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key')
CORS(app)

init_db()

@app.route('/')
def index():
    return render_template('index.html', mapbox_token=os.getenv('MAPBOX_TOKEN', ''))

@app.route('/api/projects')
def get_projects():
    session = get_session()
    
    status = request.args.get('status')
    state = request.args.get('state')
    min_mw = request.args.get('min_mw', type=float)
    open_slots = request.args.get('open_slots') == 'true'
    
    query = session.query(Project)
    
    if status:
        query = query.filter(Project.status == status)
    if state:
        query = query.filter(Project.state == state)
    if min_mw:
        query = query.filter(Project.est_mw >= min_mw)
    if open_slots:
        query = query.filter(or_(
            Project.epc == None,
            Project.electrical_contractor == None,
            Project.line_builder == None
        ))
    
    projects = query.all()
    
    result = []
    for p in projects:
        result.append({
            'id': p.id,
            'project_id': p.project_id,
            'name': p.name,
            'address': p.address,
            'city': p.city,
            'county': p.county,
            'state': p.state,
            'lat': p.lat,
            'lon': p.lon,
            'status': p.status,
            'est_mw': p.est_mw,
            'go_live_est': p.go_live_est,
            'owner': p.owner,
            'developer': p.developer,
            'customer': p.customer,
            'utility': p.utility,
            'epc': p.epc,
            'electrical_contractor': p.electrical_contractor,
            'line_builder': p.line_builder,
            'sources': p.sources,
            'has_open_slots': not all([p.epc, p.electrical_contractor, p.line_builder])
        })
    
    session.close()
    return jsonify(result)

@app.route('/api/stats')
def get_stats():
    session = get_session()
    
    total = session.query(Project).count()
    by_status = {}
    for status in ['Rumored', 'Permitting', 'Approved', 'Under Construction', 'Live']:
        count = session.query(Project).filter(Project.status == status).count()
        by_status[status] = count
    
    total_mw = session.query(Project).filter(Project.est_mw != None).all()
    total_capacity = sum([p.est_mw for p in total_mw if p.est_mw])
    
    open_opportunities = session.query(Project).filter(or_(
        Project.epc == None,
        Project.electrical_contractor == None,
        Project.line_builder == None
    )).count()
    
    session.close()
    
    return jsonify({
        'total_projects': total,
        'by_status': by_status,
        'total_capacity_mw': total_capacity,
        'open_opportunities': open_opportunities
    })

@app.route('/api/companies')
def get_companies():
    session = get_session()
    
    role = request.args.get('role')
    
    query = session.query(Company)
    if role:
        query = query.filter(Company.role.contains(role))
    
    companies = query.order_by(Company.name).all()
    
    result = []
    for c in companies:
        # Count projects this company is involved in
        project_count = session.query(Project).filter(
            or_(
                Project.owner == c.name,
                Project.developer == c.name,
                Project.epc == c.name,
                Project.electrical_contractor == c.name,
                Project.line_builder == c.name,
                Project.utility == c.name,
                Project.customer == c.name
            )
        ).count()
        
        result.append({
            'id': c.id,
            'name': c.name,
            'role': c.role,
            'website': c.website,
            'contact': c.contact,
            'project_count': project_count
        })
    
    session.close()
    return jsonify(result)

@app.route('/api/utilities')
def get_utilities():
    session = get_session()
    
    # Get all utilities and their projects
    utilities = {}
    projects = session.query(Project).filter(Project.utility != None).all()
    
    for p in projects:
        if p.utility not in utilities:
            utilities[p.utility] = {
                'name': p.utility,
                'projects': [],
                'total_mw': 0,
                'states': set()
            }
        utilities[p.utility]['projects'].append({
            'name': p.name,
            'state': p.state,
            'mw': p.est_mw or 0,
            'status': p.status
        })
        utilities[p.utility]['total_mw'] += p.est_mw or 0
        utilities[p.utility]['states'].add(p.state)
    
    result = []
    for util in utilities.values():
        util['states'] = list(util['states'])
        util['project_count'] = len(util['projects'])
        util['equipment_value'] = util['total_mw'] * 2500  # $2.5K per MW estimate
        result.append(util)
    
    result.sort(key=lambda x: x['total_mw'], reverse=True)
    
    session.close()
    return jsonify(result)

@app.route('/api/analytics')
def get_analytics():
    session = get_session()
    
    # Status breakdown
    status_data = []
    for status in ['Rumored', 'Permitting', 'Approved', 'Under Construction', 'Live']:
        projects = session.query(Project).filter(Project.status == status).all()
        mw = sum([p.est_mw for p in projects if p.est_mw])
        status_data.append({'status': status, 'count': len(projects), 'mw': mw})
    
    # State breakdown (top 10)
    state_data = {}
    projects = session.query(Project).all()
    for p in projects:
        if p.state not in state_data:
            state_data[p.state] = {'count': 0, 'mw': 0}
        state_data[p.state]['count'] += 1
        state_data[p.state]['mw'] += p.est_mw or 0
    
    state_list = [{'state': k, 'count': v['count'], 'mw': v['mw']} for k, v in state_data.items()]
    state_list.sort(key=lambda x: x['mw'], reverse=True)
    
    # Top owners
    owner_data = {}
    for p in projects:
        if p.owner:
            if p.owner not in owner_data:
                owner_data[p.owner] = {'count': 0, 'mw': 0}
            owner_data[p.owner]['count'] += 1
            owner_data[p.owner]['mw'] += p.est_mw or 0
    
    owner_list = [{'name': k, 'count': v['count'], 'mw': v['mw']} for k, v in owner_data.items()]
    owner_list.sort(key=lambda x: x['mw'], reverse=True)
    
    # Open opportunities
    open_projects = session.query(Project).filter(
        or_(
            Project.epc == None,
            Project.electrical_contractor == None,
            Project.line_builder == None
        )
    ).all()
    
    open_mw = sum([p.est_mw for p in open_projects if p.est_mw])
    
    session.close()
    
    return jsonify({
        'status_breakdown': status_data,
        'state_breakdown': state_list[:10],
        'top_owners': owner_list[:10],
        'open_opportunities': {
            'count': len(open_projects),
            'mw': open_mw,
            'value': open_mw * 2500
        }
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001)

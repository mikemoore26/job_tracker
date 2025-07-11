from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db , job, User
from functools import wraps
import os

#DECORATORS
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('You need to log in first!', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

app = Flask(__name__)
app.secret_key = "mike371326moore888809"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
@login_required
def index():
    # if 'user_id' not in session:
    #     flash('You need to log in first!', 'warning')
    #     return redirect(url_for('login'))
    
    search_query = request.args.get('search')
    status = request.args.get('status')

    query = job.query.filter_by(user_id=session['user_id'])

    if search_query:
        query = query.filter(
            (job.company.ilike(f'%{search_query}%')) |
            (job.title.ilike(f'%{search_query}%')) 
        )

    if status:
        query = query.filter_by(status=status)

    jobs = job.query.all()
    return render_template('index.html', jobs=jobs)

@app.route("/dashboard")
@login_required
def dashboard():
    uid = session["user_id"]


    total_jobs = job.query.filter_by(user_id=uid).count()
    applied_jobs = job.query.filter_by(user_id=uid, status='Applied').count()
    interviewing = job.query.filter_by(user_id=uid, status='Interviewing').count()
    offer_received = job.query.filter_by(user_id=uid, status='Offer Received').count()
    rejected = job.query.filter_by(user_id=uid, status='Rejected').count()

    return render_template('dashboard.html',
                           total_jobs=total_jobs,
                           applied_jobs=applied_jobs,
                           interviewing=interviewing,
                           offer_received=offer_received,
                           rejected=rejected)



@app.route("/add", methods=["GET", "POST"])
@login_required
def add_job():
    
    if request.method == "POST":
        company = request.form.get("company")
        title = request.form.get("title")
        location = request.form.get("location")
        status = request.form.get("status")
        notes = request.form.get("notes")

        new_job = job(company=company, title=title, location=location, status=status, notes=notes)
        db.session.add(new_job)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('add_job.html')


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'danger')
            return redirect(url_for('register'))
        user = User(username=username)
        user.set_password(password) 
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        flash('Invalid username or password', 'danger')
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route("/logout")
@login_required
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route("/delete/<int:job_id>", methods=["POST"])
@login_required
def delete_job(job_id):
     
    job_to_delete = job.query.get_or_404(job_id)
    db.session.delete(job_to_delete)
    db.session.commit()
    return redirect(url_for('index'))

@app.route("/edit/<int:job_id>", methods=["GET", "POST"])
@login_required
def edit_job(job_id):
    
    job = job.query.get_or_404(job_id)
    if request.method == "POST":
        job.company = request.form['company']
        job.title = request.form["title"]
        job.location = request.form['location']
        job.status = request.form['status']
        job.notes = request.form['notes']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_job.html', job=job)

if __name__ == '__main__':
    app.run(debug=True)
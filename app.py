from flask import Flask, render_template, request, redirect, url_for
from models import db , job

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    jobs = job.query.all()
    return render_template('index.html', jobs=jobs)

@app.route("/add", methods=["GET", "POST"])
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

@app.route("/delete/<int:job_id>", methods=["POST"])
def delete_job(job_id):
    job_to_delete = job.query.get_or_404(job_id)
    db.session.delete(job_to_delete)
    db.session.commit()
    return redirect(url_for('index'))

@app.route("/edit/<int:job_id>", methods=["GET", "POST"])
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
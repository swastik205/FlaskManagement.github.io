from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()


class Entry(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    roll = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self) -> str:
        return f"{self.sno} - {self.name}"      # displays in this formal


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        name = request.form['name']
        roll = request.form['roll']
        email = request.form['email']
        entry = Entry(name=name, roll=roll, email=email)
        db.session.add(entry)
        db.session.commit()
    allEntries = Entry.query.all()            # to display in terminal
    return render_template('hello.html', allEntries=allEntries)

@app.route('/delete/<int:sno>')         # to specify that an integer of name sno will be passed in the route
def delete(sno):
    entry_del = Entry.query.filter_by(sno=sno).first()          # to give the variable infos about the current entry
    db.session.delete(entry_del)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        name = request.form['name']
        roll = request.form['roll']
        email = request.form['email']
        entry = Entry.query.filter_by(sno=sno).first()
        entry.name = name
        entry.roll = roll
        entry.email = email
        db.session.add(entry)
        db.session.commit()
        return redirect('/')

    entry_update = Entry.query.filter_by(sno=sno).first()
    return render_template('update.html', entry=entry_update)

@app.route('/about')         # to specify that an integer of name sno will be passed in the route
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True, port=8000)
import os
from flask import Flask, render_template, request, redirect, url_for, session
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Initialize Firebase credentials
cred = credentials.Certificate(
    "fitnessapp-88ffa-firebase-adminsdk-m6ket-54330c1b3d.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://fitnessapp-88ffa-default-rtdb.firebaseio.com'
})

# Route for profile form


@app.route('/')
def profile_form():
    return render_template('profile_form.html')

# Route to handle profile form submission and redirect to profile display


@app.route('/save-profile', methods=['POST'])
def save_profile():
    # Get form data
    name = request.form['name']
    age = request.form['age']
    gender = request.form['gender']
    height = request.form['height']
    weight = request.form['weight']
    bmi = request.form['bmi']
    medication = request.form['medication']
    history = request.form['history']
    fitnessGoal = request.form['fitnessGoal']

    # Save profile data to Firebase
    ref = db.reference('profiles')
    new_profile = ref.push()
    new_profile.set({
        'name': name,
        'age': age,
        'gender': gender,
        'height': height,
        'weight': weight,
        'bmi': bmi,
        'medication': medication,
        'history': history,
        'fitnessGoal': fitnessGoal
    })

    profile_id = new_profile.key

    # Store profile ID in session
    session['profile_id'] = profile_id

    # Redirect to profile display page
    return redirect(url_for('profile_display'))

# Route for profile display and editing


@app.route('/profile', methods=['GET', 'POST'])
def profile_display():
    profile_id = session.get('profile_id')

    if not profile_id:
        # Redirect to profile form if profile ID is not stored in session
        return redirect(url_for('profile_form'))

    ref = db.reference('profiles')
    profile = ref.child(profile_id).get()

    if request.method == 'POST':
        if 'update_profile' in request.form:
            name = request.form['name']
            age = request.form['age']
            gender = request.form['gender']
            height = request.form['height']
            weight = request.form['weight']
            bmi = request.form['bmi']
            medication = request.form['medication']
            history = request.form['history']
            fitnessGoal = request.form['fitnessGoal']

            ref.child(profile_id).update({
                'name': name,
                'age': age,
                'gender': gender,
                'height': height,
                'weight': weight,
                'bmi': bmi,
                'medication': medication,
                'history': history,
                'fitnessGoal': fitnessGoal
            })
        elif 'sign_out' in request.form:
            # Clear profile ID from session
            session.pop('profile_id', None)

            # Redirect to profile form
            return redirect(url_for('profile_form'))

    return render_template('profile_display.html', profile=profile, profile_id=profile_id)


@app.route('/sign_out')
def sign_out():
    # Clear profile ID from session
    session.pop('profile_id', None)

    # Redirect to profile form
    return redirect(url_for('profile_form'))


if __name__ == '__main__':
    app.run(debug=True)

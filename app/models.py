from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from flask import current_app

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    forms = db.relationship('Form', backref='author', lazy='dynamic')
    follow_ups = db.relationship('FollowUp', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class FollowUp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    patient_name = db.Column(db.String(140))
    overall_problem = db.Column(db.String(10000))
    #headaches
    headaches = db.Column(db.String(20))
    headaches_frequency = db.Column(db.String(1000))
    headaches_length = db.Column(db.String(1000))
    headaches_spots = db.Column(db.String(20))
    headaches_flashes = db.Column(db.String(20))
    headaches_medication = db.Column(db.String(1000))
    dizziness = db.Column(db.String(20))
    unsteady_gait = db.Column(db.String(20))
    neck_pain = db.Column(db.String(20))
    neck_pain_shoulders = db.Column(db.String(20))
    neck_pain_arms = db.Column(db.String(20))
    back_pain = db.Column(db.String(20))
    back_pain_hips = db.Column(db.String(20))
    back_pain_legs = db.Column(db.String(20))
    back_pain_right_side = db.Column(db.String(20))
    back_pain_left_side = db.Column(db.String(20))
    arm_pain = db.Column(db.String(20))
    arm_pain_right_side = db.Column(db.String(20))
    arm_pain_left_side = db.Column(db.String(20))
    leg_pain = db.Column(db.String(20))
    leg_pain_right_side = db.Column(db.String(20))
    leg_pain_left_side = db.Column(db.String(20))
    fingers = db.Column(db.String(20))
    hands = db.Column(db.String(20))
    feet = db.Column(db.String(20))
    legs = db.Column(db.String(20))
    numbness_right_side = db.Column(db.String(20))
    numbness_left_side = db.Column(db.String(20))
    fainting = db.Column(db.String(20))
    fainting_frequency = db.Column(db.String(1000))
    fainting_length = db.Column(db.String(1000))
    seizure = db.Column(db.String(20))
    seizure_frequency = db.Column(db.String(1000))
    seizure_length = db.Column(db.String(1000))
    seizure_medication = db.Column(db.String(1000))
    limb_jerking = db.Column(db.String(20))
    tremors = db.Column(db.String(20))
    tremors_hands = db.Column(db.String(20))
    tremors_legs = db.Column(db.String(20))
    tremors_positions = db.Column(db.String(1000))
    sleep_difficulties = db.Column(db.String(20))
    increased_stress = db.Column(db.String(20))
    episodes_of_confusion = db.Column(db.String(20))
    episodes_of_confusion_optional = db.Column(db.String(1000))
    memory_problems = db.Column(db.String(20))
    hospital_recently = db.Column(db.String(20))
    hospital_recently_optional = db.Column(db.String(1000))
    medication_change = db.Column(db.String(20))
    medication_change_optional = db.Column(db.String(1000))

    def __repr__(self):
        return '<Follow up {}>'.format(self.patient_name)

class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    patient_name = db.Column(db.String(140))
    sex = db.Column(db.String(20))
    #date_of_birth = db.Column(db.Date)
    date_of_birth = db.Column(db.String(20))
    age = db.Column(db.Integer)
    height = db.Column(db.String(20))
    weight = db.Column(db.Integer)
    hand = db.Column(db.String(10))
    referred_by = db.Column(db.String(1000))
    reason_for_visit = db.Column(db.String(100000))
    #symptoms
    limb_jerking = db.Column(db.String(20))
    tremors = db.Column(db.String(20))
    depression = db.Column(db.String(20))
    headaches = db.Column(db.String(20))
    sleep_difficulties = db.Column(db.String(20))
    increased_stress = db.Column(db.String(20))
    memory_problems = db.Column(db.String(20))
    back_neck_pain = db.Column(db.String(20))
    numbness = db.Column(db.String(20))
    numbness_optional = db.Column(db.String(20))
    head_injury = db.Column(db.String(20))
    dizziness = db.Column(db.String(20))
    unsteady_gait = db.Column(db.String(20))
    balance_difficulties = db.Column(db.String(20))
    fainting = db.Column(db.String(20))
    word_finding = db.Column(db.String(20))
    episodes_of_confusion = db.Column(db.String(20))
    hospital_recently= db.Column(db.String(20))
    medication_change = db.Column(db.String(20))
    other_symptoms = db.Column(db.String(10000))
    #conditions
    hypertension = db.Column(db.String(20))
    heart_problems = db.Column(db.String(20))
    diabetes_mellitus = db.Column(db.String(20))
    high_cholesterol = db.Column(db.String(20))
    stroke = db.Column(db.String(20))
    seizure = db.Column(db.String(20))
    depression_disease = db.Column(db.String(20))
    migraine = db.Column(db.String(20))
    #habits
    cigarettes = db.Column(db.String(20))
    cigarettes_long = db.Column(db.String(1000))
    cigarettes_frequency = db.Column(db.String(1000))
    alcohol = db.Column(db.String(20))
    drugs = db.Column(db.String(20))
    #begin medical systems
    #constitutional
    weight_loss = db.Column(db.String(20))
    fever = db.Column(db.String(20))
    #cardiovascular
    palpitation = db.Column(db.String(20))
    chest_pain = db.Column(db.String(20))
    #pulmonary
    cough = db.Column(db.String(20))
    sputum = db.Column(db.String(20))
    #gastrointestinal
    abdominal_pain = db.Column(db.String(20))
    nausea = db.Column(db.String(20))
    vomiting = db.Column(db.String(20))
    diarrhea = db.Column(db.String(20))
    #genital urinary
    hematuria = db.Column(db.String(20))
    urination_incontinence = db.Column(db.String(25))
    #endocrinological
    over_eating = db.Column(db.String(20))
    over_urinating = db.Column(db.String(20))
    over_sweating = db.Column(db.String(20))
    always_thirsty = db.Column(db.String(20))
    #dermatological
    skin_rash = db.Column(db.String(20))
    lesion = db.Column(db.String(20))
    #hematological
    easily_bleeds = db.Column(db.String(20))
    bruises = db.Column(db.String(20))
    blood_clots = db.Column(db.String(20))
    #skeletal musculary
    joint_pain = db.Column(db.String(20))
    muscle_pain = db.Column(db.String(20))
    #extra
    elaborate = db.Column(db.String(10000))
    #misc
    occupation = db.Column(db.String(1000))
    surgeries = db.Column(db.String(10000))
    medication_allergies = db.Column(db.String(10000))
    family_medical_problems = db.Column(db.String(10000))
    current_medications = db.Column(db.String(10000))
    other_information = db.Column(db.String(10000))
    patient_signature = db.Column(db.String(140))

    def __repr__(self):
        return '<Form {}>'.format(self.patient_name)

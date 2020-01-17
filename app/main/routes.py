from flask import render_template, flash, redirect, url_for, current_app
from app import db, basic_auth
from app.main import bp
from app.main.forms import MedicalForm, FollowUpForm
from flask_login import current_user, login_user
from app.models import User, Form, FollowUp
from flask_login import logout_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse

@bp.route('/', methods = ['GET', 'POST'])
@bp.route('/index', methods = ['GET', 'POST'])
@login_required
def index():
    f = MedicalForm()
    if f.validate_on_submit():
        submit = Form(patient_name=f.patient_name.data, sex = f.sex.data, date_of_birth=f.date_of_birth.data,
                    age=f.age.data, height=f.height.data, weight = f.weight.data, hand = f.hand.data,
                    referred_by=f.referred_by.data, reason_for_visit=f.reason_for_visit.data,
                    #symptoms
                    limb_jerking=f.limb_jerking.data, tremors=f.tremors.data, depression=f.depression.data,
                    headaches=f.headaches.data, sleep_difficulties=f.sleep_difficulties.data,
                    increased_stress=f.increased_stress.data, memory_problems=f.memory_problems.data, back_neck_pain=f.back_neck_pain.data,
                    numbness=f.numbness.data, numbness_optional=f.numbness_optional.data, head_injury=f.head_injury.data,
                    dizziness=f.dizziness.data, unsteady_gait=f.unsteady_gait.data, balance_difficulties=f.balance_difficulties.data,
                    fainting=f.fainting.data, word_finding=f.word_finding.data, episodes_of_confusion=f.episodes_of_confusion.data,
                    hospital_recently=f.hospital_recently.data, medication_change=f.medication_change.data, other_symptoms=f.other_symptoms.data,
                    #diseases
                    hypertension=f.hypertension.data, heart_problems=f.heart_problems.data, diabetes_mellitus=f.diabetes_mellitus.data,
                    high_cholesterol=f.high_cholesterol.data, stroke=f.stroke.data, seizure=f.seizure.data,
                    depression_disease=f.depression_disease.data, migraine=f.migraine.data,
                    #habits
                    cigarettes=f.cigarettes.data, cigarettes_long=f.cigarettes_long.data, cigarettes_frequency=f.cigarettes_frequency.data,
                    alcohol=f.alcohol.data, drugs=f.drugs.data,
                    #medical systems
                    weight_loss=f.weight_loss.data, fever=f.fever.data, palpitation=f.palpitation.data, chest_pain=f.chest_pain.data,
                    cough=f.cough.data, sputum=f.sputum.data, abdominal_pain=f.abdominal_pain.data, nausea=f.nausea.data, vomiting=f.vomiting.data,
                    diarrhea=f.diarrhea.data, hematuria=f.hematuria.data, urination_incontinence=f.urination_incontinence.data, over_eating=f.over_eating.data,
                    over_sweating=f.over_sweating.data, over_urinating=f.over_urinating.data, always_thirsty=f.always_thirsty.data, skin_rash=f.skin_rash.data,
                    lesion=f.lesion.data, easily_bleeds=f.easily_bleeds.data, bruises=f.bruises.data, blood_clots=f.blood_clots.data,
                    joint_pain=f.joint_pain.data, muscle_pain=f.muscle_pain.data,
                    #misc
                    occupation=f.occupation.data, surgeries=f.surgeries.data, medication_allergies=f.medication_allergies.data,
                    family_medical_problems=f.family_medical_problems.data, current_medications=f.current_medications.data,
                    other_information=f.other_information.data, patient_signature=f.patient_signature.data,
                    author=current_user)
        db.session.add(submit)
        db.session.commit()
        flash('Thank you for registering! Please return IPad to front desk.')
        return redirect(url_for('main.index'))
    return render_template('index.html', title='Patient Registration', form=f)

@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    forms = user.forms[::-1]
    return render_template('user.html', user=user, forms=forms)

@bp.route('/followup', methods = ['GET', 'POST'])
@login_required
def followup():
    f = FollowUpForm()
    if f.validate_on_submit():
        submit = FollowUp(patient_name=f.patient_name.data, overall_problem=f.overall_problem.data, headaches=f.headaches.data,
                           headaches_frequency=f.headaches_frequency.data, headaches_length=f.headaches_length.data,
                           headaches_spots=f.headaches_spots.data, headaches_flashes=f.headaches_flashes.data, headaches_medication=f.headaches_medication.data,
                           dizziness=f.dizziness.data, unsteady_gait=f.unsteady_gait.data, neck_pain=f.neck_pain.data,
                           neck_pain_shoulders=f.neck_pain_shoulders.data, neck_pain_arms=f.neck_pain_arms.data, back_pain=f.back_pain.data,
                           back_pain_hips=f.back_pain_hips.data, back_pain_legs=f.back_pain_legs.data, back_pain_right_side=f.back_pain_right_side.data,
                           back_pain_left_side=f.back_pain_left_side.data, arm_pain=f.arm_pain.data, arm_pain_right_side=f.arm_pain_right_side.data,
                           arm_pain_left_side=f.arm_pain_left_side.data, leg_pain=f.leg_pain.data, leg_pain_right_side=f.leg_pain_right_side.data,
                           leg_pain_left_side=f.leg_pain_left_side.data, fingers=f.fingers.data, hands=f.hands.data, feet=f.feet.data, legs=f.legs.data,
                           numbness_right_side=f.numbness_right_side.data, numbness_left_side=f.numbness_left_side.data, fainting=f.fainting.data,
                           fainting_frequency=f.fainting_frequency.data, fainting_length=f.fainting_length.data, seizure=f.seizure.data,
                           seizure_frequency=f.seizure_frequency.data, seizure_length=f.seizure_length.data, seizure_medication=f.seizure_medication.data,
                           limb_jerking=f.limb_jerking.data, tremors=f.tremors.data, tremors_hands=f.tremors_hands.data,
                           tremors_legs=f.tremors_legs.data, tremors_positions=f.tremors_positions.data, sleep_difficulties=f.sleep_difficulties.data,
                           increased_stress=f.increased_stress.data, episodes_of_confusion=f.episodes_of_confusion.data,
                           episodes_of_confusion_optional=f.episodes_of_confusion_optional.data, memory_problems=f.memory_problems.data,
                           hospital_recently=f.hospital_recently.data, hospital_recently_optional=f.hospital_recently_optional.data,
                           medication_change=f.medication_change.data, medication_change_optional=f.medication_change_optional.data,
                           author=current_user)
        db.session.add(submit)
        db.session.commit()
        flash('Thank you for following up! Please return IPad to front desk.')
        return redirect(url_for('main.index'))
    return render_template('followup.html', title='Follow Up Form', form=f)

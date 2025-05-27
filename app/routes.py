from flask import Blueprint, render_template, request, session, redirect, url_for,flash
from app.models.intent_recognition import predict_intent
from app.models.dialogue_manager import DialogueManager
from app.models.appointment import create_appointment
bp = Blueprint('main', __name__)
dm = DialogueManager()

@bp.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        user_input = request.form.get('question', '')
        intent = predict_intent(user_input)
        # 终端打印用户意图
        print(f"用户输入: {user_input}，意图: {intent}")
        
        if intent == '挂号':
            return redirect(url_for('main.register'))

        # 问候意图也交给DialogueManager处理，实现多轮对话
        result = dm.update(user_input, intent)
        session['dialogue_history'] = dm.get_history()

    dialog_history = session.get('dialogue_history', [])
    return render_template('index.html', result=result, dialog_history=dialog_history)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        doctor_name = request.form.get('doctor_name')
        department = request.form.get('department')
        appointment_time = request.form.get('appointment_time')

        print(f"doctor_name: {doctor_name}, department: {department}, appointment_time: {appointment_time}")

        if not doctor_name or not department or not appointment_time:
            flash('请完整填写所有信息！', 'error')
            return redirect(url_for('main.register'))

        create_appointment(department, doctor_name, appointment_time)
        flash('预约成功！', 'success')
        return redirect(url_for('main.success'))

    return render_template('register.html')

@bp.route('/success')
def success():
    return render_template('success.html')
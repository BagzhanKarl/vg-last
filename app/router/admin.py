from flask import Blueprint, render_template, jsonify, request
import os
from app.db import Avatar, User, Messages, UserLog
from app.service import AssemAI

api_key = os.getenv('OPENAI_API_KEY')
assistant_id = os.getenv('OPENAI_ASSISTANT_ID')

admin = Blueprint('admin', __name__, url_prefix='/admin')

def format_phone_number(phone):
    if len(phone) == 11 and phone.isdigit():
        return f"+7 ({phone[1:4]}) {phone[4:7]}-{phone[7:9]}-{phone[9:11]}"
    else:
        return "Неверный номер телефона"

@admin.route('/')
def admin_index():
    return render_template('base.html')

@admin.route('/users')
def admin_users():
    users = User.query.all()
    response = []
    for user in users:
        response.append(
            {
                'id': user.id,
                'name': user.name,
                'phone': format_phone_number(user.phone),
            }
        )
    return render_template('users.html', response=response)

@admin.route('/users/<int:id>/chat')
def admin_users_chat(id):
    user = User.query.get(id)
    messages = Messages.query.filter_by(user_id=user.id).all()
    user = {
        "name": user.name,
        "phone": format_phone_number(user.phone),
    }
    return render_template(
        'chat-detail.html',
        user=user,
        messages=messages,
    )

@admin.route('/avatar')
def admin_avatar():
    active_avatar = Avatar.query.filter_by(is_active=True).first()
    return render_template('avatar.html', avatar=active_avatar)

@admin.route('/avatar/edit', methods=['POST'])
def admin_avatar_edit():
    # Получаем все данные из формы как MultiDict (стандартный тип для request.form)
    avatar_name = request.form.get('avatar_name')
    role_or_position = request.form.get('avatarRole')
    first_message = request.form.get('first_message')
    behavior = request.form.get('behavior')
    additional = request.form.get('additional')
    lang = request.form.get('lang')  # Для массива значений (например, языков)

    temp = request.form.get('temp')
    try:
        temp = float(temp)
    except (ValueError, TypeError):
        temp = 1.0  # или любое другое значение по умолчанию


    new_avatar_settings = Avatar(
        name=avatar_name,
        additional_info=additional,
        lang=lang,
        temp=temp,
        how_to_behave=behavior,
        first_message=first_message,
        is_active=True,
        role=role_or_position,
    )

    new_avatar_settings.save_to_db()

    response = (
        f'Привет! Тебя зовут: {new_avatar_settings.name}! Вы: {new_avatar_settings.role_or_position}! Вы должны вести себя: {new_avatar_settings.how_to_behave}, '
        f'Говорите на "{new_avatar_settings.lang}", от зависимости пользователя. У вас есть документ который иногда можете искать информацию, чтобы дать точный ответ для пользователя. Документ называется "Стандарт по Бережливому Производству", '
        f'где написано все подробнее для сотрудников компаний. Советуем посмотреть информацию от туда. '
        f'Но все же дополнительное информация если на документе не найдется: {new_avatar_settings.additional_info}')

    assistant = AssemAI(
        api_key=api_key,
        assistant_id=assistant_id,
    )

    assistant.update_assistant_instructions(new_instructions=response, temp=new_avatar_settings.temp)
    return jsonify({
        'avatar_name': avatar_name,
        'first_message': first_message,
        'behavior': behavior,
        'additional': additional,
        'temp': temp,
        'lang': lang,
    })

@admin.route('/avatar/check', methods=['GET'])
def admin_avatar_check():
    avatar = Avatar.query.filter_by(is_active=True).first()
    response = (f'Привет! Тебя зовут: {avatar.name}! Вы: {avatar.role_or_position}! Вы должны вести себя: {avatar.how_to_behave}, '
                f'Говорите на "{avatar.lang}", от зависимости пользователя. У вас есть документ который иногда можете искать информацию, чтобы дать точный ответ для пользователя. Документ называется "Стандарт по Бережливому Производству", '
                f'где написано все подробнее для сотрудников компаний. Советуем посмотреть информацию от туда. '
                f'Но все же дополнительное информация если на документе не найдется: {avatar.additional_info}')


    return jsonify({"response": response})

@admin.route('/key/check')
def admin_key_check():
    return jsonify({"api_key": assistant_id})


@admin.route('/users/<int:id>/logs')
def admin_users_logs(id):
    user = User.query.get(id)
    logs = UserLog.query.filter_by(user_id=id).order_by(UserLog.created_at.desc()).all()

    return render_template(
        'logs.html',
        user=user,
        logs=logs
    )
from flask import render_template, session, Flask, request, redirect, jsonify
import pymysql
pymysql.install_as_MySQLdb()
from flask_mysqldb import MySQL
from flask_socketio import SocketIO, emit
from datetime import datetime
import bcrypt
import os
import secrets
import string

app = Flask(__name__)

app.secret_key = 'secret'
app.config['MYSQL_DB'] = 'messager'
app.config['MYSQL_PASSWORD'] = '2005'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

def generate_chat_id(length : int = 16):
    """
    leinght: Длина генерируемого ключа, по умолчанию 16
    """
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

@app.route('/registration', methods=['POST'])
def reg():
    username = request.form.get('login')
    password = request.form.get('password')
    
    if not username or not password:
        return redirect('/')
    
    # Хешируем пароль
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    
    cursor = mysql.connection.cursor()
    try:
        cursor.execute('INSERT INTO users (username, password, chats) VALUES (%s, %s, 1)', 
                      (username, hashed.decode('utf-8')))
        mysql.connection.commit()
        session['user'] = username
    except Exception as e:
        print(f"Ошибка регистрации: {e}")
        return redirect('/')
    finally:
        cursor.close()
    
    return redirect('/main_page')

@app.route('/auth', methods=['POST'])
def auth():
    username = request.form.get('login')
    password = request.form.get('password')
    
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
    user = cursor.fetchone()
    cursor.close()
    
    if user and bcrypt.checkpw(password.encode(), user['password'].encode()):
        session['user'] = username
        return redirect('/main_page')
    else:
        return redirect('/')

@app.route('/main_page')
def main():
    if 'user' not in session:
        return redirect('/')
    return render_template('main_page.html', acc=session['user'], chats = 
            """
            <div class="chat-item active" data-chat-id="1">
                <div class="chat-name">Общий чат</div>
                <div class="chat-last-message"></div>
            </div>
            """)

@socketio.on('connect')
def handle_connect():
    print(f"Клиент подключился: {request.sid}")
    emit('connected', {'message': 'Connected to server'})

@socketio.on('disconnect')
def handle_disconnect():
    print(f"Клиент отключился: {request.sid}")

@socketio.on('send_message')
def handle_send_message(data):
    print(f"Получено сообщение: {data}")
    
    # data — это словарь, который приходит от клиента
    user = data.get('user')
    message = data.get('message')
    chat_id = data.get('chatid', 1)
    
    # Сохраняем сообщение в БД (если есть таблица messages)
    try:
        os.system('clear')
        cursor = mysql.connection.cursor()
        cursor.execute('''
            INSERT INTO chats (user_id, message, chat_id, created_at) 
            VALUES ((SELECT id FROM users WHERE username = %s), %s, %s, %s)
        ''', (user, message, chat_id, str(datetime.now())))
        mysql.connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Ошибка сохранения сообщения: {e}")
    
    # Отправляем сообщение всем клиентам
    os.system("clear")
    now = datetime.now()
    emit('new_message', {
        'user': user,
        'message': message,
        'chat_id': chat_id,
        'timestamp': now.strftime("%H:%M")
    }, broadcast=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/api/messages/<int:chat_id>')
def get_messages(chat_id):
    """Получить историю сообщений чата"""
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    cursor = mysql.connection.cursor()
    cursor.execute('''
        SELECT m.*, u.username
        FROM chats m 
        JOIN users u ON m.user_id = u.id 
        WHERE m.chat_id = %s 
        LIMIT 100
    ''', (chat_id,))
    messages = cursor.fetchall()
    cursor.close()
    
    return jsonify(messages)

if __name__ == '__main__':
    socketio.run(app, port=5001, debug=True, host='0.0.0.0')
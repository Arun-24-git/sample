
import pytesseract, re, sqlite3, cv2, requests

DB_PATH = 'database.db'

def extract_text_and_pin(image_path):
    img = cv2.imread(image_path)
    text = pytesseract.image_to_string(img)
    pin_match = re.search(r'\b\d{6}\b', text)
    pin = pin_match.group() if pin_match else '000000'
    return text, pin

def assign_bin(pin):
    mapping = {
        '110001': 'bin_north',
        '600001': 'bin_south',
        '700001': 'bin_east'
    }
    return mapping.get(pin, 'bin_default')

def log_to_db(text, pin, bin_name):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            address TEXT,
            pin TEXT,
            bin TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    c.execute('INSERT INTO logs (address, pin, bin) VALUES (?, ?, ?)',
              (text, pin, bin_name))
    conn.commit()
    conn.close()

def notify_robot(pin, bin_name):
    try:
        url = 'http://localhost:5005/sort'
        data = {'pin': pin, 'bin': bin_name}
        requests.post(url, json=data, timeout=1)
    except Exception as e:
        print(f'[notify_robot] Error contacting ROS bridge: {e}')

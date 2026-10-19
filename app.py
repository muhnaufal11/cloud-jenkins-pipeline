from flask import Flask, jsonify, request, render_template_string
import database
import datetime

app = Flask(__name__)

# Ensure DB initialized on launch
database.init_db()

HTML_PAGE = """<!DOCTYPE html>
<html>
<head>
    <title>Cloud Computing - Jenkins & Docker Pipeline</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0f172a; color: #f8fafc; margin: 0; padding: 40px; }
        .card { max-width: 800px; margin: 0 auto; background: #1e293b; border-radius: 12px; padding: 32px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }
        h1 { color: #38bdf8; margin-top: 0; }
        .badge { background: #10b981; color: white; padding: 4px 10px; border-radius: 20px; font-size: 13px; font-weight: 600; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { text-align: left; padding: 12px; border-bottom: 1px solid #334155; }
        th { background: #334155; color: #94a3b8; }
        .footer { margin-top: 30px; font-size: 13px; color: #64748b; text-align: center; }
    </style>
</head>
<body>
    <div class="card">
        <h1>Cloud Computing - Praktikum CI/CD Pipeline</h1>
        <p>Aplikasi web Flask terintegrasi dengan <strong>SQLite Database</strong> dan dideploy menggunakan <strong>Jenkins & Docker</strong>.</p>
        <p>Status Sistem: <span class="badge">Running & Connected</span></p>
        
        <h3>Server & Service Status Logs</h3>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Service Name</th>
                    <th>Status</th>
                    <th>Timestamp</th>
                </tr>
            </thead>
            <tbody>
                {% for log in logs %}
                <tr>
                    <td>{{ log.id }}</td>
                    <td>{{ log.service_name }}</td>
                    <td><span class="badge">{{ log.status }}</span></td>
                    <td>{{ log.created_at }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>

        <div class="footer">
            Modul Praktikum Komputasi Awan 2026/2027 &copy; Muhammad Naufal Rabbani
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    logs = database.get_all_logs()
    return render_template_string(HTML_PAGE, logs=logs)

@app.route('/health')
def health():
    logs = database.get_all_logs()
    return jsonify({
        "status": "UP",
        "service": "cloud-jenkins-pipeline",
        "database": "SQLite (Connected)",
        "total_records": len(logs),
        "server_time": datetime.datetime.now().isoformat()
    })

@app.route('/api/logs', methods=['GET', 'POST'])
def handle_logs():
    if request.method == 'POST':
        data = request.get_json() or {}
        service = data.get('service_name', 'Unknown-Service')
        status = data.get('status', 'OK')
        database.add_log(service, status)
        return jsonify({"message": "Log added successfully"}), 201
    return jsonify(database.get_all_logs())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

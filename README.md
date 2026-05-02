##🔐 AI-Powered Network Security Monitor with RBAC

📌 Overview

This project is a Cybersecurity Monitoring System that combines real-time network analysis, AI-based threat explanation, and role-based access control (RBAC).

It simulates a mini Security Operations Center (SOC) dashboard, capable of detecting suspicious network activity, generating alerts, and explaining threats using AI.

---

🚀 Features

🔐 Authentication & Security

- Secure login system using SQLite database
- Password hashing with bcrypt
- Role-Based Access Control (Admin/User)

📡 Network Monitoring

- Real-time network connection tracking using psutil
- Optional packet sniffing using Scapy (if permissions allowed)
- Detection of suspicious ports and connections

🚨 Threat Detection

- Blacklist-based detection
- Suspicious activity detection (e.g., SSH attacks)
- Integration with VirusTotal API for real threat intelligence

🤖 AI-Powered Assistant

- Explains security alerts using AI
- Provides:
  - Meaning of the threat
  - Risk level
  - Fix and prevention tips

📊 Dashboard & Visualization

- Live updating dashboard
- Real-time alerts
- Traffic graph using Chart.js
- Terminal-style activity simulation

🎭 UI/UX

- Hacker-style animated interface
- Neon glow design
- Sliding sidebar navigation
- Mobile responsive layout

---

🛠️ Technologies Used

- Backend: Python, Flask
- Frontend: HTML, CSS, JavaScript
- Database: SQLite
- Authentication: Flask-Login, bcrypt
- Networking: psutil, Scapy
- Visualization: Chart.js
- AI Integration: OpenAI API
- Threat Intelligence: VirusTotal API

---

📁 Project Structure

cyber-ai-monitor/
│
├── app.py
├── config.py
├── requirements.txt
├── database.db
│
├── modules/
│   ├── auth.py
│   ├── db.py
│   ├── monitor.py
│   ├── detector.py
│   ├── ai_helper.py
│   ├── vt_api.py
│   ├── sniffer.py
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── alerts.html
│   ├── admin.html
│
├── static/
│   ├── style.css
│   ├── script.js
│   ├── alert.mp3
│
└── logs/
    └── activity.json

---

⚙️ Installation & Setup

1️⃣ Clone the Repository

git clone <your-repo-link>
cd cyber-ai-monitor

2️⃣ Install Dependencies

pip install -r requirements.txt

3️⃣ Configure API Keys

Edit "config.py":

OPENAI_API_KEY = "your_openai_api_key"
VIRUSTOTAL_API_KEY = "your_virustotal_api_key"

---

4️⃣ Run the Application

python app.py

Open in browser:

http://127.0.0.1:5000

---

🔑 Default Login Credentials

Role| Username| Password
Admin| admin| admin123
User| user| user123

---

📊 System Workflow

1. User logs in (RBAC applied)
2. System monitors network connections
3. Suspicious activity is detected
4. Alerts are generated
5. Alerts can be analyzed using:
   - VirusTotal API
   - AI explanation system
6. Results displayed on dashboard

---

⚠️ Limitations

- Packet sniffing may require administrator/root privileges
- Some college networks may restrict low-level access
- VirusTotal API has rate limits (free tier)

---

🔮 Future Enhancements

- JWT-based authentication
- Cloud deployment (AWS/Render)
- Email alerts system
- Advanced ML-based intrusion detection
- Mobile application version

---

🎓 Viva Explanation (Short)

«This project is an AI-powered cybersecurity monitoring system that performs real-time network analysis, detects suspicious activities, and explains threats using AI. It integrates external threat intelligence and ensures secure access using role-based authentication.»

---

📜 License

This project is for educational purposes.

---

👩‍💻 Author

Ojaswita Desai 

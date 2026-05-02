let allAlerts = [];

// 🎯 Sidebar toggle
function toggleSidebar() {
    let sidebar = document.getElementById("sidebar");
    let main = document.getElementById("main");

    if (sidebar && main) {
        sidebar.classList.toggle("active");
        main.classList.toggle("active");
    }
}

// 🔊 Play alert sound
function playSound() {
    let audio = new Audio('/static/alert.mp3');
    audio.play().catch(() => {});
}

// 🔁 Fetch data
function fetchData() {
    fetch('/api/data')
    .then(res => res.json())
    .then(data => {

        let conn = document.getElementById("connections");
        let alerts = document.getElementById("alerts");
        let logs = document.getElementById("logs");

        // 📡 Connections
        if (conn) {
            conn.innerHTML = "";
            data.connections.forEach(c => {
                conn.innerHTML += `<li>${c.ip}:${c.port}</li>`;
            });
        }

        // 🚨 Alerts
        if (alerts) {
            allAlerts = data.alerts;
            renderAlerts(allAlerts);
        }

        // 📊 Logs (Admin Panel)
        if (logs) {
            logs.innerHTML = "";
            data.alerts.forEach(a => {
                logs.innerHTML += `<li>[${a.severity}] ${a.message}</li>`;
            });
        }

        // 🔊 Sound if high alert
        if (data.alerts.some(a => a.severity === "HIGH")) {
            playSound();
        }

    })
    .catch(err => {
        console.error("Error fetching data:", err);
    });
}

// 🎨 Render alerts
function renderAlerts(alertList) {
    let alerts = document.getElementById("alerts");
    if (!alerts) return;

    alerts.innerHTML = "";

    alertList.forEach(a => {
        let color = "white";

        if (a.severity === "HIGH") color = "red";
        else if (a.severity === "MEDIUM") color = "orange";
        else if (a.severity === "LOW") color = "yellow";

        alerts.innerHTML += `
        <li style="color:${color}">
            [${a.severity}] ${a.message}
            <button onclick="explainAlert('${a.message.replace(/'/g, "\\'")}')">
                🤖 Explain
            </button>
        </li>`;
    });
}

// 🔍 Filter alerts
function filterAlerts() {
    let filter = document.getElementById("filter");
    if (!filter) return;

    let value = filter.value;

    if (value === "ALL") {
        renderAlerts(allAlerts);
    } else {
        let filtered = allAlerts.filter(a => a.severity === value);
        renderAlerts(filtered);
    }
}

// 🤖 AI explain
function explainAlert(alertText) {
    fetch('/explain', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: 'alert=' + encodeURIComponent(alertText)
    })
    .then(res => res.text())
    .then(data => {
        alert(data);
    })
    .catch(() => {
        alert("AI explanation unavailable");
    });
}

// ▶ Initial load
fetchData();

// 🔁 Auto refresh every 3 sec
setInterval(fetchData, 3000);

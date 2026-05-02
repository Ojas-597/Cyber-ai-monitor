let allAlerts = [];

// Sidebar toggle
function toggleSidebar() {
    let sidebar = document.getElementById("sidebar");
    let main = document.getElementById("main");

    sidebar.classList.toggle("active");
    main.classList.toggle("active");
}

// Fetch data
function fetchData() {
    fetch('/api/data')
    .then(res => res.json())
    .then(data => {

        let conn = document.getElementById("connections");
        let alerts = document.getElementById("alerts");

        // Connections
        if (conn) {
            conn.innerHTML = "";
            data.connections.forEach(c => {
                conn.innerHTML += `<li>${c.ip}:${c.port}</li>`;
            });
        }

        // Alerts
        if (alerts) {
            allAlerts = data.alerts;
            renderAlerts(allAlerts);
        }
    });
}

// Render alerts
function renderAlerts(alertList) {
    let alerts = document.getElementById("alerts");
    if (!alerts) return;

    alerts.innerHTML = "";

    alertList.forEach(a => {
        let color = "white";

        if (a.severity === "HIGH") color = "red";
        if (a.severity === "MEDIUM") color = "orange";
        if (a.severity === "LOW") color = "yellow";

        alerts.innerHTML += `
        <li style="color:${color}">
            [${a.severity}] ${a.message}
            <button onclick="explain('${a.message}')">Explain</button>
        </li>`;
    });
}

// Filter alerts
function filterAlerts() {
    let value = document.getElementById("filter").value;

    if (value === "ALL") {
        renderAlerts(allAlerts);
    } else {
        let filtered = allAlerts.filter(a => a.severity === value);
        renderAlerts(filtered);
    }
}

// AI explain
function explain(alert) {
    fetch('/explain', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: 'alert=' + encodeURIComponent(alert)
    })
    .then(res => res.text())
    .then(data => {
        alert(data);
    });
}

// Auto refresh
setInterval(fetchData, 3000);

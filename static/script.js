function toggleSidebar() {
 let sidebar = document.getElementById("sidebar");
 let main = document.getElementById("main");

 sidebar.classList.toggle("active");
 main.classList.toggle("active");
}

// Auto refresh
setInterval(fetchData, 3000);

function fetchData() {
 fetch('/api/data')
 .then(res => res.json())
 .then(data => {

 let conn = document.getElementById("connections");
 let alerts = document.getElementById("alerts");

 if(conn){
 conn.innerHTML="";
 data.connections.forEach(c=>{
 conn.innerHTML += `<li>${c.ip}:${c.port}</li>`;
 });
 }

 if(alerts){
 alerts.innerHTML="";
 data.alerts.forEach(a=>{
 alerts.innerHTML += `<li style="color:red">${a}</li>`;
 });
 }
 });
}

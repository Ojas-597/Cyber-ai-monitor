setInterval(fetchData, 3000);
setInterval(loadChart, 3000);

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
                alerts.innerHTML += `<li style="color:red">${a}
                <button onclick="explain('${a}')">Explain</button></li>`;
            });

            if(data.alerts.length>0) playSound();
        }
    });
}

function explain(alert){
    fetch('/explain',{
        method:'POST',
        headers:{'Content-Type':'application/x-www-form-urlencoded'},
        body:'alert='+alert
    })
    .then(res=>res.text())
    .then(data=>alert(data));
}

function playSound(){
    new Audio('/static/alert.mp3').play();
}

/* Chart */
let chart;

function loadChart(){
    fetch('/api/traffic')
    .then(res=>res.json())
    .then(data=>{
        let ctx=document.getElementById("trafficChart").getContext("2d");

        if(chart) chart.destroy();

        chart=new Chart(ctx,{
            type:'line',
            data:{
                labels:data.map((_,i)=>i),
                datasets:[{label:'Traffic',data:data}]
            }
        });
    });
}

/* Terminal */
function terminal(){
    let t=document.getElementById("terminal");
    if(!t) return;

    let msgs=["Scanning...","Analyzing...","Detecting threats..."];
    let i=0;

    setInterval(()=>{
        t.innerHTML+=msgs[i%msgs.length]+"\n";
        i++;
    },1500);
}

terminal();

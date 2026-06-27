const REFRESH_INTERVAL = 5000;

async function fetchMetrics() {
    try {
        const res = await fetch('/api/metrics');
        const data = await res.json();
        updateDashboard(data);
        updateConnectionStatus(true);
    } catch (err) {
        updateConnectionStatus(false);
        console.error('Metrics fetch failed:', err);
    }
}

function updateDashboard(data) {
    // Timestamp
    document.getElementById('lastUpdated').textContent = `Updated: ${data.timestamp}`;

    // CPU
    document.getElementById('cpuPercent').textContent = `${data.cpu.percent}%`;
    document.getElementById('cpuCores').textContent = `${data.cpu.cores} cores`;
    document.getElementById('cpuBar').style.width = `${data.cpu.percent}%`;
    setBarColor('cpuBar', data.cpu.status);
    setBadge('cpuStatus', data.cpu.status);
    setCardStatus('cpuCard', data.cpu.status);

    // Memory
    document.getElementById('memoryPercent').textContent = `${data.memory.percent}%`;
    document.getElementById('memoryDetail').textContent = `${data.memory.used_gb} GB / ${data.memory.total_gb} GB`;
    document.getElementById('memoryBar').style.width = `${data.memory.percent}%`;
    setBarColor('memoryBar', data.memory.status);
    setBadge('memoryStatus', data.memory.status);
    setCardStatus('memoryCard', data.memory.status);

    // Disk
    document.getElementById('diskPercent').textContent = `${data.disk.percent}%`;
    document.getElementById('diskDetail').textContent = `${data.disk.used_gb} GB / ${data.disk.total_gb} GB`;
    document.getElementById('diskBar').style.width = `${data.disk.percent}%`;
    setBarColor('diskBar', data.disk.status);
    setBadge('diskStatus', data.disk.status);
    setCardStatus('diskCard', data.disk.status);

    // Network
    document.getElementById('netSent').textContent = `${data.network.bytes_sent_mb} MB`;
    document.getElementById('netRecv').textContent = `${data.network.bytes_recv_mb} MB`;

    // Alerts
    const alertCount = data.alerts.length;
    document.getElementById('alertCount').textContent = alertCount;

    const banner = document.getElementById('alertBanner');
    if (alertCount > 0) {
        banner.style.display = 'block';
        document.getElementById('alertMessage').textContent =
            data.alerts.map(a => a.message).join(' | ');
        document.getElementById('overallHealth').textContent = 'Alert';
        document.getElementById('overallHealth').className = 'card-badge critical';
    } else {
        banner.style.display = 'none';
        document.getElementById('overallHealth').textContent = 'Healthy';
        document.getElementById('overallHealth').className = 'card-badge healthy';
    }
}

async function getDiagnosis() {
    const aiContent = document.getElementById('aiContent');
    const aiStatus = document.getElementById('aiStatus');

    aiStatus.textContent = 'Analyzing...';
    aiStatus.className = 'card-badge warning';
    aiContent.innerHTML = '<div class="ai-idle">🤖 AI is analyzing your infrastructure metrics...</div>';

    try {
        const res = await fetch('/api/diagnose');
        const data = await res.json();

        if (data.diagnosis) {
            aiContent.innerHTML = `<div class="ai-result">${data.diagnosis}</div>`;
            aiStatus.textContent = 'Complete';
            aiStatus.className = 'card-badge critical';
        } else {
            aiContent.innerHTML = `<div class="ai-idle">✅ ${data.message}</div>`;
            aiStatus.textContent = 'Healthy';
            aiStatus.className = 'card-badge healthy';
        }
    } catch (err) {
        aiContent.innerHTML = '<div class="ai-idle">❌ AI diagnosis failed. Check your Groq API key in .env</div>';
        aiStatus.textContent = 'Error';
        aiStatus.className = 'card-badge critical';
    }
}

function setBarColor(id, status) {
    const bar = document.getElementById(id);
    if (status === 'critical') bar.style.background = 'linear-gradient(90deg, #ef4444, #dc2626)';
    else if (status === 'warning') bar.style.background = 'linear-gradient(90deg, #f59e0b, #d97706)';
    else bar.style.background = 'linear-gradient(90deg, #3b82f6, #06b6d4)';
}

function setBadge(id, status) {
    const badge = document.getElementById(id);
    badge.textContent = status.charAt(0).toUpperCase() + status.slice(1);
    badge.className = `card-badge ${status}`;
}

function setCardStatus(id, status) {
    const card = document.getElementById(id);
    card.className = 'card';
    if (status !== 'healthy') card.classList.add(`status-${status}`);
}

function updateConnectionStatus(connected) {
    const el = document.getElementById('connectionStatus');
    if (connected) {
        el.textContent = '● Live';
        el.style.color = '#10b981';
    } else {
        el.textContent = '● Disconnected';
        el.style.color = '#ef4444';
    }
}

// Start
fetchMetrics();
setInterval(fetchMetrics, REFRESH_INTERVAL);
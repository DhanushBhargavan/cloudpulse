from flask import Blueprint, render_template, jsonify
from app.metrics import get_system_metrics, get_alerts
from app.ai_diagnosis import diagnose_anomaly

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Serve the main dashboard."""
    return render_template('index.html')

@main.route('/api/metrics')
def metrics():
    """Return current system metrics as JSON."""
    data = get_system_metrics()
    alerts = get_alerts(data)
    data['alerts'] = alerts
    return jsonify(data)

@main.route('/api/diagnose')
def diagnose():
    """Return AI diagnosis for current anomalies."""
    data = get_system_metrics()
    alerts = get_alerts(data)
    
    if not alerts:
        return jsonify({'diagnosis': None, 'message': 'All systems healthy — no anomalies detected'})
    
    diagnosis = diagnose_anomaly(data, alerts)
    return jsonify({'diagnosis': diagnosis, 'alerts': alerts})

@main.route('/api/health')
def health():
    """Simple health check endpoint."""
    return jsonify({'status': 'ok', 'service': 'CloudPulse'})
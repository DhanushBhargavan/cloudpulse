import os
from groq import Groq
from config import Config

client = Groq(api_key=Config.GROQ_API_KEY)

def diagnose_anomaly(metrics, alerts):
    """Send metrics to Groq AI for anomaly diagnosis."""
    
    if not alerts:
        return None
    
    prompt = f"""
You are a cloud infrastructure monitoring assistant.
Analyze these system metrics and provide a brief, clear diagnosis.

Current Metrics:
- CPU Usage: {metrics['cpu']['percent']}%
- Memory Usage: {metrics['memory']['percent']}% ({metrics['memory']['used_gb']}GB / {metrics['memory']['total_gb']}GB)
- Disk Usage: {metrics['disk']['percent']}% ({metrics['disk']['used_gb']}GB / {metrics['disk']['total_gb']}GB)
- Network Sent: {metrics['network']['bytes_sent_mb']}MB
- Network Received: {metrics['network']['bytes_recv_mb']}MB

Active Alerts:
{chr(10).join([f"- {a['component']}: {a['message']}" for a in alerts])}

Provide:
1. Root cause hypothesis (1-2 sentences)
2. Recommended immediate action (1-2 sentences)
3. Severity level: LOW / MEDIUM / HIGH / CRITICAL

Keep response under 100 words. Be direct and technical.
"""
    
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI diagnosis unavailable: {str(e)}"
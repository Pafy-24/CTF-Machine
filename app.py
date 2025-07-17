#!/usr/bin/env python3
from flask import Flask, request, render_template_string, jsonify
import os
import subprocess
import sys

app = Flask(__name__)

# HTML template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>PenguLinux System Monitor</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f0f8ff; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 20px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; text-align: center; }
        .form-group { margin: 20px 0; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input[type="text"] { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
        button { background-color: #3498db; color: white; padding: 12px 30px; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background-color: #2980b9; }
        .output { background-color: #ecf0f1; padding: 15px; border-radius: 5px; margin-top: 20px; white-space: pre-wrap; font-family: monospace; }
        .hint { background-color: #fff3cd; padding: 10px; border-radius: 5px; margin-top: 10px; border-left: 4px solid #ffc107; }
        .ascii { text-align: center; margin: 20px 0; font-family: monospace; color: #2c3e50; }
        .warning { background-color: #f8d7da; padding: 10px; border-radius: 5px; margin-top: 10px; border-left: 4px solid #dc3545; color: #721c24; }
    </style>
</head>
<body>
    <div class="container">
        <div class="ascii">
          .--.<br>
         |o_o |<br>
         |:_/ |<br>
        //   \ \\<br>
       (|     | )<br>
      /'\_   _/`\\<br>
      \___)=(___/<br>
        </div>
        
        <h1>🐧 PenguLinux System Monitor 🐧</h1>
        
        <div class="hint">
            <strong>Challenge 3:</strong> Welcome to the system monitor--THE LAST STEP INTO OVERTAKING PenguLinux! This is a WEB-ONLY challenge. 
            SSH access is restricted to view the welcome message only. The shell has been locked down.
            Find the vulnerability in this web application to retrieve the final flag!
        </div>
        
        <div class="warning">
            <strong>Note:</strong> The shell environment has been restricted. Use this web interface to interact with the system.
        </div>
        
        <div class="form-group">
            <h3>Quick Actions:</h3>
            <a href="/monitor?command=ps"><button type="button">Show Processes</button></a>
            <a href="/monitor?command=whoami"><button type="button">Current User</button></a>
            <a href="/monitor?command=id"><button type="button">User ID</button></a>
            <a href="/monitor?command=ls -la"><button type="button">List Files</button></a>
            <a href="/monitor?command=cat /etc/passwd"><button type="button">View Users</button></a>
        </div>
        
        {% if output %}
        <div class="output">{{ output | e }}</div>
        {% endif %}
        
        {% if error %}
        <div class="output" style="color: red;">Error: {{ error }}</div>
        {% endif %}
        
        <div class="hint">
            <strong>Hint:</strong> The system's most sensitive information is usually stored in secret files... 
            Can you find it? 🔍
        </div>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/monitor', methods=['GET', 'POST'])
def monitor():
    output = ""
    error = ""
    command = ""
    
    if request.method == 'POST':
        command = request.form.get('command', '')
    else:
        command = request.args.get('command', '')
    
    if command and ' ' not in command and '+' not in command and '%20' not in command:
        try:
            # VULNERABLE: Direct command injection
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
            output = result.stdout
            if result.stderr:
                error = result.stderr
        except subprocess.TimeoutExpired:
            error = "Command timed out"
        except Exception as e:
            error = str(e)
    
    return render_template_string(HTML_TEMPLATE, output=output, error=error, command=command)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)

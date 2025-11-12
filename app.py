from flask import Flask, request
import socket
import datetime
import os
import pytz 

app = Flask(__name__)

# --- Helper function to get the container's internal IP address ---
def get_server_internal_ip():
    """Tries to determine the container's internal IP address."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Connect to a public server (like Google's DNS) to get the IP used for outgoing connection.
        s.connect(("8.8.8.8", 80)) 
        internal_ip = s.getsockname()[0]
        s.close()
        return internal_ip
    except Exception:
        return "N/A (Local)"

@app.route("/")
def index():
    # --- Gather all dynamic data ---
    # In a Docker container, socket.gethostname() returns the Container ID
    container_id = socket.gethostname() 
    server_ip = get_server_internal_ip()
    client_ip = request.remote_addr
    
    # --- Set Time Zone to IST (Indian Standard Time) ---
    try:
        ist = pytz.timezone('Asia/Kolkata')
        current_time_ist = datetime.datetime.now(ist).strftime("%Y-%m-%d %H:%M:%S %Z")
    except Exception:
        # Fallback if pytz isn't installed
        current_time_ist = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S (UTC Fallback)")


    # --- Start building the HTML response ---
    return f"""
    <html>
        <head>
            <title>BeeN Service Dashboard</title>
            <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700;800&family=Orbitron:wght@700&display=swap" rel="stylesheet">
            
            <style>
                /* 🎨 VIBRANT COLOR PALETTE */
                :root {{
                    --color-bg-light: #f0f2f5; 
                    --color-card: #ffffff;
                    --color-gradient-start: #6a11cb; /* Purple */
                    --color-gradient-end: #2575fc; /* Blue */
                    --color-text-dark: #2c3e50;
                    --color-text-light: #fdfdfd;
                    --color-text-muted: #7f8c8d;
                    --color-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
                    /* Dynamic Data Colors */
                    --color-pill-id: #e74c3c; /* Red */
                    --color-pill-ip: #f39c12; /* Orange */
                    --color-pill-client: #2ecc71; /* Green */
                    --color-pill-time: #3498db; /* Blue */
                    
                    /* New Stamp Color */
                    --color-stamp-blue: #007bff;
                }}

                body {{
                    font-family: 'Montserrat', sans-serif;
                    margin: 0;
                    padding: 0;
                    background-color: var(--color-bg-light);
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    min-height: 100vh;
                    color: var(--color-text-dark);
                }}

                /* 📦 Enhanced Card UI */
                .container {{
                    text-align: center;
                    background: var(--color-card);
                    border-radius: 12px;
                    box-shadow: var(--color-shadow);
                    max-width: 750px;
                    width: 90%;
                    overflow: hidden;
                    position: relative;
                }}
                
                /* Colorful left accent border */
                .container::before {{
                    content: '';
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 8px; /* Width of the colored bar */
                    height: 100%;
                    background: linear-gradient(to bottom, var(--color-gradient-start), var(--color-gradient-end));
                }}
                
                /* --- ROUND & ANIMATED Verified Stamp --- */
                @keyframes bluePulse {{
                    0% {{ box-shadow: 0 0 0 0 rgba(0, 123, 255, 0.7); }}
                    70% {{ box-shadow: 0 0 0 20px rgba(0, 123, 255, 0); }}
                    100% {{ box-shadow: 0 0 0 0 rgba(0, 123, 255, 0); }}
                }}

                .verified-stamp {{
                    position: fixed;
                    left: 20px;
                    top: 20px;
                    background-color: var(--color-stamp-blue);
                    color: white;
                    width: 120px;
                    height: 120px;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-weight: 700;
                    font-size: 0.9em;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
                    animation: bluePulse 2s infinite; 
                    z-index: 10;
                    text-align: center;
                    line-height: 1.2;
                    border: 3px solid rgba(255,255,255,0.8);
                }}

                /* Header Block with Gradient */
                .header-block {{
                    background: linear-gradient(135deg, var(--color-gradient-start), var(--color-gradient-end));
                    color: var(--color-text-light);
                    padding: 30px 50px;
                    text-align: center;
                    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
                    margin-bottom: 25px;
                }}

                h1 {{
                    font-family: 'Orbitron', sans-serif;
                    font-size: 2.5em;
                    font-weight: 800;
                    margin: 0;
                    text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.1);
                }}
                
                h3 {{
                    color: rgba(255, 255, 255, 0.85);
                    font-size: 1.1em;
                    font-weight: 400;
                    margin: 10px 0 0;
                }}
                
                .motto {{
                    font-size: 0.9em;
                    font-weight: 700;
                    color: #fff;
                    background-color: rgba(255, 255, 255, 0.15);
                    padding: 5px 10px;
                    border-radius: 5px;
                    margin-top: 15px;
                    display: inline-block;
                }}

                .passion-line {{
                    color: var(--color-text-muted);
                    font-size: 1.1em;
                    padding: 0 50px 25px;
                    border-bottom: 1px dashed var(--color-border);
                    margin-bottom: 25px;
                }}

                .info-box {{
                    text-align: left;
                    padding: 0 50px 30px 50px;
                }}

                /* 🌈 Dynamic Color-Coded Pills */
                .info-box p {{
                    font-size: 1.1em;
                    margin: 20px 0;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    transition: all 0.3s ease;
                }}
                
                .info-box p:hover {{
                    transform: translateY(-2px);
                    color: var(--color-gradient-end);
                }}

                .info-box p b {{
                    color: var(--color-text-dark);
                    font-weight: 700;
                    flex-shrink: 0;
                }}

                .data-pill {{
                    padding: 8px 15px;
                    border-radius: 20px;
                    font-weight: 700;
                    font-size: 0.9em;
                    color: var(--color-text-light);
                    transition: all 0.3s ease;
                    text-align: right;
                    word-break: break-all;
                    max-width: 60%;
                }}
                
                /* Specific Pill Colors */
                .id-pill {{ background-color: var(--color-pill-id); }}
                .ip-pill {{ background-color: var(--color-pill-ip); }}
                .client-pill {{ background-color: var(--color-pill-client); }}
                .time-pill {{ background-color: var(--color-pill-time); }}
                
                /* --- Dynamic Colourful BeeN Text --- */
                @keyframes colorShift {{
                    0% {{ filter: hue-rotate(0deg) brightness(1.2); }}
                    100% {{ filter: hue-rotate(360deg) brightness(1.2); }}
                }}
                
                .been-dynamic-color {{
                    display: inline-block;
                    animation: colorShift 5s linear infinite;
                    text-shadow: 0 0 5px rgba(255, 255, 255, 0.5);
                    font-weight: 800;
                    font-size: 1.2em;
                }}

                /* --- Footer/Copyright --- */
                .footer {{
                    background-color: #f8f9fa;
                    color: var(--color-text-muted);
                    padding: 15px;
                    font-size: 0.9em;
                    border-top: 1px solid var(--color-border);
                    margin-top: 20px;
                }}
            </style>
        </head>
        <body>
            <div class="verified-stamp">Verified<br>by<br>BeeN</div>
            
            <div class="container">
                <div class="header-block">
                    <h1>BeeN Flask-App Service</h1>
                    <div class="motto">Build | Educate | Execute | Navigate</div>
                    <h3>
                        <span class="sree-name">👨‍💻 Created by Sree</span>
                        | 
                        🐝 <span class="been-dynamic-color">Maintained & Sponsored by BeeN</span>
                    </h3>
                </div>

                <p class="passion-line"><b>💡 DevOps | Python | Production-Grade Infrastructure</b></p>

                <div class="info-box">
                    <p>
                        <b>📦 Docker Container ID / Hostname:</b> 
                        <span class="data-pill id-pill">{container_id}</span>
                    </p>
                    <p>
                        <b>🏠 Server Internal IP:</b> 
                        <span class="data-pill ip-pill">{server_ip}</span>
                    </p>
                    <p>
                        <b>🌍 Client IP Address:</b> 
                        <span class="data-pill client-pill">{client_ip}</span>
                    </p>
                    <p>
                        <b>⏰ Server Time (IST):</b> 
                        <span class="data-pill time-pill">{current_time_ist}</span>
                    </p>
                </div>
                
                <div class="footer">
                    &copy; {datetime.datetime.now().year} All rights reserved to **BeeN subscriber**. Thank you for using this service.
                </div>
            </div>
        </body>
    </html>
    """

@app.route("/health")
def health():
    return "healthy", 200

if __name__ == '__main__':
    # Flask default port is 8000, but checking environment variable is standard practice for deployment
    port = int(os.environ.get('PORT', 8000))
    print(f" * Starting Flask server on http://0.0.0.0:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)

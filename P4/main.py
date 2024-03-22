# project: p4
# submitter: kkhill4
# partner: none
# hours: 15

import pandas as pd
from flask import Flask, render_template, jsonify, request, abort
from collections import Counter
import time
import matplotlib

matplotlib.use('Agg')


app = Flask(__name__)


# For A/B Test
a = 0
b = 0
total_visits = 0 

@app.route('/')
def home():
    global total_visits, a, b
    if total_visits < 10:
        template_name = "index.html" if total_visits % 2 == 0 else "index_alt.html"
    else:
        template_name = "index.html" if a >= b else "index_alt.html"
    with open(template_name) as f:
        html = f.read()
    total_visits += 1  
    return html



# for browse(), browse_json(), visitors_json()
df = pd.read_csv("server_log.zip", compression="zip", nrows=500)
ip_access_times = {}
visited_ips = set()


@app.route('/browse.html')
def browse():
    table = df.head(500).to_html(index=False)
    content = "<html><body><h1>Browse Page</h1>{}</body></html>".format(table)
    return content

visitor = []
times = {}

@app.route('/browse.json')
def browse_json():
    global visitors, times
    rate = 3
    ip = request.remote_addr
    ua = request.user_agent.string
    visitors.append([ip, ua])
    now = time.time()
    if ip in times:
        td = now - times[ip]
        if td < rate:
            return Response("Please come back in " + str(rate - td) + " seconds.", status = 429, headers = {"Retry-After": str(rate)})
        else:
            times[ip] = now
            return "Welcome back, [" + ip + "] " + ua
    else:
        times[ip] = now
        return "Hello, [" + ip + "] " + ua

@app.route('/visitors.json')
def visitors_json():
    visited_ips.add(request.remote_addr)
    ip_list = list(visited_ips)
    return jsonify(ip_list)


@app.route('/donate.html')
def donate():
    global a, b
    version = request.args.get("from", "A")
    if version == "A":
        a += 1
    elif version == "B":
        b += 1
    with open("donate.html") as f:
        html = f.read()
    return html  
    
                    
@app.route('/analysis.html')
def analysis():
              
    with open("analysis.html") as f:
        html = f.read()
    return html

                    
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, threaded=False)
 # don't change this line!

# NOTE: app.run never returns (it runs for ever, unless you kill the process)
# Thus, don't define any functions after the app.run call, because it will
# never get that far.
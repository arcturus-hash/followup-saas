from flask import Flask, request, jsonify, render_template_string
import json
import os

app = Flask(__name__)

DATA_FILE = "followups.json"

def load_followups():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_followups(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

HTML = """
<!doctype html>
<title>Follow-up Tracker</title>
<h1>Follow-up Tracker</h1>

<form method="post" action="/add">
  <input name="text" placeholder="Call instagram lead tommorrow">
  <button>Add</button>
</form>

<ul>
{% for f in followups %}
  <li style="color: {% if f.done %}gray{% else %}black{% endif %};
           text-decoration: {% if f.done %}line-through{% else %}none{% endif %};">
    {{ f.text }}
    {% if not f.done %}
        <a href="/done/{{ loop.index0 }}"> ✅</a>
    {% else %}
        ✔
    {% endif %}
<li style="color: {% if f.done %}gray{% else %}black{% endif %};
           text-decoration: {% if f.done %}line-through{% else %}none{% endif %};">
    {{ f.text }}

    {% if not f.done %}
        <a href="/done/{{ loop.index0 }}"> ✅</a>
    {% endif %}

    <a href="/delete/{{ loop.index0 }}" style="color:red;"> ❌</a>
</li>
    {% if not f.done %}
      <a href="/done/{{ loop.index0 }}">✅</a>
    {% else %}
      ✔
    {% endif %}
  </li>
{% endfor %}
</ul>
"""

@app.route("/")
def index():
    followups = load_followups()
    return render_template_string(HTML, followups=followups)

@app.route("/add", methods=["POST"])
def add():
    followups = load_followups()
    followups.append({
        "text": request.form["text"],
        "done": False
    })
    save_followups(followups)
    return "", 302, {"Location": "/"}

@app.route("/done/<int:i>")
def done(i):
    followups = load_followups()
    followups[i]["done"] = True
    save_followups(followups)
    return "", 302, {"Location": "/"}
@app.route("/delete/<int:i>")
def delete(i):
    followups = load_followups()
    if 0 <= i < len(followups):
        followups.pop(i)
        save_followups(followups)
    return "", 302, {"Location": "/"}
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


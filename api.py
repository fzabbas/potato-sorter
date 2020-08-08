import uuid
import json
from pathlib import Path
from flask import Flask, request, url_for, redirect, send_from_directory
# set the project root directory as the static folder, you can set others.
app = Flask(__name__)

POTATO_ROOT = Path("potato")
POTATO_ROOT.mkdir(parents=True, exist_ok=True)

@app.route('/')
def root():
    print("in the root")
    return app.send_static_file('index.html')

@app.route('/potato', methods=["POST"])
def make_potato():
    print("make new potato")
    print(request.form["potato"])
    potato_name = request.form["potato"]
    decision_framework = "regret"
    table = generate_table(framework=decision_framework)
    potato = {
        "name": potato_name, 
        "decision_framework": decision_framework, 
        "table": table
    }
    potato_id = str(uuid.uuid4())
    potato_path = path_for_potato(potato_id=potato_id)
    with open(potato_path,"w") as f:
        json.dump(potato, f)
    return redirect(url_for("potato", potato_id=potato_id))

@app.route("/potato/<potato_id>", methods=["GET"])
def potato(potato_id):
    print(request.headers)
    print(request.headers.get('Accept', ""))
    if request.headers.get('Accept', "") == "application/json":
        potato_path = path_for_potato(potato_id=potato_id)
        print(f"serving json for {potato_path}")
        with open(potato_path, "r") as f:
            return json.load(f)
    else:
        print(f"Serving potato.html for {potato_id}")
        return app.send_static_file("potato.html")

def generate_table(framework):
    if framework =="regret":
        return {"options":[], "users":[], "choices":{}}

def path_for_potato(potato_id):
    return POTATO_ROOT / f"{potato_id}.json"


print("this is running")
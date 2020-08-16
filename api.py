import uuid
import json
from pathlib import Path
from flask import Flask, request, url_for, redirect, send_from_directory


POTATO_ROOT = Path("potato")
POTATO_ROOT.mkdir(parents=True, exist_ok=True)

def create_app():
    # set the project root directory as the static folder, you can set others.
    app = Flask(__name__)
    app.config["DEBUG"] = True

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
        print(f"Serving potato.html for {potato_id}")
        return app.send_static_file("potato.html")

    @app.route("/potato/<potato_id>/state", methods=["GET"])
    def potato_state(potato_id):
        print(request.headers)
        print(request.headers.get('Accept', ""))
        potato_path = path_for_potato(potato_id=potato_id)
        print(f"serving json for {potato_path}")
        with open(potato_path, "r") as f:
            return json.load(f)

    @app.route("/potato/<potato_id>/option", methods=["POST"])
    def update_choice(potato_id):
        changes = request.form
        old_choice = changes["oldOption"]
        new_choice = changes["newOption"]
        potato_path = path_for_potato(potato_id=potato_id)
        with open(potato_path, "r") as f:
            potato_state = json.load(f)
        potato_table = potato_state["table"]
        if old_choice ==" ":
            potato_table["choices"][new_choice]= {}
        else:
            potato_table["choices"][new_choice] = potato_table["choices"].pop(old_choice) 
        with open(potato_path,"w") as f:
            json.dump(potato_state, f)
        return "updated potato", 202


    @app.route("/potato/<potato_id>/weight", methods=["POST"])
    def update_potato(potato_id):
        changes = request.form
        user = changes["user"]
        option = changes["option"]
        weight = changes["weight"]
        potato_path = path_for_potato(potato_id=potato_id)
        with open(potato_path, "r") as f:
            potato_state = json.load(f)
        potato_table = potato_state["table"]
        # if user not in potato_table["users"]:
        #     potato_table["users"].append(user)
        potato_table["choices"][option][user] = int(weight)
        with open(potato_path,"w") as f:
            json.dump(potato_state, f)
        return "updated potato", 202
    
    @app.route("/potato/<potato_id>/user", methods=["POST"])
    def update_user(potato_id):
        changes = request.form
        user = changes["newUser"]
        potato_path = path_for_potato(potato_id=potato_id)   

        with open(potato_path, "r") as f:
            potato_state = json.load(f)
            potato_table = potato_state["table"]
        if user not in potato_table["users"]:
            potato_table["users"].append(user)
            with open(potato_path,"w") as f:
                json.dump(potato_state, f)
            return "updated potato", 202
            
    def generate_table(framework):
        if framework =="regret":
            return {"users":[], "choices":{}}

    def path_for_potato(potato_id):
        return POTATO_ROOT / f"{potato_id}.json"


    print("this is running")
    return app
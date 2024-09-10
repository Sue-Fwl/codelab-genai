import os
import json, logging

class JsonFormatter(logging.Formatter):
    def format(self, record):
        json_log_object = {
            "severity": record.levelname,
            "message": record.getMessage(),
        }
        json_log_object.update(getattr(record, "json_fields", {}))
        return json.dumps(json_log_object)
logger = logging.getLogger(__name__)
sh = logging.StreamHandler()
sh.setFormatter(JsonFormatter())
logger.addHandler(sh)
logger.setLevel(logging.DEBUG)

from flask import Flask, request

import google.auth
import vertexai
from vertexai.generative_models import GenerativeModel

_, project = google.auth.default()

app = Flask(__name__)

@app.route("/")
def hello_world():
    vertexai.init(project=project, location="us-central1")
    model = GenerativeModel("gemini-1.5-flash")
    animal = request.args.get("animal", "dog") 
    #prompt = f"Give me 10 not so fun facts about {animal}, and right after give me 10 fun facts about cats. Return this as html without backticks."
    prompt = f" أظهر لعبة تعليمية لتعليم اللغة العربية تحاكي لعبة ذاكرة الكلمات، أظهر 10 كلمات 6 منهم تتعلق ببعضها و4 لاتتعلق ببعضها واسأل ايها لاتتعلق ببعضها" 
    #response = model.generate_content(prompt)
    response = model.start_chat(prompt)
    json_fields = {"prompt": prompt, "response": response}
    logger.debug("Content is generated", extra={"json_fields": json_fields})
    return response.text

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
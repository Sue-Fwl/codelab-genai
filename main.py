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
    #model = GenerativeModel("gemini-1.5-flash")
    model = ChatModel("gemini-1.5-pro-001")
    #animal = request.args.get("animal", "dog") 
    #prompt = f"Give me 10 not so fun facts about {animal}, and right after give me 10 fun facts about cats. Return this as html without backticks."
    #prompt = f" أظهر لعبة تعليمية لتعليم اللغة العربية تحاكي لعبة ذاكرة الكلمات، أظهر 10 كلمات 6 منهم تتعلق ببعضها و4 لاتتعلق ببعضها واسأل ايها لاتتعلق ببعضها" 
    #response = model.generate_content(prompt)
    chat = chat_model.start_chat(
    context="My Name is Sana and you're my personal Arabic teacher. I'm a beginner and would like to learn the basics of Arabic Grammar using text based games.",
    #examples=[
    #    InputOutputTextPair(
    #        input_text="",
    #        output_text="I work for Ned.",
    #    ),
    #    InputOutputTextPair(
    #        input_text="What do I like?",
    #        output_text="Ned likes watching movies.",
    #    ),
    #],
    #    temperature=0.3,
    )

    chat.send_message("Design and execute a game in arabic to teach a beginner in arabic the basics of the arabic grammar. The game should be either a memory game or a scribble game, or a word game.")

    #json_fields = {"prompt": prompt, "response": response}
    #logger.debug("Content is generated", extra={"json_fields": json_fields})
    #return response.text
    return chat.text

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
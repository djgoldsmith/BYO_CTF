"""
Very simple Flask App.  For Testing
"""

import flask
app = flask.Flask(__name__)

errorPage = """
<div class="alert alert-danger" role="alert">
WHOx
</div>
{% endblock content %}
"""


theTemplate = """
<html>
<form>
  <input name="payload">
  <button class="submit">Go</button>
</form>
  
 <p>User Input is {{ userinput | safe}}</p>
</html>
"""

unsafeTemplate = """
<html>
<form>
  <input name="payload">
  <button class="submit">Go</button>
</form>
  
 <p>Unsafe Input is {}</p>
</html>
"""


def showError(theKing = None):
    """
    Display an Error Message to the users
    """
    if not theKing:
        theKing = "Unknown King"
    return flask.render_template_string(errorPage.replace("WHO", theKing))


@app.route('/')
def main():

    payload = flask.request.args.get("payload")
    
    #return flask.render_template('index.html', userinput=userinput)
    #return flask.render_template_string(theTemplate, userinput = payload)
    return flask.render_template_string(unsafeTemplate.format(payload))

@app.route('/debug')
def debug():
    return flask.Response(open(__file__).read(), mimetype='text/plain')

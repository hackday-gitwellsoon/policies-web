from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length
import requests

app = Flask(__name__)
app.config["SECRET_KEY"] = "git"
bootstrap = Bootstrap(app)

class SearchForm(FlaskForm):
	query = StringField("Search", validators=[DataRequired(), Length(min=0,max=256)], default="")
	filter = SelectField("Filter", choices=["Title", "Description", "Hospital"], default="Title")
	submit = SubmitField("Search")

@app.route('/', methods=["GET", "POST"])
def homePage():
	form = SearchForm()

	if form.validate_on_submit():
		query = form.query.data
		filter = form.filter.data
	else:
		query = "" # always show all results when no query is made
		filter = "Title" # default filter

	# results = requests.get(f'https://api.guidelines.fyi/documents?search_query="{query}"&filter="{filter}"')
	results = [{"id": i, "title": f"test {i + 1}"} for i in range(100)]

	return render_template("index.html", form=form, results=results)

@app.route('/document/<int:docId>')
def policyPage(docId):
	return render_template("policy.html", docId=docId)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=9000)
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
	query = StringField("Search", validators=[DataRequired(), Length(min=0,max=100)], default="")
	filter = SelectField("Filter", choices=["Title", "Description"], default="Title")
	submit = SubmitField("Search")

class HospitalSearchForm(FlaskForm):
	hospital_query = StringField("Hospital", validators=[DataRequired(), Length(min=0, max=100)])
	submit = SubmitField("Search")

@app.route('/', methods=["GET", "POST"])
def hospitalsPage():
	form = HospitalSearchForm()

	if form.validate_on_submit():
		hospital_query = form.hospital_query.data
	else:
		hospital_query = ""
	
	results = requests.get(f'https://api.guidelines.fyi/hospitals?search_query={hospital_query}').json()
	print(results, flush=True)

	return render_template("hospital_search.html", form=form, results=results)

@app.route('/search-policies/<int:hospitalId>', methods=["GET", "POST"])
def searchPage(hospitalId):
	form = SearchForm()

	if form.validate_on_submit():
		query = form.query.data
		filter = form.filter.data
	else:
		query = "" # always show all results when no query is made
		filter = "Title" # default filter

	results = requests.get(f'https://api.guidelines.fyi/documents?search_query={query}&filter_by={filter}&hospital_id={hospitalId}').json()

	return render_template("index.html", form=form, results=results)

@app.route('/document/<int:docId>')
def policyPage(docId):
	result = requests.get(f'https://api.guidelines.fyi/document_by_id/{id}').json()
	return render_template("policy.html", result=result)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=9000)
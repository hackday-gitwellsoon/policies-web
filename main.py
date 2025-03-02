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
	filter = SelectField("Filter", choices=["Title", "Description"], default="Title")
	submit = SubmitField("Search")

@app.route('/', methods=["GET", "POST"])
def homePage():
	form = SearchForm()
	searched = False
	if form.validate_on_submit():

		if False:
			print("commenting doesnt seem to be working, so this is the alternative")
			results = requests.get(f'https://api.guidelines.fyi/documents?search_query="{form.query.data}"&filter="{form.filter.data}"')

		results = [{"title": "test 1"}, {"title": "test 2"}, {"title": "test 3"}, {"title": "test 4"}]
		titles = []
		for result in results:
			titles.append(result["title"])
		searched = True
		return render_template("index.html", form=form, searched=searched, titles=titles)
	else:
		return render_template("index.html", form=form, searched=searched)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=9000)
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

app = Flask(__name__)
bootstrap = Bootstrap(app)

class SearchForm(FlaskForm):
	query = StringField("Search", validators=[DataRequired(), Length(min=0,max=256)])
	submit = SubmitField("Submit")

@app.route('/', methods=["GET", "POST"])
def homePage():
	form = SearchForm()
	if form.validate_on_submit():
		return render_template("searchResults.html", query = form.query.data)
	else:
		return render_template("index.html", form = form)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=9000)
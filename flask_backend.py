from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisasecret'
bootstrap = Bootstrap(app)
#http://127.0.0.1:5000/

class LyricForm(FlaskForm):
    lyric = StringField('lyric')

@app.route('/', methods =['GET', 'POST'])
def my_form():
    form = LyricForm()
    if form.validate_on_submit():
        text = request.form['lyric']
        processed = text
        return redirect(url_for('lyrics', lyric=processed))
    return render_template('text_box.html', form=form)

@app.route('/lyrics')
def lyrics():
    lyric = request.args.get('lyric', None)
    return render_template('Lyrics_page.html', lyric=lyric)

if __name__ == '__main__':
    app.run(debug=True)
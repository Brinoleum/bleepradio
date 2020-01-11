from src.process_lyrics import process_lyrics, output_processed
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
        processed = process_lyrics(text)
        return redirect(url_for('lyrics', lyric=processed))
    return render_template('text_box.html', form=form)

@app.route('/lyrics')
def lyrics():
    lyric = request.args.get('lyric', None)
    output_processed(lyric)
    lyric_location = "/static/output.mp3"
    return render_template('Lyrics_page.html', lyric=lyric, mp3=lyric_location)

if __name__ == '__main__':
    app.run(debug=True)

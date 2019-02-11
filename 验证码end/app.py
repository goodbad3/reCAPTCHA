from flask import Flask ,render_template,flash,url_for,redirect
from flask_wtf import FlaskForm,RecaptchaField

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'
app.config['RECAPTCHA_PUBLIC_KEY'] = '6Lcss5AUAAAAAOa4o7RjcV3NlQE2nR8XTFqPWoxg'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6Lcss5AUAAAAAPKjw5gc2uSco0QpkB9drx5l2nKu'

class RegisterForm(FlaskForm):
	
	recaptcha = RecaptchaField()

@app.route('/')
def index():
	return 'hello world'
@app.route('/register')
def register():
	form = RegisterForm()
	return render_template('index.html',form=form)
	


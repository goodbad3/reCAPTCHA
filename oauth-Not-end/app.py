import os
from flask import Flask,url_for
from flask_oauthlib.client import OAuth
app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'secret string')
oauth = OAuth(app)
#https://github.com/login?client_id=cf90e458d4c166593154&return_to=%2Flogin%2Foauth%2Fauthorize%3Fclient_id%3Dcf90e458d4c166593154%26redirect_uri%3Dhttp%253A%252F%252F127.0.0.1%253A5000%252Fcallback%252Fgithub%26response_type%3Dcode%26scope%3Duser

#https://github.com/login/oauth/authorize?client_id=cf90e458d4c166593154&redirect_uri=http%3A%2F%2F127.0.0.1%3A5000%2Fcallback%2Fgithub&response_type=code&scope=user

github = oauth.remote_app(
    name='github',
    consumer_key=os.getenv('GITHUB_CLIENT_ID'),
    consumer_secret=os.getenv('GITHUB_CLIENT_SECRET'),
    request_token_params={'scope': 'user'},
    base_url='https://api.github.com/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
)

providers = {
    'github': github
}

@app.route('/login/<provider_name>')
def oauth_login(provider_name):
    if provider_name not in providers.keys():
        abort(404)
    #if current_user.is_authenticated:
        #return redirect(url_for('/'))
    callback = url_for('.oauth_callback', provider_name=provider_name, _external=True)
    return providers[provider_name].authorize(callback=callback)

profile_endpoints = {
    'github': 'user'
}

def get_social_profile(provider, access_token):
    profile_endpoint = profile_endpoints[provider.name]
    response = provider.get(profile_endpoint, token=access_token)
    if provider.name == 'github':
        username = response.data.get('name')
        website = response.data.get('blog')
        github = response.data.get('html_url')
        email = response.data.get('email')
        bio = response.data.get('bio')
    return username, website, github, email, bio
@app.route('/callback/<provider_name>')
def oauth_callback(provider_name):
    if provider_name not in providers.keys():
        abort(404)
    provider = providers[provider_name]
    response = provider.authorized_response()
    if response is not None:
            access_token = response.get('access_token')
    else:
        access_token = None
    if access_token is None:
        flash('Access denied, please try again.')
        return redirect(url_for('login-u'))
    username, website, github, email, bio = get_social_profile(provider, access_token)

    user = User.query.filter_by(email=email).first()
    if user is None:
        user = User(email=email, nickname=username, website=website,
                    github=github, bio=bio)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        return redirect(url_for('/profile'))
    login_user(user, remember=True)
    return redirect(url_for('/'))




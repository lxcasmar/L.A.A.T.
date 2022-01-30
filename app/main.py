import csv
from datetime import datetime
import json
import random
import time
from flask import Blueprint, Response, request, render_template, url_for, flash, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_user, login_required, logout_user
#from account_requests import bot
from app.models import User
from app.extensions import db
from bars import Bars
from ta import Ta

main = Blueprint('main', __name__)
#alpaca = bot()
bars = None
ta = None

# am unsure if more validation is required (probably for password)
# need to render templates
@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists!")
            return render_template('register.html')
        username = request.form.get('username')
        user = User.query.filter_by(username=username).first()
        if user:
            flash("Username already exists!")
            return render_template('register.html')
        password = request.form.get('password')
        new_user = User(email=email, username=username, password=generate_password_hash(password, method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('main.login'))
    else:
        return render_template('register.html')
    

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password.strip()):
           flash('Incorrect username or password!')
           return render_template('login.html')# ideally, don't refresh username
        
        login_user(user)
        # need to change this for later
        
        # brings user to selection screen if they haven't chosen anything yet
        if not user.portfolio or not user.indicators or not user.active:
            return redirect(url_for('main.setup'))
        global bars
        bars = Bars(json.loads(user.portfolio), json.loads(user.active))
        return redirect(url_for('main.index'))
    return render_template('login.html')
        
@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

# will contain a generic home page that introduces the site and asks the user to login if not already
@main.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('main.login'))
    if not current_user.portfolio or not current_user.indicators:
        return redirect(url_for('main.setup'))
    return render_template('index.html')

    #user = current_user
    #if user:
    #    if not user.portfolio or not user.indicators:
    #        return redirect(url_for('main.setup'))
    #return render_template('index.html')

@main.route("/chart-data")
def chart_data():
    user = current_user
    # instantiates bars and ta if they still don't exist
    global bars, ta
    if bars is None:
        bars = Bars(json.loads(user.portfolio), json.loads(user.active))
    if ta is None:
        ta = Ta(json.loads(user.active))
    bars.get_response()
#   ta.execute('rsi_ema')
    def generate_random_data():
        while True:
            json_data = json.dumps(
                {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'value': random.random() * 100}
            )
            yield f"data:{json_data}\n\n"
            time.sleep(1)
    def generate_stock_data():
        with open('account_value.txt', "r") as csvfile:
            r = csv.reader(csvfile, delimiter=',')
            tickers = []
            for i, line in enumerate(r):
                if i == 0:
                    tickers = line[:]
                    json_data = json.dumps(tickers)
                    yield f"data:{json_data}\n\n"
                else:
                    
                    line_data = line #line.split(',')
                    print(line_data[0])
                    json_data = json.dumps(
                        #{'time': datetime.strptime(line_data[0], '%Y-%m-%dT%H:%M:%SZ'), 'values': json.dumps(line_data[1])}
                        #{'time': line_data[0], 'values': json.dumps(line_data[1])}
                        {'value': line_data[0]}
                    )
                    yield f"data:{json_data}\n\n"
                    print("getting")
                    time.sleep(1)
    
    return Response(generate_stock_data(), mimetype='text/event-stream')

@main.route("/setup")
@login_required
def setup():
    # account_value.txt, out.txt
    with open('nasdaq_tickers.csv', 'r') as f:
        r = csv.reader(f, delimiter=',')
        tickers = []
        for i, line in enumerate(r):
            if i != 0:
                tickers.append(line[0])
    data = {'tickers': json.dumps(tickers)}
            
    return render_template('setup.html', data=data)

@main.route("/submit", methods=['GET', 'POST'])
@login_required
def submit():
    user = current_user
    if user:
        # will definitely need a lot more validation
        active_stocks = request.form.get('myTickers', '')
        #prev_historical = json.load(user.historical)
        active_stocks_arr = json.loads(active_stocks)
        prev_portfolio = user.portfolio

        if not prev_portfolio:
            prev_portfolio = {}
        else:
            prev_portfolio = json.loads(prev_portfolio)
        prev_portfolio_keys = prev_portfolio.keys()
        
        for active_stock in active_stocks_arr:
            if active_stock not in prev_portfolio_keys:
                prev_portfolio[active_stock] = 0.0
                
        user.portfolio = json.dumps(prev_portfolio)
        user.active = active_stocks
        print(json.dumps(prev_portfolio))
        #user.historical = json.dumps(prev_historical)
        user.indicators = request.form.get('strat', '')
        db.session.commit()
        global bars, ta
        bars = Bars(json.loads(user.portfolio), json.loads(user.active))
        ta = Ta(user.active)
        # change to index for prod
        #return redirect(url_for('main.setup'))
        return redirect(url_for('main.index'))
    else:
        # should come up with better way to handle user not found
        return redirect(url_for('main.login'))
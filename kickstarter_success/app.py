"""Main app/routing file for Twitoff"""
from os import getenv
from flask import Flask, render_template, request
from .models import DB, User
from .twitter import add_or_update_user, update_all_users
from .prediction import predict_user
# h


def create_app():
    """Creating and configuring an instance of the Flask"""
    app = Flask(__name__)
    
    app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    DB.init_app(app)

    @app.route('/')
    def root():
        # renders base.html template and passes down title and users
        return render_template('base.html',title="Home", users=User.query.all())
    
    @app.route('/compare', methods=['POST'])
    def compare():
        user0, user1 = sorted([request.values['user1'], request.values['user2']])
        if user0 == user1:
            message = "Cannot compare users to themselves!"
        else:
            prediction = predict_user(user0, user1, request.values['tweet_text'])
            message = '{} is more likely to be said by {} than {}.'.format(
                request.values["tweet_text"], user1 if prediction else user0,
                user0 if prediction else user1
            )

        return render_template('predictions.html', title="Prediction", message=message)
    
    @app.route('/user', methods=["POST"])
    @app.route('/user/<name>',methods=["GET"])
    def user(name=None, message=''):
        name = name or request.values["user_name"]
        try:
            if request.method == "POST":
                add_or_update_user(name)
                message = "User {} was succsessfully added.".format(name)
            
            tweets = User.query.filter(User.name == name).one().tweets
        except Exception as e:
            message = "Error adding {}: {}".format(name, e)
            tweets = []
        
        return render_template("user.html",title=name, tweets=tweets, message=message)
    @app.route('/update')  # http://127.0.0.1:5000/update
    def update():
        update_all_users()
        insert_example_users()
        return render_template('base.html', title="Home", users=User.query.all())

    @app.route('/reset')  # http://127.0.0.1:5000/reset
    def reset():
        # we must create the database
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title="Home")
    
    @app.route('/add',methods=["POST"])
    def add_user():
        if request.method == "POST":
            username = request.form['text']
            add_or_update_user(username)
        return render_template('base.html',title="Home")
    return app

def insert_example_users():
    add_or_update_user('elonmusk')
    add_or_update_user('nasa')


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)
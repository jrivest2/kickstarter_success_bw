"""Main app/routing file for Twitoff!"""

# import flask
from flask import Flask, render_template, request
# from .models import DB, User, Tweet
# from .twitter import insert_example_users, add_or_update_user
from os import getenv
from .predict import predict_success


def create_app():
    app = Flask(__name__,static_folder='./static')
    # making the database for the API so we can reference
    app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # initializes the database within our app
    # DB.init_app(app)
    # DB.create_all()

    # TODO make the app

    # listens for path '/' and executes function when heard
    @app.route('/')
    def root():
        # a SELECT * query (in SQLAlchemy form)
        # users = User.query.all()
        # insert_example_users()
        # rendering template that we created passing Home to template
        return render_template('base.html', title='Home Page')


    @app.route('/predict', methods=['POST'])  # POST=changing something for the users
    def compare():

        # using request to access user input(variables referenced in the html file)
        
        prediction = predict_success(request.values['project_name'],request.values['project_desc'])
        return render_template('prediction.html', title='Prediction', message=prediction)

    return app


# if __name__=='__main__':
#     app.run()
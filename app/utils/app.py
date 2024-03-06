from flask import render_template
from init import create_app, db

# Create the Flask app using the application factory
app = create_app()

# Define a route for the homepage or landing page
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

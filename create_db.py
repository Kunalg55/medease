from models import db # Import the app and db from your main application file

# Use the application context to create the database tables
with app.app_context():
    db.create_all()
    print("Database tables created successfully in medease.db")

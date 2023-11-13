from main import create_app
import os 
from main import db

# Calling the function create app
app = create_app()

# Activate the application context
app.app_context().push()

if __name__ == "__main__":
    # Database creation
    db.create_all()
    # Application execution
    app.run(debug=True, port=os.getenv("PORT"))
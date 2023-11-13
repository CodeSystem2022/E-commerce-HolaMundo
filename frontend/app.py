from main import create_app
import os
from dotenv import load_dotenv

# Cargo las variables de entorno
load_dotenv()

# Configuro las variables de entorno
app = create_app()
app.static_folder = 'static'

app.app_context().push()

if __name__ == '__main__':
    app.run(debug = True , port = os.getenv("PORT"))
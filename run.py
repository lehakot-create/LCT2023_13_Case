from app import app
from app.database import init_db


init_db()
app.run(debug=True)
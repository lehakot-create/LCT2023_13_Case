from __init__ import app
# import app
from database import init_db


init_db()
app.run(debug=True,
        host='0.0.0.0',
        port=8000)

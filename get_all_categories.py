from webapp import create_app
from webapp.categories import get_categories

app = create_app()
with app.app_context():
    get_categories()


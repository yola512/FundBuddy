from website import create_app
from website.templates.authentication import auth_bp

app = create_app()

if __name__ == '__main__':
    app.run(debug = True) 


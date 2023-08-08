# within folder named "website" import function defined "create_app"
from website import create_app

#if
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

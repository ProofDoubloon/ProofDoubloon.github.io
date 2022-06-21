from website import create_app
from website import db


app = create_app()
@app.before_first_request


def create_tables():
    db.create_all()
 
if __name__ == '__main__':

    app.run(debug=True)

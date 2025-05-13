from app import create_app
from app.routes import stats 

app = create_app()
 

if __name__ == '__main__':
    app.run(debug=True, port=5001)

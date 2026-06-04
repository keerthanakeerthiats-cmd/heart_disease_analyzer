from flask import Flask, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test():
    return {'status': 'working', 'message': 'Website is running!'}

if __name__ == '__main__':
    print("=" * 60)
    print("Starting Basic Test Server...")
    print("=" * 60)
    print("\nIf you see this, Python and Flask are working!")
    print("\nOpen browser to: http://localhost:5000")
    print("\nPress Ctrl+C to stop")
    print("=" * 60)
    print()
    
    app.run(debug=True, host='0.0.0.0', port=5000)

from flask import Flask, render_template, request
import pandas as pd
from recommendation_system import RecomendationSystem
from ContentBaseFiltering import content_base_filtering

app = Flask(__name__)

# Load data 
data = "/home/reyhan/RecomApp/demographic.csv"  
test_system = RecomendationSystem(data)

content_data = "/home/reyhan/RecomApp/content_by_multiple.csv"  
content_system = content_base_filtering(content_data, content_col="metadata")
content_system.fit()  

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommendations', methods=['GET'])
def get_recommendations():
    # Retrieve parameters 
    genre = request.args.get('genre')
    duration = request.args.get('duration')
    year = request.args.get('year')
    method = request.args.get('method')

    # Parameter parsing 
    genre = genre.split(', ') if genre else None
    duration = tuple(map(int, duration.split('-'))) if duration else None
    year = tuple(map(int, year.split('-'))) if year else None

    if method == "demographic":
        recommendations = test_system.recommendation(genre=genre, duration=duration, year=year)
    elif method == "content":
        favorite_movie = request.args.get('title')
        recommendations = content_system.recommend(title=favorite_movie)
    else:
        recommendations = pd.DataFrame()

    recommendations.insert(0, 'No', range(1, len(recommendations) + 1))
    recommendations_html = recommendations.to_html(index=False, border=0)
    return render_template('recommendations.html', table=recommendations_html)

if __name__ == '__main__':
    app.run(debug=True, host='192.168.0.20')


from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# The URL to scrape
url = "https://timesofindia.indiatimes.com/"

@app.route('/news', methods=['GET'])
def get_news():
    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content
    Parsecontenet = BeautifulSoup(response.content, 'html.parser')

    # Initialize a list to hold the articles
    articles = []

    alltagdata = Parsecontenet.find_all('figure', class_='_YVis')

    # Find all article elements
    for figure in alltagdata:
        # Attempt to find the article link
        link_tag = figure.find('a')
        if link_tag:  # Check if the link exists
            link = link_tag.get('href')  # Use get to avoid KeyError
        else:
            continue  # Skip this figure if there's no link

        # Attempt to find the article title
        title_tag = figure.find('figcaption')
        if title_tag:  # Check if the title exists
            title = title_tag.text.strip()
        else:
            title = "No title available"  # Default title if not found

        # Attempt to find the article image source
        img_tag = figure.find('img')
        if img_tag:  # Check if the image exists
            img = img_tag.get('src')  # Use get to avoid KeyError
        else:
            img = "No image available"  # Default image if not found

        # Append the article information to the list
        articles.append({
            'title': title,
            'link': link,
            'image': img
        })

    # Return the articles as JSON
    return jsonify(articles)

if __name__ == '__main__':
    app.run()  # No debug=True, use gunicorn in production

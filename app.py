from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# The URL to scrape
url = "https://timesofindia.indiatimes.com/"

@app.route('/news', methods=['GET'])
def get_news():
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses

        # Parse the HTML content
        Parsecontenet = BeautifulSoup(response.content, 'html.parser')

        # Initialize a list to hold the articles
        articles = []

        alltagdata = Parsecontenet.find_all('figure', class_='_YVis')

        # Find all article elements
        for figure in alltagdata:
            # Attempt to find the article link
            link_tag = figure.find('a')
            if link_tag:
                link = link_tag.get('href')
            else:
                continue

            # Attempt to find the article title
            title_tag = figure.find('figcaption')
            if title_tag:
                title = title_tag.text.strip()
            else:
                title = "No title available"

            # Attempt to find the article image source
            img_tag = figure.find('img')
            if img_tag:
                img = img_tag.get('src')
            else:
                img = "No image available"

            # Append the article information to the list
            articles.append({
                'title': title,
                'link': link,
                'image': img
            })

        # Return the articles as JSON
        return jsonify(articles)

    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500  # Return error as JSON

if __name__ == '__main__':
    app.run(debug=True)

import random
import requests
from bs4 import BeautifulSoup as bs
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import time
from scraper_api import ScraperAPIClient
def sentiment_scores(review):
    global countPositive
    global countNegative
    global countNeutral
    sid_obj = SentimentIntensityAnalyzer()
    sentiment_dict = sid_obj.polarity_scores(review)
    print(f"\nOverall sentiment dictionary is: ", sentiment_dict)
    print(f"Review was rated as {sentiment_dict['neg'] * 100:.4f} % Negative")
    print(f"Review was rated as {sentiment_dict['neu'] * 100:.4f} % Neutral")
    print(f"Review was rated as {sentiment_dict['pos'] * 100:.4f} % Positive")
    print("\nReview Overall Rated As", end = " ")
    if sentiment_dict['compound'] >= 0.05:
        countPositive += 1
        print("Positive")
    elif sentiment_dict['compound'] <= -0.05:
        countNegative += 1
        print("Negative")
    else:
        countNeutral += 1
        print("Neutral")
def avg_sentiment(wm_content):
    sid = SentimentIntensityAnalyzer()
    positive_scores = []
    negative_scores = []
    neutral_scores = []
    for review in wm_content:
        sentiment_scores = sid.polarity_scores(review)
        positive_scores.append(sentiment_scores['pos'])
        negative_scores.append(sentiment_scores['neg'])
        neutral_scores.append(sentiment_scores['neu'])
    # print(f"\nOverall  : ", sentiment_scores)
    # print(f"Overall Negative : {(sum(negative_scores) / len(negative_scores)) * 100:.4f} %")
    # print(f"Overall Neutral : {(sum(neutral_scores) / len(neutral_scores)) * 100:.4f} %")
    # print(f"Overall Positive : {(sum(positive_scores) / len(positive_scores)) * 100:.4f} %")
    print("\nAverage Rated As", end = " ")
    if sentiment_scores['compound'] >= 0.05:
        print("Positive\nMost buyers like this product.")
    elif sentiment_scores['compound'] <= - 0.05:
        print("Negative\nMost buyers don't like this product.")
    else:
        print("Neutral\nSome buyers like this product while others don't.")
if __name__ == "__main__":
    countPositive = 0
    countNegative = 0
    countNeutral = 0
    API_KEY = ""
    client = ScraperAPIClient(API_KEY)
    # lnk = input("Enter the Amazon product review link: ")
    # n = int(input("Enter the number of pages: "))
    lnk = "https://www.amazon.in/Redmi-Note-11T-5G-Dimensity/product-reviews/B09LHX1YFX/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"
    n = 2
    wm_content = []
    for i in range(1, n + 1):
        try:
            link = f"http://api.scraperapi.com?api_key={API_KEY}&render=true&url={lnk}&pageNumber={i}"
            response = requests.get(link)
            if response.status_code != 200:
                print(f"Failed to fetch page {i}, status code: {response.status_code}")
                continue
            delay_seconds = 2 + 2 * random.random()
            print(f"Delaying for {delay_seconds:.2f} seconds...")
            time.sleep(delay_seconds)
            print("")
            soup = bs(response.content, "html.parser")
            review = soup.find_all("span", {"data-hook": "review-body"})
            br_tags = soup.find_all('br')
            for br_tag in br_tags:
                br_tag.replace_with('\n')
            review_content = []
            for j in range(0, len(review)):
                review_content.append(review[j].get_text())
            review_content[:] = [reviews.lstrip('\n') for reviews in review_content]
            review_content[:] = [reviews.rstrip('\n') for reviews in review_content]
            wm_content.extend(review_content)
            for review_text in review_content:
                print(review_text)
                sentiment_scores(review_text)
                print("=" * 50)
            '''if i == n:
                print("#" * 50)
                print(f"Number of reviews: {len(wm_content)}")
                print(f"Number of Positive Reviews: {countPositive}")
                print(f"Number of Negative Reviews: {countNegative}")
                print(f"Number of Neutral Reviews: {countNeutral}")
                avg_sentiment(wm_content)
                print("#" * 50)'''
        except Exception as e:
            print(f"An error occurred: {e}")
    print("#" * 50)
    print(f"Number of reviews: {len(wm_content)}")
    print(f"Number of Positive Reviews: {countPositive}")
    print(f"Number of Negative Reviews: {countNegative}")
    print(f"Number of Neutral Reviews: {countNeutral}")
    avg_sentiment(wm_content)
    print("#" * 50)
import tweepy
import time
from feedback.models import CustomerFeedback
from analysis.sentiment import analyze_sentiment
import os

# Your Bearer Token from environment variable
BEARER_TOKEN = os.environ.get('BEARER_TOKEN')

# Step 1: Initialize Tweepy client (no session param)
client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    wait_on_rate_limit=True
)

# Step 2: Tweet fetch function with manual retry and timeout logic
def fetch_tweets(query="#feedback", max_results=10, retries=3):
    attempt = 0
    while attempt < retries:
        try:
            response = client.search_recent_tweets(
                query=query,
                tweet_fields=['author_id', 'created_at'],
                max_results=max_results
            )

            if not response.data:
                print("No tweets found.")
                return

            for tweet in response.data:
                message = tweet.text
                username = f"user_{tweet.author_id}"
                sentiment = analyze_sentiment(message)

                CustomerFeedback.objects.create(
                    message=message,
                    username=username,
                    platform='Twitter',
                    sentiment=sentiment
                )

            print("Tweets fetched and saved successfully.")
            return

        except tweepy.errors.TooManyRequests as e:
            # Handle rate limits
            print(f"Rate limit hit: sleeping for 15 minutes")
            time.sleep(15 * 60)
        except tweepy.TweepyException as e:
            print(f"Tweepy error: {e}")
            break
        except Exception as e:
            attempt += 1
            print(f"Error occurred (attempt {attempt}/{retries}): {e}")
            time.sleep(2)


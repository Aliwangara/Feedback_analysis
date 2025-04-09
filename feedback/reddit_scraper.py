import praw
from django.conf import settings
from .models import CustomerFeedback
from analysis.sentiment import analyze_sentiment  # Assuming you have this function defined




def fetch_reddit_comments():
    reddit = praw.Reddit(
        client_id=settings.REDDIT_CLIENT_ID,
        client_secret=settings.REDDIT_CLIENT_SECRET,
        user_agent=settings.REDDIT_USER_AGENT
    )

    subreddit = reddit.subreddit("streetwear")  # Or any subreddit you're interested in
    comments = subreddit.comments(limit=10)

    for comment in comments:
        text = comment.body
        sentiment = analyze_sentiment(text)
        CustomerFeedback.objects.get_or_create(
            message=text,
            platform="Reddit",
            username=str(comment.author),
            sentiment=sentiment
        )

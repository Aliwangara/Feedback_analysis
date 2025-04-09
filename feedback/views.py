from django.shortcuts import render, redirect
from .forms import CustomerFeedbackForm
from analysis.sentiment import analyze_sentiment
import plotly.graph_objs as go
from django.db.models import Count
from .models import CustomerFeedback
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from feedback.twitter_scraper import fetch_tweets
from feedback.reddit_scraper  import fetch_reddit_comments
from django.utils import timezone

# Create your views here.
def home(request):
    return render(request, 'home.html')





def submit_feedback(request):
    if request.method == 'POST':
        form = CustomerFeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.sentiment = analyze_sentiment(feedback.message)  # <-- Analyze before saving
            feedback.save()
            return redirect('thank_you')
    else:
        form = CustomerFeedbackForm()
    return render(request, 'submit.html', {'form': form})

def thank_you(request):
    return render(request, 'thank_you.html')

def dashboard(request):
    # Sentiment Distribution
    sentiment_data = CustomerFeedback.objects.values('sentiment').annotate(count=Count('sentiment'))
    labels = [(entry['sentiment'] or 'Unknown').capitalize() for entry in sentiment_data]
    values = [entry['count'] for entry in sentiment_data]

    # Platform Distribution
    platform_data = CustomerFeedback.objects.values('platform').annotate(count=Count('platform'))
    platform_labels = [(entry['platform'] or 'Unknown').capitalize() for entry in platform_data]
    platform_values = [entry['count'] for entry in platform_data]

    # Stats
    total_feedback = CustomerFeedback.objects.count()
    neutral_count = CustomerFeedback.objects.filter(sentiment='neutral').count()
    negative_count = CustomerFeedback.objects.filter(sentiment='negative').count()

    # Comments list
    comments = CustomerFeedback.objects.all().order_by('-submitted_at')[:10]

    return render(request, 'dashboard.html', {
        'labels': labels,
        'values': values,
        'platform_labels': platform_labels,
        'platform_values': platform_values,
        'comments': comments,
        'total_feedback': total_feedback,
        'neutral_count': neutral_count,
        'negative_count': negative_count
    })


@csrf_exempt
def fetch_twitter_view(request):
    if request.method == 'POST':
        try:
            fetch_tweets(query="#feedback", max_results=10)  # Customize as needed
            return JsonResponse({"message": "Tweets fetched successfully!"})
        except Exception as e:
            return JsonResponse({"message": f"Error fetching tweets: {str(e)}"}, status=500)
    return JsonResponse({"message": "Invalid request method"}, status=405)

def fetch_reddit(request):
    fetch_reddit_comments()
    return redirect('dashboard')


def all_comments(request):
    comments = CustomerFeedback.objects.all().order_by('-submitted_at')
    return render(request, 'all_comments.html', {'comments': comments})


def statistics_report(request):
    sentiment_data = CustomerFeedback.objects.values('sentiment').annotate(count=Count('sentiment'))
    platform_data = CustomerFeedback.objects.values('platform').annotate(count=Count('platform'))

    sentiment_distribution = [((entry['sentiment'] or 'Unknown').capitalize(), entry['count']) for entry in sentiment_data]
    platform_distribution = [((entry['platform'] or 'Unknown').capitalize(), entry['count']) for entry in platform_data]

    total_feedback = CustomerFeedback.objects.count()
    neutral_count = CustomerFeedback.objects.filter(sentiment='neutral').count()
    negative_count = CustomerFeedback.objects.filter(sentiment='negative').count()

    return render(request, 'statistics_report.html', {
        'now': timezone.now(),
        'sentiment_distribution': sentiment_distribution,
        'platform_distribution': platform_distribution,
        'total_feedback': total_feedback,
        'neutral_count': neutral_count,
        'negative_count': negative_count,
    })




 
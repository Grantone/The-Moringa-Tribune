from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
import datetime as dt
from .models import Article
from .forms import NewsLetterForm
from .email import send_welcome_email

# Create your views here.


def welcome(request):
    return render(request, 'welcome.html')
    # return HttpResponse('Welcome to the Moringa Tribune')


def news_today(request):
    date = dt.date.today()
    news = Article.todays_news()

    if request.method == 'POST':
        form = NewsLetterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['your_name']
            email = form.cleaned_data['email']
            recipient = NewsLetterRecipients(name=name, email=email)
            recipient.save()
            send_welcome_email(name, email)

            HttpResponseRedirect('news_today')
            # print('valid')
    else:
        form = NewsLetterForm()
        return render(request, 'all-news/today-news.html', {"date": date, "news": news, "form": form})


def convert_dates(dates):

    # Function that gets the weekday number for the date.
    day_number = dt.date.weekday(dates)

    days = ['Monday', 'Tuesday', 'Wednesday',
            'Thursday', 'Friday', 'Saturday', "Sunday"]

    # Returning the actual day of the week

    day = days[day_number]
    return day


def past_days_news(request, past_date):
    # Converts data from the string url

    try:

        date = dt.datetime.strptime(past_date, '%Y-%m-%d').date()

    except ValueError:
        # Raise 404 error when ValueError is thrown
        raise Http404()
        assert False

    if date == dt.date.today():
        return redirect(news_today)

    return render(request, 'all-news/past-news.html', {"date": date, "news": news})

    # day = convert_dates(date)
    # html = f'''
    #     <html>
    #         <body>
    #             <h1>News for {day} {date.day}-{date.month}-{date.year}</h1>
    #         </body>
    #     </html>
    #         '''
    # return HttpResponse(html)


def news_today(request):
    date = dt.date.today()
    news = Article.todays_news()
    return render(request, 'all-news/today_news.html', {"date": date, "news": news})


def search_results(request):
    if 'article' in request.GET and request.GET["article"]:
        search_term = request.GET.get("article")
        searched_articles = Article.search_by_title(search_term)
        message = f"{search_term}"

        return render(request, 'all-news/search.html', {"message": message, "articles": searched_articles})

    else:
        message = "You haven't searched for any term"
        return render(request, 'all-news/search.html', {"message": message})


def article(request, article_id):
    try:
        article = Article.objects.get(id=article_id)
        tags = article.tags.all()
    except DoesNotExist:
        raise Http404()
    return render(request, "all-news/article.html", {"article": article, "tags": tags})

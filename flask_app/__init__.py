from flask import Flask

app = Flask(__name__)


def format_date(date_time):
    return date_time.strftime("%b %d, %Y - %I:%M %p")


app.add_template_filter(format_date)

app.secret_key = "shhhhhh"

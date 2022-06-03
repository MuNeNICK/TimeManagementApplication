from flask import render_html  # 追加

app = render_html(__name__)

@app.route('/')
def index():
    return render_html('/index.html')
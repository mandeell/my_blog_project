import requests, smtplib, os, ssl
from flask import Flask, render_template, request
from email.mime.text import MIMEText
from dotenv import load_dotenv

app = Flask(__name__)

blog_url = 'https://api.npoint.io/50950d92e830b2c583d1'
posts = requests.get(url=blog_url).json()

load_dotenv()
my_email = os.getenv("MY_EMAIL")
to_email_address = os.getenv("TO_EMAIL")
my_password = os.getenv("MY_PASSWORD")


context = ssl.create_default_context()



@app.route('/')
def home():
    return render_template('index.html', all_posts=posts)

@app.route('/about')
def about_page():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact_page():
    if request.method == 'POST':
        content = (f'Name: {request.form['name']}\nEmail: {request.form['email']}'
                   f'\n Phone Number: {request.form['phone']}\nMessage: {request.form['message']}')
        msg = MIMEText(content, "plain", "utf-8")
        msg['Subject'] = "Blog Contact Form"
        msg['From'] = my_email
        msg['To'] = to_email_address
        print(f'{request.form['name']}\n{request.form['email']}'
              f'\n{request.form['phone']}\n{request.form['message']}')
        with smtplib.SMTP_SSL("smtp.gmail.com", 465,context=context, timeout=50) as connection:
            # connection.starttls()
            connection.login(user=my_email, password=my_password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs=to_email_address,
                msg=msg.as_string()
            )
        print("Email sent successfully!")

    return render_template('contact.html')

@app.route('/post/<int:index>')
def blog_page(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template('post.html', all_posts=posts, post=requested_post)


if __name__ == '__main__':
    app.run()

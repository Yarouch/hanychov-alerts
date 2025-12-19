import feedparser
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Parse RSS feed
feed = feedparser.parse('http://www.liberec.cz/rss/uredni_deska.atom')
hanychov_items = []

for entry in feed.entries[:10]:  # Check last 10 items
    if any(keyword in (entry.title + entry.summary).lower() for keyword in ['hanychov', 'horní hanychov']):
        hanychov_items.append({
            'title': entry.title,
            'link': entry.link,
            'date': entry.get('published', 'No date'),
            'summary': (entry.summary or '')[:200] + '...'
        })

# Send email if matches found
if hanychov_items:
    msg = MIMEMultipart()
    msg['From'] = os.getenv('GMAIL_USER')
    msg['To'] = os.getenv('GMAIL_USER')
    msg['Subject'] = f'Horní Hanychov Alert: {len(hanychov_items)} new items'
    
    body = '\n'.join([
        f"• {item['title']} ({item['date']})\nLink: {item['link']}\nSummary: {item['summary']}\n{'-'*50}"
        for item in hanychov_items
    ])
    msg.attach(MIMEText(body, 'plain'))
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(os.getenv('GMAIL_USER'), os.getenv('GMAIL_APP_PASS'))
    server.send_message(msg)
    server.quit()
    print(f"Sent {len(hanychov_items)} alerts")
else:
    print("No new Hanychov items found")

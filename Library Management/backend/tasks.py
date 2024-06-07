import requests
from app import celery, cache
from datetime import datetime, timedelta, date
from application.models import User, UserBook, Section, Book, Feedback  # Update with the correct paths for your models
from application.database import db
from jinja2 import Template
import os
import csv
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib import colors
from mail_config import send_email
from reportlab.lib.styles import ParagraphStyle

# Other imports and setup code remain unchanged

@celery.on_after_finalize.connect
def setup_intervalTASK(sender, **kwargs):
    sender.add_periodic_task(
        10,  # Execute task every 10 seconds
        send_reminder_webhooks.s(),
        name="Daily reminder"
    )

    sender.add_periodic_task(
        10,  # Execute task every 10 seconds
        send_monthly_reports.s(),
        name="Monthly Report"
    )

@celery.task(name='tasks.send_reminder_webhooks')
def send_reminder_webhooks():
    yesterday = datetime.now() - timedelta(days=1)
    inactive_users = User.query.filter(User.lastAct < yesterday).all()
    
    for user in inactive_users:
        if user.lastAct is None:
            continue  # Skip users without activity data
        
        webhook_url = "https://chat.googleapis.com/v1/spaces/AAAAfxSdsPU/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=l1ql-vNZR2ptcsPrGgD7yDphlvQt1ER18cX_sPL4W3s"  # Update with your actual webhook URL
            
        payload = {
            "text": f"{user.username} Please visit our site, Happy Reading!",
        }
        
        response = requests.post(webhook_url, json=payload)
        print(response.status_code)
        if response.status_code == 200:
            print("Success")

@celery.task()
def send_monthly_reports():
    print("cstart")
    users = User.query.all()
    for user in users:
        if user.username == 'admin':
            pass
        user_books = UserBook.query.filter_by(user_id=user.username).all()
        print(user_books)
        if len(user_books) == 0:
            pass
        print('hi1')
        month = date.today().strftime("%B")
        e = user.email
        u = {'logged': user.lastAct, 'email': e}
        u['username'] = user.username

        filepath = f"static/monthly_reports/monthly_report_{str(u['username'])}.pdf"
        print('hi2')
        if not os.path.exists('static/monthly_reports/'):
            os.mkdir(path='static/monthly_reports/')

        with open(r"templates/monthly_report.html") as file:
            msg_template = Template(file.read())
        with open(r"templates/pdf.html") as file:
            pdf_template = Template(file.read())  # Load pdf.html template

        booking_info_text = []
        for user_book in user_books:
            book = Book.query.get(user_book.book_id)
            section = Section.query.get(book.section_id)
            booking_info = {
                'bookingID': user_book.id,
                'bookName': book.name,
                'sectionName': section.name,
                'issueDate': user_book.issue_date.strftime("%Y-%m-%d"),
                'dueDate': user_book.due_date.strftime("%Y-%m-%d"),
                'status': user_book.status
            }
            booking_info_text.append(booking_info)
        print('hi3')
        booking_info = booking_info_text

        doc = SimpleDocTemplate(filepath, pagesize=letter)
        elements = []

        elements.append(Paragraph(f"Monthly Report for {month}", ParagraphStyle(name='Title')))
        elements.append(Paragraph(f"Username: {u['username']}", ParagraphStyle(name='Normal')))
        elements.append(Paragraph(f"Email: {u['email']}", ParagraphStyle(name='Normal')))
        elements.append(Paragraph("\n", ParagraphStyle(name='Normal')))

        table_data = [
            ["S.no", "Book Name", "Section Name", "Issue Date", "Due Date", "Status"],
            *[[booking['bookingID'], booking['bookName'], booking['sectionName'], booking['issueDate'],
                booking['dueDate'], booking['status']] for booking in booking_info]
        ]
        print('hi4')
        # Specify column widths as integers
        table = Table(table_data, colWidths=[50, 250, 90, 70, 70, 50], rowHeights=20)
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                   ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                                   ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                   ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                   ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                   ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                   ('GRID', (0, 0), (-1, -1), 1, colors.black)]))

        elements.append(table)
        doc.build(elements)
        print('hi5')
        send_email(to=e, subject="Monthly report", attachment=filepath, msg=pdf_template.render(user=u, month=month, booking_info=booking_info))
    return 'success'

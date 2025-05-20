from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import csv
import os
 
app = Flask(__name__)
 
user_sessions = {}
 
COUNTRIES = ['Togo', 'Benin', 'Kenya', 'Rwanda', 'Uganda', 'Tanzania', 'Cameroon', 'Other']
DEPARTMENTS = ['IOT S/W', 'IOT H/W', 'Athena/Atlas', 'Field Ops', 'Payments', 'Swap Station/ Energy Services', 'Sales', 'Delivery', 'Immobilization','Other']
PRIORITIES = ['P0 – Super Urgent (Instant Response)', 'P1 – Urgent (Response within 1 hour)', 'P2 – Response by End of Day (EOD)', 'P3 – Respond by next day']
 
DEPARTMENT_EMAILS = {
    'IOT S/W': 'naman.singh2402@gmail.com',
    'IOT H/W': 'naman.singh2402@gmail.com',
    'Athena/Atlas': 'naman.singh2402@gmail.com',
    'Field Ops': 'naman.singh2402@gmail.com',
    'Payments': 'naman.singh2402@gmail.com',
    'Swap Station/ Energy Services': 'naman.singh2402@gmail.com',
    'Sales': 'naman.singh2402@gmail.com',
    'Delivery': 'naman.singh2402@gmail.com',
    'Immobilization': 'naman.singh2402@gmail.com',
    'Other': 'naman.singh2402@gmail.com'
}
 
EMAIL_SENDER = 'namanspiro@gmail.com'
EMAIL_PASSWORD = "mjqqnhpxxnzvxdxa"
 
CSV_FILE = 'chatbot\help_center_issues.csv'
 
@app.route('/webhook', methods=['POST'])
def whatsapp_webhook():
    incoming_msg = request.values.get('Body', '').strip()
    user = request.values.get('From', '')
    
    user = user.replace('whatsapp:', '') if 'whatsapp:' in user else user
   
    resp = MessagingResponse()
    msg = resp.message()
 
    session = user_sessions.get(user, {'step':'hi'})
 
    if incoming_msg.lower() == 'hi':
        session = {'step': 'country'}
        msg.body("Welcome to Spiro Help Center! Please select your Country: \n" + format_options(COUNTRIES))
 
    elif session['step'] == 'country':
        if incoming_msg.isdigit() and 1 <= int(incoming_msg) <= len(COUNTRIES):
            selected = COUNTRIES[int(incoming_msg) - 1]
            if selected.lower() == 'other':
                msg.body("Please type the Country you belong to: ")
                session['step'] = 'custom_country'
            else:
                session['country'] = selected
                msg.body('Which Department does this problem belong to?\n' + format_options(DEPARTMENTS))
                session['step'] = 'department'
        else:
            msg.body("Invalid input. Please select a country: \n" + format_options(COUNTRIES))
 
    elif session['step'] == 'custom_country':
        session['country'] = incoming_msg
        msg.body('Which Department does this problem belong to?\n' + format_options(DEPARTMENTS))
        session['step'] = 'department'
 
    elif session['step'] == 'department':
        if incoming_msg.isdigit() and 1 <= int(incoming_msg) <= len(DEPARTMENTS):
            selected = DEPARTMENTS[int(incoming_msg) - 1]
            if selected.lower() == 'other':
                msg.body("Please type the Department's name: ")
                session['step'] = 'custom_department'
            else:
                session['department'] = selected
                msg.body("Please describe your query in detail.")
                session['step'] = "query"
        else:
            msg.body("Invalid input. Please select a department: \n" + format_options(DEPARTMENTS))
 
    elif session['step'] == 'custom_department':
        session['department'] = incoming_msg
        msg.body("Please describe your query in detail.")
        session['step'] = "query"
 
    elif session['step'] == 'query':
        session['problem'] = incoming_msg
        msg.body('Please select the Priority level:\n' + format_options(PRIORITIES))
        session['step'] = 'priority'
 
    elif session['step'] == 'priority':
        if incoming_msg.isdigit() and 1 <= int(incoming_msg) <= len(PRIORITIES):
            selected = PRIORITIES[int(incoming_msg) - 1]
            session['priority'] = selected
            store_issue(user, session)
            msg.body("Thank you! Your issue has been recorded and will be forwarded.")
            session['step'] = "completed"
        else:
            msg.body("Invalid input. Please select a priority level: \n" + format_options(PRIORITIES))
 
    elif session['step'] == 'completed':
        msg.body('You already submitted an issue. Type "hi" to start again')
 
    user_sessions[user] = session
    return str(resp)
 
def format_options(options):
    return "\n".join([f"{i+1}. {opt}" for i, opt in enumerate(options)])
 
def store_issue(user, session):
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode = 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Phone_no", "Country", "Department", "Problem", "Priority"])
 
    with open(CSV_FILE, mode = 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            user,
            session.get('country'),
            session.get('department'),
            session.get('problem'),
            session.get('priority')
        ])
 
    send_email_alert(user, session)
 
def send_email_alert(user, session):
    subject = f"[Help Center] New query from {session.get('country')}"
    to_email = DEPARTMENT_EMAILS.get(session.get('department'), DEPARTMENT_EMAILS.get('Other'))
 
    body = f"""
    New issue reported via WhatsApp Help Center:

        From: {user}
    Country: {session.get('country')}
    Department: {session.get('department')}
    Priority: {session.get('priority')}
    Problem:
    {session.get('problem')}
    """

    msg = MIMEMultipart()
    msg['From'] = EMAIL_SENDER
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, to_email, msg.as_string())
        print(f"Email sent to {to_email}")

    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == "__main__":
    app.run(port=5000)
from django.shortcuts import render
from icfn_new.settings import SENDGRID_API_KEY
from sendgrid.helpers.mail import To, Mail,ReplyTo,Email,Cc,Attachment, FileContent, FileName, FileType, Disposition
from sendgrid import SendGridAPIClient


def convert_safe_text(content):
	try:
		if type(content) != str:
			content = str(content)
	except:
		content = str(content.encode("utf8"))
	return content

#Main Function to send the mail using semgrid throughout the applicaion
def send_sandgridmail(sender,receiver,subject,content,reply_to=None,cc=None,attachment=None):
	content = convert_safe_text(content)
	# to_email = To(receiver)
	message = Mail(
		from_email=str(sender),
		to_emails=receiver,
		subject=str(subject),
		html_content=content)
	if reply_to:
		message.reply_to = ReplyTo(reply_to)
	if attachment:
		with open(attachment, 'rb') as f:
			data = f.read()
			f.close()
		encoded_file = base64.b64encode(data).decode()
		attachedFile = Attachment(
		FileContent(encoded_file),
		FileName('attachment.pdf'),
		FileType('application/pdf'),
		Disposition('attachment')
		)
		message.attachment = attachedFile

	if cc:
		cc_mail = []
		for cc_person in cc:
			cc_mail.append(Cc(cc_person,""))
		message.add_cc(cc_mail)
	try:
		sg = SendGridAPIClient(SENDGRID_API_KEY)
		response = sg.send(message)
		print(response.status_code)
		print(response.body)
		print(response.headers)
	except Exception as e:
		print(e.args[0])
	return response
	
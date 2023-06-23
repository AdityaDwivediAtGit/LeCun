f = open("webhook_url.txt", 'r')
webhook_url = f.read()
f.close()
print(webhook_url, type(webhook_url))
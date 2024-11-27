import requests
import schedule
import smtplib
import paramiko
import digitalocean as do
import os
import time
import sys
host_ip = "157.230.119.62"
webserver_url = f"http://{host_ip}:8080/"
DO_TOKEN = os.environ.get("DO_TOKEN")
EMAIL_ADDRESS =  os.environ.get("EMAIL_ADDRESS")
EMAIL_PASSWORD =  os.environ.get("EMAIL_PASSWORD")


def send_email_notification(msg):
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_ADRESS,EMAIL_PASSWORD)
        msg = f"Subject: Site DOWN\n {msg}"

def restart_server_and_application():
    manager = do.Manager(token=DO_TOKEN)
    nginx_droplet = manager.get_droplet(droplet_id="453045946")
    print("Rebooting droplet")
    nginx_droplet.reboot()
    
    while (True):
        time.sleep(10)
        nginx_droplet = manager.get_droplet(droplet_id="453045946")
        print(nginx_droplet.status)
        if nginx_droplet.status == "active":
            restart_application()
            break


#Restart application
def restart_application():
    #in case of a bad request response we restart the application by ssh-ing into the server and restarting the container
    #we do this using the paramiko library
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=host_ip, username="root", key_filename="/home/jonas/.ssh/id_rsa")
    stdin, stdout, stderr = ssh.exec_command("docker start c82a3959f7c3")
    print(stdout.readlines())
    ssh.close()

def monitor_application():
    try:
        response = requests.get(webserver_url)

        if response.status_code == 200:
            print("Application is up and running.")

        else:
            message = "Application is not running!"
            send_email_notification(msg=message)
            
    except Exception as error:
        send_email_notification(msg=f"Connection error happened {error}")
        restart_server_and_application()

schedule.every(20).seconds.do(monitor_application)

while True:
    schedule.run_pending()

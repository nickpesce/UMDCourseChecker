import urllib2
import smtplib
import sys
import time
from bs4 import BeautifulSoup
from email.mime.text import MIMEText

#check that correct num commands are given 
if len(sys.argv) < 3: 
    print "USAGE: " + sys.argv[0] + " course_code sections..." 
    sys.exit(2)

#Address's to send email to
receivers = !OMMITTED!
#Address that the email is sent from
sender = !OMMITTED!
#Password of the sender email
password = !OMMITTED!
#Course code to check for
course = sys.argv[1]
#Section numbers to check
sections = sys.argv[2:]
#List of sections that were already emailed about
already_emailed = []
#Current term code
term = "201608"
#Seconds to wait for
sleep_time = 60

#Url of course schedule
url = "https://ntst.umd.edu/soc/search?courseId="+course+"&sectionId=&termId="+term+"&courseStartCompare=&courseStartMin=&courseStartAM="

#Continuously check untill program is stopped by user
while(True):
    print "Checking status of " + course + " section(s) " + " ,".join(sections)
    try:
        soup = BeautifulSoup(urllib2.urlopen(url).read(), 'html.parser')
    except:
        print "Could not connect"
        pass
    #All of the tags that contain section ids on the page
    id_tags = soup.find_all("span", class_="section-id")
    #All of the tags that contain open seat counts
    open_tags = soup.find_all("span", class_="open-seats-count")
    for i in range(0, len(open_tags)):
        open_tag = open_tags[i]
        open = unicode(open_tag.string)
        if int(open) == 0:
            #Corresponding section number
            section = id_tags[i].string.strip()
            if section in sections and section not in already_emailed:
                #Make message
                body = "Link to add/drop:  https://ntst.umd.edu/testudo/main/dropAdd?venusTermId="+term+"&crslist=" + course + "/"+section + " . " + course + " section " + section + " has " + open + " spots open!\n"
                for receiver in receivers:
                    msg = MIMEText(body)
                    #set header
                    msg['Subject'] = "QUICKLY! There is an opening in " + course + "!"
                    msg['From'] = sender 
                    msg['To'] = receiver

                    #Send the email
                    s = smtplib.SMTP("smtp.gmail.com", 587)
                    s.ehlo()
                    s.starttls()
                    s.login(sender, password)
                    s.sendmail(sender, receiver, msg.as_string())
                    s.quit()
                already_emailed.append(section);
                print "Emailed " + " & ".join(receivers) + " becuase section " + section + " of " + course + " now has " + open + " spots."
            else:
                #If the section is full, it should be able to be emailed about again(If it was already emailed about)
                try:
                    already_emailed.remove(section)
                except ValueError:
                    pass
    #Wait, then check again
    time.sleep(sleep_time);

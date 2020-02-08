An Application, supposed to run on a Raspberry pi that routinely checks the
your Eltrnportal Account for updates in the "Vertretungsplan" section.

When detecting any updates / changes it then proceeds to send the changes to
all the emails specified in the email_list file.

To start the Application run the main.py file but not before installing the
following packages by pasting the command in your CMD / Terminal window:
! Install pip before proceeding !

requests:
sudo python3 -m pip install requests

bs4(BeautifulSoup):
sudo python3 -m pip install bs4

Specify your Settings in the settings.ini file

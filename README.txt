An Application, supposed to run on a Raspberry pi that routinely checks
your Eltrnportal Account for updates in the "Vertretungsplan" section.

When detecting any updates / changes it then proceeds to send the changes to
all the emails specified in the email_list file.

To start the Application follow these steps:

1. Install Python3
2. Install pip
3. Install requests and bs4 (BeautifulSoup) by pasting the following in your CMD / Terminal window:
   $ sudo python3 -m pip install requests
   $ sudo python3 -m pip install bs4
4. Specify your Settings in the settings.ini file
5. Specify who receives the email in the email_list file
6. Run the script once for the test
7. If you are sure that it works you can enter the following in your raspberrypi to make sure it runs in the background
   and that it doesn't quit when you close the ssh connection:
   $ sudo nohup python3 main.py &
8. Enjoy

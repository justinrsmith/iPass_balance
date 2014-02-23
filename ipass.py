import mechanize
import cookielib
from BeautifulSoup import BeautifulSoup
from twilio.rest import TwilioRestClient
from twilio.rest import TwilioRestClient

account = 'AC9f84eb4a30bd6169fa955c12ac870dc0'
token   = '940c32386afc339be294d4d019127436'
client  = TwilioRestClient(account, token)

br = mechanize.Browser()

cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

br.open('https://www.getipass.com/ipass/MobileLogin.jsp')

br.select_form(name='doMobileLogin')

br.form['txtLoginParam'] = '***'
br.form['txtPIN'] = '***'

br.submit()
page_source = br.open('https://www.getipass.com/ipass/mAcctBalance.jsp').read()

soup = BeautifulSoup(page_source)
td = soup.find('td', {'class':'oracle.jbo.format.DefaultCurrencyFormatter'})
balance = float(td.renderContents().strip().strip('$'))

if balance <= 15:
    message = client.sms.messages.create(to='***', 
                                         from_='***', 
                                         body='Your iPass balance is ' + str(balance))
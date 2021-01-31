import time
import ffpb
import tqdm
import sys
import _pickle as pickle
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options


class ProgressBar(tqdm.tqdm):
    def update(self, n):
        super().update(n)


def init_chrome(url):
    opt_args = Options()
    opt_args.add_argument("--no-sandbox")
    opt_args.add_argument("--remote-debugging-port=9222")
    # opt_args.add_argument("--headless")
    opt_args.add_argument("--window-size=1920,1080")
    opt_args.add_argument("--disable-gpu")

    browser = webdriver.Chrome(options=opt_args)

    cookies = import_session_cookies(browser)
    time.sleep(2)
    browser.get(url)

    return browser, cookies


def close_browser(b):
    b.close()


def extract_keys():
    try:
        with open("keys") as f:
            auth_data = f.read()

            auth_info = []

            for s in auth_data.splitlines():
                if not (s == ''):
                    auth_info.append(s)

            return auth_info[0], auth_info[1]

    except FileNotFoundError:
        print("*** file doesn't exists, creating 'keys'"
              " file, now fill it with data! ... exiting ***")
        open("keys", 'w')
        close_browser()


def logged_checker(b, url):
    try:
        login_button = b.find_element_by_xpath("//button[@class='button is-medium is-fullwidth is-rounded is-primary']")
        handle_login(b, login_button)
        b.get(url)

    except NoSuchElementException:
        print("Login needed but could not find button!")


def handle_login(b, button):

    e, p = extract_keys()

    email = b.find_element_by_xpath("//input[@type='email']")
    psw = b.find_element_by_xpath("//input[@type='password']")

    email.send_keys(e)
    psw.send_keys(p)

    button.click()

    time.sleep(2)

    try:
        expecting_nothing = b.find_element_by_xpath("//button[@class='button is-medium is-fullwidth is-rounded is-primary']")
        print("Login Failed")
        close_browser(b)
    except NoSuchElementException:
        print("Logged In!")
        export_session_cookies(b)


def export_session_cookies(b):
    with open("cookies", 'wb') as f:
        pickle.dump(b.get_cookies(), f)

    print("cookies saved")


def import_session_cookies(b):
    try:
        with open("cookies", 'rb') as ck:
            session_cookies = pickle.load(ck)
            # Forcing cookie domain
            b.get("https://app.buddyfit.club")
            for c in session_cookies:
                b.add_cookie(c)

        print("Logged in via session-saved cookies")
        return True

    except FileNotFoundError:
        print("*** cookies session file NOT found ***")
        return False


def retrieve_file(b):
    try:
        b.switch_to.frame(b.find_elements_by_tag_name("iframe")[0])
        url = b.find_element_by_xpath("//source[@id='MSVD-VideoSource']").get_attribute("src").split("?")[0]

        commands = ["-i", url, "-c", "copy", "output.mp4"]
        ffpb.main(argv=commands, stream=sys.stderr, encoding=None, tqdm=ProgressBar)

    except NoSuchElementException:
        print("Video source not found!")


def main():

    video = "https://app.buddyfit.club/classes/replay/7f2de072-2eb4-4eed-9f84-011af4b11395/live"
    b, cookies_flag = init_chrome(url=video)

    if not cookies_flag:
        logged_checker(b, video)

    time.sleep(2)
    retrieve_file(b)

    if input("Quit?") == "Y":
        close_browser(b)
    else:
        close_browser(b)


if __name__ == "__main__":
    main()

import time
import ffpb
import tqdm
import sys
import subprocess
import _pickle as pickle
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options


class ProgressBar(tqdm.tqdm):
    def update(self, n):
        super().update(n)


def init_chrome():
    opt_args = Options()
    opt_args.add_argument("--no-sandbox")
    opt_args.add_argument("--remote-debugging-port=9222")
    opt_args.add_argument("--headless")
    opt_args.add_argument("--window-size=1920,1080")
    opt_args.add_argument("--disable-gpu")

    b = webdriver.Chrome(options=opt_args)

    return b


def close_browser(b):
    b.close()


def extract_keys(b):
    try:
        with open("keys") as f:
            auth_data = f.read()

            auth_info = []

            for s in auth_data.splitlines():
                if not (s == ''):
                    auth_info.append(s)

            return auth_info[0], auth_info[1]

    except FileNotFoundError:
        open("keys", 'w')
        close_browser(b)
        sys.exit("*** file doesn't exists, creating 'keys'"
                 " file, now fill it with data! ... exiting ***")
    except IndexError:
        sys.exit("error in reading keys, have you correctly inserted the login data?")


def extract_video_URLs():
    try:
        with open("video_links") as f:
            data = f.read()

            links = []

            for s in data.splitlines():
                if not (s == ''):
                    links.append(s)

            return links

    except FileNotFoundError:
        open("video_links", 'w')
        sys.exit("*** file doesn't exists, creating 'video_links'"
                 " file, now fill it with URLs! ... exiting ***")


def logged_checker(b, url):
    try:
        login_button = b.find_element_by_xpath("//button[@class='button is-medium is-fullwidth is-rounded is-primary']")
        handle_login(b, login_button)
        b.get(url)

    except NoSuchElementException:
        clean_cookies()
        sys.exit("Login needed but could not find button!")


def handle_login(b, button):
    e, p = extract_keys(b)

    email = b.find_element_by_xpath("//input[@type='email']")
    psw = b.find_element_by_xpath("//input[@type='password']")

    email.send_keys(e)
    psw.send_keys(p)

    button.click()

    time.sleep(2)

    try:
        expecting_nothing = b.find_element_by_xpath(
            "//button[@class='button is-medium is-fullwidth is-rounded is-primary']")
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

            b.get("https://app.buddyfit.club")
            for c in session_cookies:
                b.add_cookie(c)

        print("Logged in via session-saved cookies")
        return True

    except FileNotFoundError:
        print("*** cookies session file NOT found ***")
        return False


def download_video(b):
    try:
        b.switch_to.frame(b.find_elements_by_tag_name("iframe")[0])
        url = b.find_element_by_xpath("//source[@id='MSVD-VideoSource']").get_attribute("src").split("?")
        file_name = "videos/"+url[1]+".mp4"

        commands = ["-i", url[0], "-c", "copy", file_name]
        ffpb.main(argv=commands, stream=sys.stderr, encoding=None, tqdm=ProgressBar)

    except NoSuchElementException:
        print("Video source not found!")
    except IndexError:
        print("Error founding frame...")


def clean_cookies():
    subprocess.run(["rm", "cookies"])


def main():

    subprocess.run(["mkdir", "videos"])
    videos = extract_video_URLs()

    b = init_chrome()

    for n, link in enumerate(videos):
        if n == 0:
            cookies = import_session_cookies(b)
            time.sleep(2)
            b.get(link)
            if not cookies:
                logged_checker(b, link)
            time.sleep(2)
            download_video(b)
        else:
            b.get(link)
            time.sleep(2)
            download_video(b)

    clean_cookies()
    close_browser(b)


if __name__ == "__main__":
    main()

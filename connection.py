from io import BytesIO
from selenium import webdriver
import time
# PIL = imaging library, save image from url
from PIL import Image
from fake_useragent import UserAgent
import constants as co
from python_anticaptcha import AnticaptchaClient, ImageToTextTask


class Connection:

    def __init__(self):
        self.options = webdriver.ChromeOptions()
        ua = UserAgent()
        user_agent = ua.random
        self.options.add_argument("--proxy-server=socks5://127.0.0.1:9150")
        self.options.add_argument('user-agent={user_agent}')
        # self.options.add_argument('--headless')
        self.driver = webdriver.Chrome(r"C:\chromedriver.exe", options=self.options)
        self.driver.get("http://avengersdutyk3xf.onion")
        self.driver.maximize_window()

    def login(self, user_name, user_password):
        # self.options.headless = False
        self.driver = webdriver.Chrome(r"C:\chromedriver.exe", options=self.options)
        self.driver.get("http://avengersdutyk3xf.onion")
        self.driver.maximize_window()
        self.driver.find_element_by_xpath(
            '//*[@id="content"]/div/table/tbody/tr[2]/td/form/table/tbody/tr[2]/td[2]/input').send_keys(user_name)
        time.sleep(1)
        self.driver.find_element_by_xpath(
           '//*[@id="content"]/div/table/tbody/tr[2]/td/form/table/tbody/tr[3]/td[2]/input').send_keys(user_password)
        time.sleep(2)
        self.driver.find_element_by_xpath(
            '//*[@id="content"]/div/table/tbody/tr[2]/td/form/table/tbody/tr[5]/td/input').click()

    def go_to_link(self, link, user='Dwider', password='qwerty123'):
        self.login(user, password)
        time.sleep(2)
        self.driver.get(link)

    def solve_captcha_image(self):
        element = self.driver.find_element_by_id('captcha_img').screenshot_as_png
        im = Image.open(BytesIO(element))  # uses PIL library to open image in memory
        im.save('screenshot.png')  # saves new cropped image
        api_key = co.API_CAPTCHA_KEY
        captcha_fp = open('screenshot.png', 'rb')
        client = AnticaptchaClient(api_key)
        task = ImageToTextTask(captcha_fp)
        job = client.createTask(task)
        job.join()
        print(job.get_captcha_text())
        self.driver.find_element_by_xpath('//*[@id="imagestring"]').send_keys(job.get_captcha_text())

    def create_user(self, user_name, user_password, user_email):
        if self.driver.current_url == co.HOME_PAGE:
            self.driver.find_element_by_xpath(
                '//*[@id="content"]/div/table/tbody/tr[2]/td/form/table/tbody/tr[5]/td/span/a[1]').click()
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="content"]/div/form/div/input[3]').click()

        self.driver.find_element_by_xpath('//*[@id="username"]').send_keys(user_name)
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="password"]').send_keys(user_password)
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="password2"]').send_keys(user_password)
        time.sleep(1)

        self.driver.find_element_by_xpath('//*[@id="email"]').clear()
        self.driver.find_element_by_xpath('//*[@id="email"]').send_keys(user_email)
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="email2"]').clear()
        self.driver.find_element_by_xpath('//*[@id="email2"]').send_keys(user_email)
        time.sleep(1)
        # solve captcha image
        self.solve_captcha_image()
        time.sleep(1)

        self.driver.find_element_by_xpath('//*[@id="registration_form"]/div/input[4]').click()
        url = str(self.driver.current_url)
        # if there is problem with register details, the user enters other details
        if url == co.REGISTER_URL:
            if self.driver.find_element_by_xpath('//*[@id="registration_form"]/div[1]/p/em') is not None:
                error_text = str(self.driver.find_element_by_xpath('//*[@id="registration_form"]/div[1]/ul').text)
                # print(error_text)
                if error_text.__contains__('username') or error_text.__contains__('password'):
                    return False, error_text
                while error_text.__contains__(co.RECAPTCHA_ERROR):
                    self.solve_captcha_image()
                    self.driver.find_element_by_xpath('//*[@id="registration_form"]/div/input[4]').click()
                    error_text = str(self.driver.find_element_by_xpath('//*[@id="registration_form"]/div[1]/ul').text)
        return True, 'Avatar Created'

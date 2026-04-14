from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class UserAction:

    def __init__(self, driver:WebDriver):
        self.driver = driver
        self.ecWait = 30

    def get(self, url):
        self.driver.get(url)

    def refreshPage(self):
        self.driver.refresh()

    def sendKeys(self, byLocator, txt: str, clear_first=True):
        elm = WebDriverWait(driver=self.driver, timeout=self.ecWait, poll_frequency=5).until(EC.visibility_of_element_located(byLocator))
    
        if clear_first:
            elm.clear()
            
        elm.send_keys(txt)

    def click(self, byLocator):
        elm = WebDriverWait(driver=self.driver, timeout=self.ecWait, poll_frequency=5).until(EC.element_to_be_clickable(byLocator))
        elm.click()

    def getTitle(self):
        return self.driver.title
    
    def getText(self, byLocator):
        elm = WebDriverWait(driver=self.driver, timeout=self.ecWait, poll_frequency=5).until(EC.visibility_of_element_located(byLocator))
        return elm.text
    
    def getAllElements(self, byLocator):
        elms = WebDriverWait(driver=self.driver, timeout=self.ecWait, poll_frequency=5).until(EC.visibility_of_all_elements_located(byLocator))
        return elms
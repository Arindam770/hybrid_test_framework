from dataclasses import dataclass
from selenium.webdriver.common.by import By
from util.web.user_action import UserAction
import allure

@dataclass
class ElementsEventHub:
    txtLoginPage = (By.XPATH,"//h1[text()='Sign in to EventHub']")
    boxEmail = (By.CSS_SELECTOR,"#email")
    boxPassword = (By.CSS_SELECTOR,"#password")
    btnSignIn = (By.CSS_SELECTOR,"#login-btn")


class Login(UserAction):

    def __init__(self, driver, take_screenshot=None):
        super().__init__(driver)
        self._screenshot = take_screenshot
    
    def _snap(self, name: str):
        """Calls take_screenshot only if it was injected."""
        if self._screenshot:
            self._screenshot(name)

    def openEventHub(self, url):
        with allure.step("Open the login page"):
            self.get(url)
            text_loginPage = self.getText(ElementsEventHub.txtLoginPage)
            self._snap("Login Page — Initial Load")
            return text_loginPage
    
    def performLoginEventHub(self, userName, password):
        with allure.step("Enter username & password"):
            self.sendKeys(byLocator=ElementsEventHub.boxEmail, txt=userName)
            self.sendKeys(byLocator=ElementsEventHub.boxPassword, txt=password)
            self._snap("Login Page — Enter login credentials")
            self.click(byLocator = ElementsEventHub.btnSignIn)
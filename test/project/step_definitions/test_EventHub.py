from pytest_bdd import parsers, when, given, then, scenario
from util.file import toml_support, excel_support
from project.func_support.login_page import Login
import pytest


@scenario("../features/eventHub.feature", "Check login functionality of EventHub")
def test_chcek_login():
    pass


@given("User opens the EventHub application")
def given_open_application(driver, take_screenshot):
    toml_details = toml_support.Toml_Support("test\\config\\app_details.toml").read_toml()
    login = Login(driver, take_screenshot)
    text_loginPage = login.openEventHub(toml_details['sit']['EventHub']['appUrl'])
    assert "Sign in to EventHub" in text_loginPage, "EventHub page is not available"

@when("User logs in with valid credentials")
def when_perform_login(driver, take_screenshot):
    toml_details = toml_support.Toml_Support("test\\config\\app_details.toml").read_toml()
    login = Login(driver, take_screenshot)
    login.performLoginEventHub(userName = toml_details['sit']['EventHub']['userName'], password= toml_details['sit']['EventHub']['password'])

@then("User should be successfully logged in")
def then_validate_login(driver, take_screenshot):
    #pytest.skip("Login validation not yet implemented")
    pass
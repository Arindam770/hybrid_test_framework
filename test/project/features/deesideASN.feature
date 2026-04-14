@EventHub
Feature: Validate required functionalities in EventHub application
    This feature will cover all the main functionalities

    @login
    Scenario: Check login functionality of EventHub
        Given User opens the EventHub application
        When User logs in with valid credentials
        Then User should be successfully logged in
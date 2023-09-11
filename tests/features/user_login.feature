# Created by maxli at 10.09.2023
Feature: User login
  Scenario: Successful user login
    Given registered user on "http://127.0.0.1:5000/register"
    | phone_number | password     | email                | name      |
    | 79877321243  | testPassword | testEmail1@gmail.com | Alexander |
    When user login on "http://127.0.0.1:5000/auth"
    | phone_number | password     |
    | 79877321243  | testPassword |
    Then response code is "200"
  Scenario: User login with invalid password
    Given registered user on "http://127.0.0.1:5000/register"
    | phone_number | password     | email                | name      |
    | 79877321243  | testPassword | testEmail1@gmail.com | Alexander |
    When user login on "http://127.0.0.1:5000/auth"
    | phone_number | password     |
    | 79877321243  | testPasrdq21 |
    Then response code is "401"
  Scenario: User login with invalid phone number
    Given registered user on "http://127.0.0.1:5000/register"
    | phone_number | password     | email                | name      |
    | 79877321243  | testPassword | testEmail1@gmail.com | Alexander |
    When user login on "http://127.0.0.1:5000/auth"
    | phone_number | password     |
    | 79877320000  | testPassword |
    Then response code is "401"

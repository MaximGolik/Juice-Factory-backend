Feature: User registration test on Behave
  @smoke
  Scenario: Successful user registration
    When we register user on "http://127.0.0.1:5000/register"
    | phone_number | password     | email                | name      |
    | 79877321243  | testPassword | testEmail1@gmail.com | Alexander |
    Then response code is "201"
  @smoke
  Scenario: Phone number is already taken
    When we register user on "http://127.0.0.1:5000/register"
    | phone_number | password     | email                | name      |
    | 79877321243  | testPassword | testEmail1@gmail.com | Alexander |
    And we register user on "http://127.0.0.1:5000/register"
    | phone_number | password     | email                   | name      |
    | 79877321243  | testPassword | test323Email1@gmail.com | Alexander |
    Then response code is "400"
  @smoke
  Scenario: Email is already taken
    When we register user on "http://127.0.0.1:5000/register"
    | phone_number | password     | email                | name      |
    | 79877321243  | testPassword | testEmail1@gmail.com | Alexander |
    And we register user on "http://127.0.0.1:5000/register"
    | phone_number | password     | email                | name      |
    | 79877321000  | testPassword | testEmail1@gmail.com | Alexander |
    Then response code is "400"
  @smoke
  Scenario: Email is not valid
    When we register user on "http://127.0.0.1:5000/register"
    | phone_number | password     | email          | name      |
    | 79877321243  | testPassword | testEmail1gmai | Alexander |
    Then response code is "400"

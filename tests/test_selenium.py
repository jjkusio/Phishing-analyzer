from selenium.webdriver.common.by import By

from features.dynamic_stats import connection_1


def test_selenium_starts():
    driver = connection_1()

    try:
        driver.get(
            "data:text/html,"
            "<title>Selenium test</title>"
            "<h1>Selenium works</h1>"
        )

        assert driver.title == "Selenium test"
        assert driver.find_element(By.TAG_NAME, "h1").text == "Selenium works"
    finally:
        driver.quit()
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Function to click the "Reply" button, scrape comments, and return
def click_reply_and_scrape_comments(driver):
    # Find and click the "Reply" button
    try:
        reply_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div#reply-button-end ytd-button-renderer a'))
        )
        ActionChains(driver).move_to_element(reply_button).click().perform()
    except Exception as e:
        print(f"Error clicking the reply button: {str(e)}")

    # Wait for the comments to load (adjust the wait time as needed)
    time.sleep(5)  # Adjust as needed

    # Extract and save comments
    comments = driver.find_elements(By.CSS_SELECTOR, 'ytd-backstage-comment')
    with open('daniel.txt', 'a', encoding='utf-8') as file:
        for comment in comments:
            comment_text = comment.find_element(By.CSS_SELECTOR, 'div#content').text
            file.write(comment_text + '\n')

    # Go back to the community page
    driver.back()

# Function to scrape community posts and read comments
def scrape_community_post_and_comments():
    # Initialize the Selenium WebDriver (use Chrome or Firefox WebDriver)
    driver = webdriver.Chrome()  # Use Chrome WebDriver
    # driver = webdriver.Firefox()  # Use Firefox WebDriver

    # Open the channel's community page
    channel_url = 'https://www.youtube.com/@DanielLarson-ob2jw/community'  # Replace with the actual channel URL
    driver.get(channel_url)

    # Find and extract the first community post (with explicit wait)
    try:
        first_post = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'ytd-backstage-post-thread-renderer'))
        )
    except Exception as e:
        print(f"No community posts found: {str(e)}")
        driver.quit()
        return

    # Extract and save the content of the first post
    post_content = first_post.text

    # Extract and save comments for the first post if available
    click_reply_and_scrape_comments(driver)

    with open('daniel.txt', 'a', encoding='utf-8') as file:
        file.write("Post Content:\n")
        file.write(post_content + '\n\n')

    # Close the WebDriver
    driver.quit()

# Call the function to start scraping and saving every minute
while True:
    scrape_community_post_and_comments()
    time.sleep(20)  # Wait for 20 seconds before repeating

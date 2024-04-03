import undetected_chromedriver as uc
import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pandas as pd

url = "https://www.flyairlink.com/en-za/"

options = uc.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--disable-extensions")
options.add_argument("--disable-web-security")
options.add_argument("--disable-browser-side-navigation")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-features=VizDisplayCompositor")
# options.add_argument("--headless")

driver = uc.Chrome(options=options)

driver.get(url)


def type_like_human(element, text):
    for char in text:
        element.send_keys(char)
        # Randomize the typing speed between keystrokes
        time.sleep(random.uniform(0.1, 0.3))

origin = "Harare, Zimbabwe"
destination = "Cape Town, South Africa"

input_origin = driver.find_element(By.ID, "flights-booking-id-1-input")
input_destination = driver.find_element(By.ID, "flights-booking-id-2-input")

# Input origin and destination
type_like_human(input_origin, origin)
input_origin.send_keys(Keys.ENTER)
time.sleep(2)
type_like_human(input_destination, destination)
input_destination.send_keys(Keys.ENTER)
time.sleep(5)

search_button = driver.find_element(By.XPATH, '//button[@data-att="search"]')
search_button.click()
time.sleep(15)

departure_fare_elements = driver.find_elements(By.CSS_SELECTOR, 'tr.calendarPerBound-inner-elements-outbound .calendarPerBound-fare')
dep_fares_and_dates = []
# Iterate through each fare element
for departure_fare_element in departure_fare_elements:
    # Find the date element within the current fare element
    dep_day_element = departure_fare_element.find_element(By.CSS_SELECTOR, '.calendarPerBound-date-section .calendarPerBound-dayOfWeek')
    dep_date_element = departure_fare_element.find_element(By.CSS_SELECTOR, '.calendarPerBound-date-section .calendarPerBound-date')
    dep_month_element = departure_fare_element.find_element(By.CSS_SELECTOR, '.calendarPerBound-date-section .calendarPerBound-month')

    dep_day = dep_day_element.text
    dep_date = dep_date_element.text
    dep_month = dep_month_element.text

    dep_full_date = f"{dep_day}, {dep_date} {dep_month}"
    
    
    # Find the price-amount element within the current fare element
    dep_price_element = departure_fare_element.find_element(By.CSS_SELECTOR, '.calendarPerBound-price .price-amount')
    # Extract the text of the price amount
    dep_price_amount = dep_price_element.text
    
    # Append the date and price amount as a tuple to the list
    dep_fares_and_dates.append((dep_full_date, dep_price_amount))

# Print the list of tuples containing dates and price amounts
for dep_full_date, dep_price_amount in dep_fares_and_dates:
    print("Departure Date:", dep_full_date, "- Price amount:", dep_price_amount)


return_fare_elements = driver.find_elements(By.CSS_SELECTOR, 'tr.calendarPerBound-inner-elements-inbound .calendarPerBound-fare')
fares_and_dates = []
# Iterate through each fare element
for return_fare_element in return_fare_elements:
    # Find the date element within the current fare element
    day_element = return_fare_element.find_element(By.CSS_SELECTOR, '.calendarPerBound-date-section .calendarPerBound-dayOfWeek')
    date_element = return_fare_element.find_element(By.CSS_SELECTOR, '.calendarPerBound-date-section .calendarPerBound-date')
    month_element = return_fare_element.find_element(By.CSS_SELECTOR, '.calendarPerBound-date-section .calendarPerBound-month')
    # Extract the text of the date
    day = day_element.text
    date = date_element.text
    month = month_element.text

    full_date = f"{day}, {date} {month}"
    
    
    # Find the price-amount element within the current fare element
    price_element = return_fare_element.find_element(By.CSS_SELECTOR, '.calendarPerBound-price .price-amount')
    # Extract the text of the price amount
    price_amount = price_element.text
    
    # Append the date and price amount as a tuple to the list
    fares_and_dates.append((full_date, price_amount))
    
    

# Print the list of tuples containing dates and price amounts
for full_date, price_amount in fares_and_dates:
    print("Return Date:", full_date, "- Price amount:", price_amount)

input("Enter to sort by price...")

# Sort the departure fare tuples by price
dep_fares_and_dates.sort(key=lambda x: float(x[1]))
# Sort the return fare tuples by price
fares_and_dates.sort(key=lambda x: float(x[1]))


# Create a DataFrame using pandas
df = pd.DataFrame({
    'Departure Date': [x[0] for x in dep_fares_and_dates],
    'Departure Price': [x[1] for x in dep_fares_and_dates],
    'Return Date': [x[0] for x in fares_and_dates],
    'Return Price': [x[1] for x in fares_and_dates]
})

# Write the DataFrame to an Excel file
df.to_excel("flight_prices.xlsx", index=False)

input("Enter to quit")

driver.quit()

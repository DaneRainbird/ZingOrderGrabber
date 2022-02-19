# Imports
import getopt
import json
import sys
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path

# Global Variables
allOrders = []
output = Path(Path.cwd(), "./outfile.json")
verbose = None
detached = False


def getArgs(args):
    """
    Handles arguments provided to the script

    :param args: command-line arguments provided to the script
    """
    try:
        opts, args = getopt.getopt(args[1:], 'ho:vd', ['help', 'output=', 'verbose', 'detached'])
    except getopt.GetoptError as e:
        print(e)
        sys.exit(2)

    for o, a in opts:
        # Verbose Printing
        if o == "-v":
            global verbose
            verbose = True
        # Output Filepath
        elif o in ("-o", "--output"):
            global output
            output = Path(a)
        # Help / Usage
        elif o in ("-h", "--help"):
            usageGuide()
            sys.exit()
        # Detached Browser
        elif o in ("-d", "--detached"):
            global detached
            detached = True
        else:
            assert False, "Unhandled option."


def usageGuide():
    """
    Prints usage instructions to stdout.
    """
    print("[*] Zing Pop Culture Order Details Grabber")
    print("[*] By Dane Rainbird (hello@danerainbird.me)")
    print("[*] This script scrapes your order list from the Zing website and exports them in JSON format.\n")
    print("[*] Usage: main.py [-o / --output outputFilePath] [-v / --verbose], [-d / --detached] [-h / --help]")
    print("     [*] -o / --output = a fully-quantified filepath to which the output of the script should be written.")
    print("     [*] -v / --verbose = if the script should write logs / activity to standard out while running..")
    print("     [*] -d / --detached = if the WebDriver should be \"detached\" (i.e. should it remain open once the script is done.")
    print("     [*] -h / --help = displays this message.")


def verbosePrint(string):
    """
    Prints a string if the verbose flag has been set

    :param string: the string to be printed to stdout
    """
    global verbose
    if verbose:
        print(string)


def createDriver():
    """
    Creates a Chrome WebDriver and adds options to minimize chances of being detected as a bot.

    :return: a Chrome Webdriver instance
    """
    options = Options()

    # Suppress errors (INFO = 0, WARNING = 1, LOG_ERROR = 2, LOG_FATAL = 3), default 0
    options.add_argument('--log-level=3')

    # Add defensive options to prevent auto-detection of Selenium / ChromeDriver
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    # If the user wants the browser to be detached (i.e. exist after the script runs)
    if detached:
        options.add_experimental_option("detach", True)

    verbosePrint("[*] Creating WebDriver")

    # Create a new webdriver with provided options
    driver = webdriver.Chrome(service=Service(ChromeDriverManager(log_level=0, print_first_line=False).install()), options=options)

    return driver


def getCookies(file="zing_cookies.txt"):
    """
    Obtains a list of cookies from a text file.

    :param file: the .txt file containing the cookie values to load (defaults to zing_cookies.txt in the working dir)
    :return: A list containing dictionary values of cookies in the form of {name, value}
    """

    cookies = []
    verbosePrint("[*] Getting cookies from {0}".format(file))
    with open(file, 'r') as fileData:
        for line in fileData:
            line = line.strip()
            # Ignore any comment lines
            if line.startswith("#") or not line:
                continue
            values = line.split(" ")
            cookies.append({'name': values[0], 'value': values[1]})

    verbosePrint("[*] Obtained cookies from {0}".format(file))
    return cookies


def addCookies(cookies, driver):
    """
    Reads cookies in from an array and adds them to the driver.

    :param cookies: A list containing dictionary values of cookies in the form of {name, value}
    :param driver: A ChromeDriver instance
    """
    for cookie in cookies:
        driver.add_cookie(cookie)


def parseOrder(order):
    """
    Parses the HTML div for an order and gets relevant data

    :param order: the HTML for an "order" div
    :return: a dictionary containing relevant information from the order
    """
    orderDate = order.find_element(By.CLASS_NAME, "date").text
    orderUrl = order.find_element(By.CLASS_NAME, "shipment").get_attribute("href")
    orderTotalPrice = order.find_element(By.CLASS_NAME, "total").text
    orderLocation = order.find_element(By.CLASS_NAME, "location").text
    orderProductList = []

    orderProducts = order.find_elements(By.CLASS_NAME, "product")
    for product in orderProducts:
        orderProductList.append({'name': product.find_element(By.CLASS_NAME, 'description').text,
                                 'status': product.find_element(By.CLASS_NAME, "status").text})

    orderDetails = {
        'date': orderDate,
        'url': orderUrl,
        'totalPrice': orderTotalPrice,
        'location': orderLocation,
        'products': orderProductList
    }

    return orderDetails


def findOrders(driver, page):
    """
    Finds the order list on the EBWorld page, and sends the data to be parsed.

    :param driver: A ChromeDriver instance
    :param page: The page number to be searching
    :return: a list of all parsed order details
    """
    verbosePrint("[*] Obtaining orders for page {0}".format(page))

    orderHistory = driver.find_element(By.CLASS_NAME, "order-history")
    orders = orderHistory.find_elements(By.CLASS_NAME, 'order')

    verbosePrint("[*] Found {0} orders on page {1}\n".format(len(orders), page))

    # For each order found, parse their details
    for order in orders:
        orderDetails = parseOrder(order)
        allOrders.append(orderDetails)

    # Pagination is present on every page, even if the user has only one page
    pagination = driver.find_element(By.CLASS_NAME, "pagination")

    # If there is no right-chevron icon in the pagination, then there are no more pages
    if len(pagination.find_elements(By.CLASS_NAME, "icon-chervon-right")) == 0:
        verbosePrint("[*] No more order pages, ending\n")
        return allOrders

    else:
        verbosePrint("[*] Found more order pages, continuing")
        page = page + 1
        driver.get("https://www.zingpopculture.com.au/ebworld/order-history?page={0}".format(page))

        # Wait for 5 seconds to simulate human browsing and prevent Cloudflare detection
        time.sleep(5)

        # Recursively find orders
        findOrders(driver, page)


def __init__():
    """
    init function
    """

    # Get and process CLI arguments
    getArgs(sys.argv)

    # Create a driver and change webdriver "navigator" value to undefined
    driver = createDriver()
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    verbosePrint("[*] Navigating to dummy page and adding cookies")

    # Get a dummy page in order to set the cookies (see https://www.selenium.dev/documentation/webdriver/browser/cookies/)
    driver.get("https://www.zingpopculture.com.au/404")

    # Get cookies and add them to the driver
    cookies = getCookies()
    addCookies(cookies, driver)

    verbosePrint("[*] Added cookies")

    # Wait for 5 seconds before attempting to view order history (simulating a human browsing the page)
    time.sleep(5)
    driver.get("https://www.zingpopculture.com.au/ebworld/order-history?page=1")

    # Find orders from the order history, starting on page one
    findOrders(driver, 1)

    # Save to file based on the user's selected filepath (defaults to working dir if no argument provided)
    with open(output, 'w') as outfile:
        json.dump(allOrders, outfile)


__init__()

# Zing Pop Culture Order Grabber

A Selenium-based webscraper that obtains your order history from the Zing Pop Culture website and exports them in a JSON format. A simple website for formatting and searching this data is also provided. 

# Getting Started 

## Python Libraries

Firstly, install the required Python libraries using pip from your working directory:

```
pip install -r requirements.txt
```

**N.B.** It is highly recommended that you create a [Python Virtual Environment](https://docs.python.org/3/library/venv.html) before installing these libraries to prevent incompataibilty issues.

## Obtaining the Cookies
In order to allow the program to scrape your order data, you must first obtain your Session cookies from the Zing website:

1. Make a copy of the `zing_cookies_template.txt` file and name it `zing_cookies.txt`.
2. Sign into the [Zing website](https://zingpopculture.com.au/).
3. Open your browser's Developer Tools and locate the cookies for `zingpopculture.com.au` and `.zingpopculture.com.au`. 
4. Copy the relevant values (see `zing_cookies_template.txt` for a list of required cookie values) into the `zing_cookies.txt` file, ensuring there is a space after the name of the cookie.

Your `zing_cookies.txt` file should look similar to the image below:

![Screenshot of the zing_cookies.txt file with the values mostly blurred out.](https://i.imgur.com/oO0XQLM.png "zing_cookiex.txt file with values filled.")

**N.B.** Only the _value_ of the cookie is required, no other details (such as the expiry) are required.

# Running the Program 
Once you have your cookies file saved, you can run the program as below:

```
python main.py [-o / --output outputFilePath] [-v / --verbose], [-d / --detached] [-h / --help]
```

This will download the latest ChromeDriver to your device, open it to your order list, and begin to scrape data. Each page will stay open for 5 seconds in order to prevent the server detecting the script as a bot.

## Switches / Options
- `-o / --output` - a fully-quantified filepath to which the output of the script should be written. Defaults to the current working directory.
- `-v / --verbose` - if the script should write logs / activity to standard out while running. 
- `-d / --detached` - if the WebDriver should be "detached" (i.e. should it remain open once the script is done. 
- `-h / --help` - display a help message and then exit.

# Viewing the Output
Once the program has successfully finished running, a file named `output.json` will be generated in your working directory (if you make use of the `-o` switch, the file will be named whatever you inputted as part of the filepath.)

This file contains a list of JSON objects containing basic details about each order, as well as a link to view the order details. An example of this can be seen below:

![Screenshot of the output.json file, containing order details for the purchase of a Nintendo Switch Lite on Tuesday the 5th of May 2020.](https://i.imgur.com/aMmKhPP.png "An example order object.")

## Viewing Output in the Viewer Webapp
If preferred, this data can be nicely formatated by opening the `index.html` page present within the `html` folder. 

On this page, you can select your `output.json` file and see a simple list of your orders, which can be searched through by product name, location, or price:

![Screenshot of the Viewer Webapp, containing order details for the purchase of a Nintendo Switch Lite on Tuesday the 5th of May 2020.](https://i.imgur.com/FdMk6Tb.png "An example order in the webapp.")

## Disclaimer 
This tool is not affiliated with, or authorised by, Zing Pop Culture. The name and logo of Zing Pop Culture are registered trademarks of Electronics Boutique Australia Pty Limited, trading as "ZiNG Pop Culture". I make no claim to any of the data that this tool exports.

This tool is provided as-is, for educational purposes only. I am not responsible for any potential issues caused by using this tool, such as, but not limited to, account suspension or deletion.
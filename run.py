import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

def print_instructions():
    """
    Display the instructions for using the Link-Validator Tool.
    """
    print("Welcome to the Link-Validator Tool!")
    print("This tool allows you to scrape a webpage and validate all the links.")
    print("Please enter the URL you want to scrape below.")
    print("")

def get_user_input():
    """
    Get the URL input from the user and validate it.
    """
    while True:
        try:
            url = input("Enter the URL you want to scrape: \n")
            # Check if the URL starts with "http://" or "https://"
            if not url.startswith(("http://", "https://")):
                # If not, add "http://" to the beginning of the URL
                url = "https://" + url
            if validate_url(url):
                return url
            else:
                print("Invalid URL. Please try again.")
        except KeyboardInterrupt:
            print("\nProgram terminated by user.")
            exit()

def validate_url(url):
    """
    Validate the URL by sending a HEAD request and checking the status code.
    """
    try:
        response = requests.head(url, allow_redirects=True, stream=True, timeout=5)
        print("Status code: " + str(response.status_code))
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return False
    except ValueError as e:
        print(f"Invalid URL: {e}")
        return False

def load_page_with_progress(url):
    """
    Load a webpage and display a progress bar while loading.
    """
    try:
        # Get the HTML content of the webpage
        response = requests.get(url, stream=True)

        # Store the response content in a variable
        html_content = response.content

        # Display the progress bar while reading the content
        with tqdm(total=len(html_content), unit="B", unit_scale=True, desc="Loading", unit_divisor=2048) as progress_bar:
            for chunk in response.iter_content(chunk_size=1024):
                progress_bar.update(len(chunk))

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")
        
        return soup
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
    
def main():
    """
    The main function of the Link-Validator Tool.
    """
    print_instructions()
    url = get_user_input()
    print("You entered: " + url)
    data = []
    
    # proceed = True
    
    # Check if the URL is allowed to be scraped by robots.txt
    # robots_url = url + "/robots.txt"
    # robots_response = requests.get(robots_url)
    # robots_content = robots_response.text

    # Check if the website allows scraping
    # if "User-agent: *" in robots_content and "Disallow: /" in robots_content:
    #     print("This website does not allow scraping.")
    #     print("Please check the robots.txt file for more information.")
    #     print(robots_url)
    #     proceed = False
    # else:
        # If the website allows scraping, proceed with the scraping

    # Print the current page being scraped
    print(f"Scraping {url}...")
    
    # Load the webpage and parse the HTML content
    soup = load_page_with_progress(url)
   
    if soup:
        # Find all the links on the page
        all_links = soup.find_all("a")

        # Loop through all the links and get the href attribute
        for link in all_links:
            # Get the href attribute of the link
            href = link.get("href")
            data.append(href)

        # Print the number of links found on the page
        print(f"Found {len(data)} links on {url}.")

        # Convert the list to a DataFrame and save it to a CSV file
        df = pd.DataFrame(data, columns=["link"])
        df.to_csv("links.csv", index=False)
        print("Scraping complete!")
    
    # Ask the user if they want to scrape another URL
    if input("Do you want to scrape another URL? (y/n): ").lower() == "y":
        main()
    else:
        print("Goodbye!")

# Sort the data
# data.sort()

# test - URL: https://jeffdruid.github.io/fitzgeralds-menu/menu

# TODO - Add link validation to check if the link is valid
# TODO - Add filtering to remove duplicate links
# TODO - Add filtering types (e.g. only internal links, only external links)
# TODO - Add a function to save the data to a file
# TODO - Add a function to load the data from a file
# TODO - Add a function to handle different types of data (e.g. images, videos, text)
# TODO - Add error handling for requests where url is invalid or inaccessible
# TODO - Add a function to sort the data
# TODO - Add a function to display the data
# TODO - Add a function to search the data
# TODO - Add a function to filter the data
# TODO - Add a function to handle pagination
# TODO - Add a function to handle proxies
# TODO - Add a function to handle user agents
# TODO - Add a function to handle rate limits
# TODO - Add a function to handle timeouts

if __name__ == "__main__":
    main()
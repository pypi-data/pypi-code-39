from bs4 import BeautifulSoup
import requests
import webbrowser
import os

def get_soup(url):
    web_page = requests.get(url)
    return BeautifulSoup(web_page.text, "html.parser")

def get_link(soup, locator, url, logger):
    path = locator.split(":")
    working_area = soup
    for i, node in enumerate(path):
        try:
            if i > 0:
                logger.log("Current Scope:")
                logger.log(str(working_area))
        
            if node.startswith("."):
                logger.log("\n# Finding tag with class: " + node[1:])
                working_area = working_area.find(class_=node[1:])
            elif node.startswith("#"):
                logger.log("\n# Finding tag with class: " + node[1:])
                working_area = working_area.find(id=node[1:])
            elif node.startswith("^"):
                logger.log("\n# Moving to parent tag...")
                working_area = soup.find(working_area).parent
            elif node.startswith("*"):
                logger.log("\n# Getting attribute: href")
                working_area = working_area.get_attribute_list("href")[0]
            elif node.startswith("@"):
                logger.log("\n# Getting attribute: " + node[1:])
                working_area = working_area.get_attribute_list(node[1:])
            else:
                logger.log("\n# Finding tag: " + node + "...")
                working_area = working_area.find(name=node)
        except AttributeError:
            logger.log("\nUnable to locate link.  Please correct config file.", True)
        
    try:
        logger.log("# Current Location: ")
        logger.log(working_area)
        if not working_area.startswith("http"):
            logger.log("# Relative URL found.")
            working_area = url[:find_nth(url, "/", 3)] + working_area
            logger.log("# Edited location: " + working_area)
    except Exception:
        logger.log("# Empty Location")
        return False

    
    return working_area

def download(out_folder_location, file_name, url, locator, folder, logger):
    logger.log("\n\n######## " + file_name + " ########", True)
    logger.log("Searching for download at URL: " + url, True)

    download_link = False
    if locator == "+":
        logger.log("# Downloading directly at URL: " + url, True)
        download_link = url
    elif locator == "-":
        logger.log("# Manual download required.  Opening page in default browser...", True)
        webbrowser.open(url)
        status = "Manual"
    else:
        soup = get_soup(url)
        download_link = get_link(soup, locator, url, logger)
    
    if not download_link == False:
        download_file = requests.get(download_link, allow_redirects = True)
        out_folder = os.path.join(out_folder_location, folder)
        if not os.path.exists(out_folder):
            os.makedirs(out_folder)
        
        out = os.path.join(out_folder, file_name)
        open(out, 'wb').write(download_file.content)
        logger.log("# "+file_name+" downloaded.", True)
        logger.log("# Saved to "+out, True)
        result = "Success"
    else:
        logger.log("# Unable to save file.  See log file for further details.")
        result = "Failed"
    
    return result

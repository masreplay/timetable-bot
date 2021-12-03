from typing import List

from extract_emails import DefaultFilterAndEmailFactory
from extract_emails.browsers.chrome_browser import ChromeBrowser
from extract_emails.workers import DefaultWorker


def get_emails(links: List[str]) -> List[str]:
    emails: List[str] = []
    with ChromeBrowser(executable_path="./chromedriver.exe") as browser:
        for link in links:
            factory = DefaultFilterAndEmailFactory(
                website_url=link,
                browser=browser, depth=0, max_links_from_page=1)
            extractor = DefaultWorker(factory)
            data = extractor.get_data()

            for email in data[0].data.get("email"):
                if email != "contact@ytcvn.com":
                    emails.append(email)
                    break
    return emails

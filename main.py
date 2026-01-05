from agent.browser import BrowserAgent
import random


def main():
    websites = [
        "https://www.google.com",
        "https://www.microsoft.com",
        "https://www.apple.com",
        "https://www.amazon.com",
        "https://about.meta.com",
        "https://www.netflix.com",
        "https://www.tesla.com",
        "https://www.ibm.com",
        "https://www.adobe.com",
        "https://www.nvidia.com",
        "https://www.intel.com",
        "https://www.oracle.com",
        "https://www.spotify.com",
        "https://www.salesforce.com",
        "https://www.airbnb.com",
    ]

    selected_site = random.choice(websites)
    print(f"[MAIN] Starting agent on: {selected_site}")

    agent = BrowserAgent(headless=False)
    agent.open_website(selected_site)


if __name__ == "__main__":
    main()

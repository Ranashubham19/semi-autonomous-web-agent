from playwright.sync_api import sync_playwright
from agent.decision import DecisionAgent
from agent.logger import AgentLogger


class BrowserAgent:
    def __init__(self, headless=False):
        self.headless = headless
        self.decision_agent = DecisionAgent()
        self.logger = AgentLogger()

    def open_website(self, url):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            context = browser.new_context()
            page = context.new_page()

            # ---------- OPEN ----------
            self.logger.log(f"Opening website: {url}")
            page.goto(url, timeout=60000)
            page.wait_for_timeout(3000)

            # ---------- ISSUE DETECTION ----------
            for issue in self.decision_agent.detect_issues(page):
                self.logger.log_issue(issue)

            # ---------- ANALYZE ----------
            insights = self.decision_agent.analyze_page(page)
            for insight in insights:
                self.logger.log(insight)

            # ---------- DECISION ----------
            decision = self.decision_agent.decide_next_action(page)
            self.logger.log(
                f"Decision: {decision['reason']} "
                f"(confidence={decision['confidence']})"
            )

            from_url = page.url

            # ---------- ACTION 1 ----------
            try:
                if decision["action"] == "click_button":
                    page.locator("button:visible").first.click()
                    self.logger.log("Clicked a visible button")
                    page.wait_for_timeout(3000)

                elif decision["action"] == "click_cta_link":
                    links = page.locator("a:visible")
                    for i in range(min(links.count(), 10)):
                        text = links.nth(i).inner_text().lower()
                        if any(k in text for k in self.decision_agent.CTA_KEYWORDS):
                            with context.expect_page() as new_page:
                                links.nth(i).click()
                            page = new_page.value
                            page.wait_for_load_state()
                            self.logger.log(f"Clicked CTA link '{text}'")
                            break

                elif decision["action"] == "click_link":
                    with context.expect_page() as new_page:
                        page.locator("a:visible").first.click()
                    page = new_page.value
                    page.wait_for_load_state()
                    self.logger.log("Clicked generic visible link")

                else:
                    self.logger.log("No action taken")

            except Exception as e:
                self.logger.log(f"Action failed safely: {e}")

            # ---------- TRANSITION ----------
            if page.url != from_url:
                self.logger.log_transition(from_url, page.url)

            # ---------- ACTION 2 (REACTION) ----------
            self.logger.log("Performing secondary action: scrolling")
            page.mouse.wheel(0, 1200)
            page.wait_for_timeout(3000)

            # ---------- FINALIZE ----------
            self.logger.save_report()
            page.wait_for_timeout(4000)
            browser.close()

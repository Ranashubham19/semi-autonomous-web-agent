class DecisionAgent:
    CTA_KEYWORDS = [
        "explore", "learn", "get started", "discover",
        "book", "buy", "shop", "try", "view", "see"
    ]

    def analyze_page(self, page):
        insights = []

        link_count = page.locator("a").count()
        button_count = page.locator("button").count()

        insights.append(f"{link_count} link(s) found.")
        insights.append(f"{button_count} button(s) found.")

        title = page.title()
        if title:
            insights.append(f"Page title: {title}")
        else:
            insights.append("Page has no title.")

        return insights

    def detect_issues(self, page):
        issues = []

        if not page.title():
            issues.append("Missing page title")

        if page.locator("a").count() == 0 and page.locator("button").count() == 0:
            issues.append("No actionable elements found")

        if page.locator("a").count() > 300:
            issues.append("Excessive number of links (possible cluttered UI)")

        return issues

    def decide_next_action(self, page):
        # Prefer buttons (strongest signal)
        buttons = page.locator("button:visible")
        if buttons.count() > 0:
            return {
                "action": "click_button",
                "confidence": 0.9,
                "reason": "Visible buttons indicate primary actions"
            }

        # Prefer CTA links
        links = page.locator("a:visible")
        for i in range(min(links.count(), 10)):
            text = links.nth(i).inner_text().lower()
            if any(k in text for k in self.CTA_KEYWORDS):
                return {
                    "action": "click_cta_link",
                    "confidence": 0.75,
                    "reason": f"CTA keyword found in link text '{text}'"
                }

        # Fallback
        if links.count() > 0:
            return {
                "action": "click_link",
                "confidence": 0.5,
                "reason": "Fallback to generic visible link"
            }

        return {
            "action": "do_nothing",
            "confidence": 0.1,
            "reason": "No actionable elements found"
        }

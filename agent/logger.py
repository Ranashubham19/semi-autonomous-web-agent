import json
from datetime import datetime


class AgentLogger:
    def __init__(self):
        self.logs = []
        self.transitions = []
        self.issues = []

    def log(self, message):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "message": message
        }
        print(message)
        self.logs.append(entry)

    def log_transition(self, from_url, to_url):
        self.transitions.append({
            "from": from_url,
            "to": to_url
        })
        self.log(f"Page transition: {from_url} → {to_url}")

    def log_issue(self, issue):
        self.issues.append(issue)
        self.log(f"[ISSUE DETECTED] {issue}")

    def save_report(self):
        report = {
            "logs": self.logs,
            "transitions": self.transitions,
            "issues": self.issues
        }

        # Save JSON report
        with open("report.json", "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        # Save Markdown report
        with open("report.md", "w", encoding="utf-8") as f:
            f.write("# Agent Execution Report\n\n")

            f.write("## Logs\n")
            for l in self.logs:
                f.write(f"- {l['timestamp']}: {l['message']}\n")

            f.write("\n## Page Transitions\n")
            for t in self.transitions:
                f.write(f"- {t['from']} → {t['to']}\n")

            f.write("\n## Detected Issues\n")
            if self.issues:
                for i in self.issues:
                    f.write(f"- {i}\n")
            else:
                f.write("- No issues detected\n")

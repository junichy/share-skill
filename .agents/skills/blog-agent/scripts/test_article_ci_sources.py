import unittest

from article_ci import render_research_template, research_ci


class ResearchSourcesTest(unittest.TestCase):
    def check_source(self, text, expected):
        findings = []
        research_ci(findings, [text], "sample")
        source = next(f for f in findings if f.check == "Primary SERP source")
        self.assertEqual(source.status, expected)
        return findings

    def test_keyword_source_snapshot(self):
        findings = self.check_source(
            "- Search source: approved keyword source / headline / API\n"
            "- Date: 2026-09-20\n- q: sample\n"
            "- Source reference / export: research/sample.json\n", "PASS"
        )
        metadata = next(f for f in findings if f.check == "SERP snapshot metadata")
        self.assertEqual(metadata.status, "PASS")

    def test_japanese_keyword_source(self):
        self.check_source("- Search source: approved keyword source / 見出し抽出", "PASS")

    def test_actual_browser_remains_supported(self):
        self.check_source("- Search source: user Chrome / Google", "PASS")

    def test_blank_template_is_not_observation(self):
        self.check_source(render_research_template("sample"), "WARN")

    def test_casual_mention_is_not_source(self):
        self.check_source("Approved keyword source could be used later; search summary only.", "WARN")

    def test_missing_research_still_blocks(self):
        findings = []
        research_ci(findings, [], "sample")
        self.assertEqual(findings[0].status, "NEEDS_EVIDENCE")


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

from pathlib import Path

from playwright.sync_api import sync_playwright


OUTPUT = Path("docs/screenshots")


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(
            viewport={"width": 1440, "height": 1000},
            device_scale_factor=1,
        )
        page.goto("http://127.0.0.1:8000", wait_until="networkidle")
        page.screenshot(path=OUTPUT / "dashboard.png", full_page=True)

        with page.expect_response(lambda response: "/api/analyses/demo" in response.url):
            page.get_by_role("button", name="Analyze insecure PR").click()
        page.wait_for_timeout(500)
        page.screenshot(path=OUTPUT / "insecure-analysis.png", full_page=True)

        with page.expect_response(lambda response: "/api/analyses/demo" in response.url):
            page.get_by_role("button", name="Verify fixed version").click()
        page.wait_for_timeout(500)
        page.screenshot(path=OUTPUT / "secure-analysis.png", full_page=True)
        browser.close()


if __name__ == "__main__":
    main()

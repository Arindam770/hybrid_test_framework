import pytest
import allure
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


# ──────────────────────────────────────────────
# 0. PRE-CREATE OUTPUT DIRECTORIES
# ──────────────────────────────────────────────
def pytest_configure(config):
    base = os.path.join(os.getcwd(), "test", "support_files")
    os.makedirs(os.path.join(base, "allure-results"), exist_ok=True)
    os.makedirs(os.path.join(base, "screenshots"), exist_ok=True)


def pytest_sessionfinish(session, exitstatus):
    import subprocess
    timestamp      = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    allure_results = os.path.join(os.getcwd(), "test", "support_files", "allure-results")
    allure_report  = os.path.join(os.getcwd(), "test", "report", timestamp)
    subprocess.run(
        ["allure", "generate", allure_results, "-o", allure_report],
        check=False,
        shell=True
    )


# ──────────────────────────────────────────────
# 1. DRIVER FIXTURE
# ──────────────────────────────────────────────
@pytest.fixture(scope="function")
def driver(request):
    """
    Initializes and tears down the WebDriver.
    Attaches the driver to the request node so
    it is accessible from hooks.
    """
    options = Options()
    # options.add_argument("--headless")  # Uncomment for CI
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    #driver.implicitly_wait(10)

    # ✅ Attach driver to the pytest request node — key for hooks
    request.node._driver = driver

    yield driver

    driver.quit()


# ──────────────────────────────────────────────
# 2. SCREENSHOT HELPER UTILITY
# ──────────────────────────────────────────────
def capture_screenshot(driver, name: str, attach_to_allure: bool = True) -> str:
    """
    Captures a screenshot and optionally attaches it to Allure.

    Args:
        driver:            Active WebDriver instance
        name:              Logical name for the screenshot
        attach_to_allure:  Whether to attach to Allure report

    Returns:
        File path of the saved screenshot
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    safe_name = name.replace(" ", "_").replace("/", "-")
    filename = f"{safe_name}_{timestamp}.png"

    # Save locally (optional but useful for debugging)
    screenshots_dir = os.path.join(os.getcwd(), "test", "support_files", "screenshots")
    os.makedirs(screenshots_dir, exist_ok=True)
    filepath = os.path.join(screenshots_dir, filename)
    driver.save_screenshot(filepath)

    # Attach to Allure
    if attach_to_allure:
        allure.attach(
            driver.get_screenshot_as_png(),
            name=name,
            attachment_type=allure.attachment_type.PNG
        )

    return filepath


# ──────────────────────────────────────────────
# 3. MANUAL SCREENSHOT FIXTURE (for mid-test use)
# ──────────────────────────────────────────────
@pytest.fixture(scope="function")
def take_screenshot(driver):
    """
    Inject this fixture into any step/test to take
    screenshots manually at any point during execution.

    Usage in step:
        def step_impl(driver, take_screenshot):
            take_screenshot("After clicking Submit")
    """
    def _take(name: str):
        return capture_screenshot(driver, name)

    return _take


# ──────────────────────────────────────────────
# 4. AUTOMATIC PASS / FAIL SCREENSHOT — HOOK
# ──────────────────────────────────────────────
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook that fires after each test PHASE (setup/call/teardown).
    Used to:
      - Take a FAIL screenshot automatically on test failure
      - Take a PASS screenshot automatically on test success
    """
    outcome = yield                        # Run the test phase
    report = outcome.get_result()

    # Only act on the actual test body (call phase)
    if report.when == "call":
        driver = getattr(item, "_driver", None)

        if driver is None:
            return  # No driver attached, skip screenshot logic

        if report.failed:
            # ── FAIL Screenshot ──
            test_name = item.name
            capture_screenshot(driver, f"FAILED_{test_name}")

            # Attach extra metadata to Allure
            allure.attach(
                f"Test: {test_name}\nError: {str(report.longrepr)}",
                name="Failure Details",
                attachment_type=allure.attachment_type.TEXT
            )

        elif report.passed:
            # ── PASS Screenshot (optional — remove if too noisy) ──
            test_name = item.name
            capture_screenshot(driver, f"PASSED_{test_name}")


# ──────────────────────────────────────────────
# 5. ALLURE ENVIRONMENT & BDD METADATA HELPERS
# ──────────────────────────────────────────────
@pytest.fixture(autouse=True)
def allure_metadata(request):
    """
    Auto-attaches BDD feature/scenario metadata to every test in Allure.
    Works seamlessly with pytest-bdd.
    """
    # Attach test name as Allure description
    allure.dynamic.description(f"Scenario: {request.node.name}")

    # Tag severity — override per-test using @allure.severity marker
    marker = request.node.get_closest_marker("severity")
    if marker:
        allure.dynamic.severity(marker.args[0])
    else:
        allure.dynamic.severity(allure.severity_level.NORMAL)

    yield
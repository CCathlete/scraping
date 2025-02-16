from selenium.common.exceptions import NoSuchElementException, TimeoutException


class Spider:
    def paginate(
        self,
        next_button_locator: Optional[Locator] = None,
        next_page_url_fn: Optional[Callable[[int], str]] = None,
        scroll: bool = False,
        max_pages: int = 10,
    ) -> None:
        """
        Handles pagination based on the provided strategy:
        - Clicks a 'Next' button if `next_button_locator` is provided.
        - Navigates using URL pattern if `next_page_url_fn` is provided.
        - Scrolls down for infinite scrolling if `scroll` is True.

        Args:
            next_button_locator (Locator, optional): Locator for the "Next" button.
            next_page_url_fn (Callable[[int], str], optional): Function to generate paginated URLs.
            scroll (bool, optional): Enables infinite scrolling.
            max_pages (int): Maximum number of pages to prevent infinite loops.
        """
        for page in range(1, max_pages + 1):
            if scroll:
                self._scroll_down()
                continue

            if next_page_url_fn:
                next_url = next_page_url_fn(page)
                if next_url:
                    self.driver.get(next_url)
                    continue

            if next_button_locator:
                try:
                    next_button = self.driver.find_element(
                        next_button_locator.type, next_button_locator.value
                    )
                    if next_button.is_displayed():
                        next_button.click()
                        time.sleep(2)  # Allow page load
                        continue
                except (NoSuchElementException, TimeoutException):
                    break  # No more pages

            break  # Exit if no pagination method applies

    def _scroll_down(self):
        """Scrolls to the bottom of the page to trigger loading more content."""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Adjust based on loading behavior

from selenium.common.exceptions import NoSuchElementException, TimeoutException


def paginate(
    self,
    override_pag_opts: Optional[PaginationOptions] = None,
) -> bool:
    """
    Attempts to move to the next page. Returns True if successful, False otherwise.
    """
    if override_pag_opts:
        next_button_locator = override_pag_opts.next_button_locator
        next_page_url_fn = override_pag_opts.next_page_url_fn
        scroll = override_pag_opts.scroll
        max_pages = override_pag_opts.max_pages
    elif self.pagination_opts:
        next_button_locator = self.pagination_opts.next_button_locator
        next_page_url_fn = self.pagination_opts.next_page_url_fn
        scroll = self.pagination_opts.scroll
        max_pages = self.pagination_opts.max_pages
    else:
        return False  # No pagination options set

    for page in range(1, max_pages + 1):
        if scroll:
            prev_height = self.driver.execute_script(
                "return document.body.scrollHeight"
            )
            self.__scroll_to_bottom()
            time.sleep(2)  # Allow time for new content to load
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height > prev_height:
                return True  # Successfully scrolled
            return False  # No more content to load

        if next_page_url_fn:
            next_url = next_page_url_fn(page)
            if next_url:
                self.driver.get(next_url)
                return True  # Successfully navigated

        if next_button_locator:
            try:
                next_button = self.driver.find_element(
                    next_button_locator.type, next_button_locator.value
                )
                if next_button.is_displayed():
                    next_button.click()
                    time.sleep(2)  # Allow time for loading
                    return True  # Successfully clicked next button
            except (NoSuchElementException, TimeoutException):
                return False  # No more pages available

    return False  # Exhausted pagination options

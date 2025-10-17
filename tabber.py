import pywinauto; from pywinauto.findwindows import ElementNotFoundError; from pywinauto.application import ProcessNotFoundError
import psutil

def hi():
    print("hi")

def count_browser_tabs(browser_executable):
    """
    Counts open tabs in specified web browser, Windows specific.
    Supports Chromium-based browsers and Firefox at the moment.

    Args:
        browser_executable (str): The executable name of the browser (e.g., 'chrome.exe', 'firefox.exe', 'msedge.exe').
    
    Returns:
        int: The number of open tabs in the specified browser, or 0 if the browser isn't running.
    """

    total_tabs = 0

    # find windows, whatever they're called, not all processes because not all processes have windows so saving processing power
    desktop = pywinauto.Desktop(backend="uia")
    all_windows = []
    brand_counts = {}   # for all chrome.exes
    target_exe = browser_executable.lower()

    def is_verified_process(window):        # imposters
        try:
            return psutil.Process(window.process_id()).name().lower() == target_exe
        except psutil.NoSuchProcess:
            return False

    try:
        # all windows ending in Mozilla Firefox
        if "firefox" in browser_executable.lower():

            all_windows = [win for win in desktop.windows(title_re=".*Mozilla Firefox$") if is_verified_process(win)]

        # chromium-based browsers using standard Chrome UI class
        else:
            all_windows = [win for win in desktop.windows(class_name="Chrome_WidgetWin_1") if is_verified_process(win)]

        if not all_windows:
            print(f"No open windows found for {browser_executable}.")
            return 0
        
        print(f"Found {len(all_windows)} windows for {browser_executable}.")

        for window in all_windows:
            if "firefox" in browser_executable.lower():
                # this is FIREFOX specific handling
                # i can't child_window() cause UIAWrapper doesn't have it. children() works fine though
                toolbars = window.children(title="Browser tabs", control_type="ToolBar")

                if toolbars:
                    wrapper = toolbars[0]

                    tab_control = wrapper.children(control_type="Tab")

                    if tab_control:
                        tab_control = tab_control[0]
                        total_tabs += tab_control.tab_count()

            elif "msedge" in browser_executable.lower():
                # I can't just TabItem because I get 53 when only 3 tabs are open idk why
                tab_control = window.descendants(control_type="Tab")
                tabs = len(tab_control[0].children()[1].children()[0].children()) - 1
                total_tabs += tabs

            else:
                # all other Chromium distributions incl. Google Chrome
                title = window.window_text()
                
                # default brand to a generic name if unable to parse
                brand = "Chromium-based"
                # split title like "Page Name - Brand Name" to get the brand
                if ' - ' in title:
                    brand = title.rsplit(' - ', 1)[-1]

                tabs_in_window = len(window.descendants(control_type="TabItem"))
                
                # add to the grand total but brands handled after
                total_tabs += tabs_in_window
                brand_counts[brand] = brand_counts.get(brand, 0) + tabs_in_window

        if 'firefox' in target_exe or 'msedge' in target_exe:
            return total_tabs
        else:
            return (total_tabs, list(brand_counts.items()))
    
    except (ProcessNotFoundError, ElementNotFoundError):
        # browser not running or no tabs found
        print(f"{browser_executable} not running or no tabs found.")
        return 0
    except Exception as e:
        print(f"An error occurred: {e}")
        return 0
    
if __name__ == "__main__":
    # uncomment browser to set that browser as var to pass as arg to function
    browser = 'chrome.exe'
    #browser = 'firefox.exe'
    #browser = 'msedge.exe'

    result = count_browser_tabs(browser)

    if isinstance(result, tuple):
        # handle the case for Chromium: (total_tabs, brand_list)
        total, brand_details = result
        if total > 0:
            print(f"Total open tabs across all Chromium distributions: {total}")
            print("--- Breakdown by Brand ---")
            for brand, count in brand_details:
                print(f"  - {brand}: {count} tabs")
        else:
            print(f"No open tabs found in {browser}.")
    else:
        # handle the simple integer return for Firefox/Edge
        total = result
        if total > 0:
            print(f"Open tabs in {browser}: {total}")
        else:
            print(f"No open tabs found in {browser}.")
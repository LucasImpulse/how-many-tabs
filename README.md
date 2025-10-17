# how-many-tabs
Enumerate how many tabs are open for a given executable (chrome.exe, firefox.exe). Discerns between different distributions of browsers using the same executable name (Google Chrome and Chromium).

---

## What it does
Counts open tabs for **msedge.exe**, **firefox.exe**, **chrome.exe** (including Chromium and Google Chrome).
Breakdown of where tabs come from if multiple chrome.exe distributions.
Relies on pywinauto UI automation so it doesn't need browser-specific extensions or APIs.
Includes process verification to ensure it's targeting the correct application and no impostor processes that have the same name.

---

## Future aims
I add a UI that tracks live with polling rate of 10 seconds or whatever the user wants.

---

## Requirements

-   Python 3.x
-   Windows Operating System
-   Required Python packages: `pywinauto` and `psutil`.

Install the necessary packages using pip:
```bash
pip install pywinauto psutil
```

---

## Usage

**tabber.py**
1.  Save the file.
2.  Open the file in a text editor.
3.  Navigate to the `if __name__ == "__main__":` block at the bottom of the script.
4.  Uncomment the line for the browser you wish to inspect. To count chrome.exe tabs:
    ```python
    if __name__ == "__main__":
        # Uncomment the browser you want to count.
        browser = 'chrome.exe'
        # browser = 'firefox.exe'
        # browser = 'msedge.exe'
    
        result = count_browser_tabs(browser)
        # ...
    ```
5.  Run the script from your terminal focused on the directory containing the file:
    ```bash
    python tabber.py
    ```

**omnitabber.py**
1.  Save the file.
2.  Open the file in a text editor.
3.  Check if `browsers_to_check` has all the executables you want to check.
4.  Run the script from your terminal focused on the directory containing the file:
    ```bash
    python omnitabber.py
    ```

### Expected Output

The script will print the total number of tabs found.

-   For Firefox or Edge you will get a single integer count:
    ```
    Found 1 windows for msedge.exe.
    Open tabs in msedge.exe: 8
    ```
-   **For `chrome.exe`**, you will get a total count and a detailed breakdown by brand:
    ```
    Found 2 windows for chrome.exe.
    Total open tabs across all Chromium distributions: 12
    --- Breakdown by Brand ---
      - Google Chrome: 9 tabs
      - Chromium: 3 tabs
    ```

omnitabber.py will do every executable in a batch operation, and the output is much the same.

---

## Why

My friends kept asking how many tabs I have open. I got tired of counting.

---

## Limitations to note

**Windows Only**: This script relies on Windows-specific UI automation libraries and will not work on macOS or Linux.
**UI Dependent**: Since it reads the live UI structure, significant updates to a browser's user interface could potentially break the script's ability to find the tab elements correctly. I will try to update if easy.

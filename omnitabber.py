import tabber

if __name__ == "__main__":
    # exe of all browsers you want to check
    browsers_to_check = ['chrome.exe', 'firefox.exe', 'msedge.exe']

    all_results = []

    for exe in browsers_to_check:
        print(f"Analyzing {exe}...")
        result = tabber.count_browser_tabs(exe)
        all_results.append((exe, result))

    # summary
    print("\n" + "="*40)
    print("Browser Tab Count Summary")
    print("="*40)

    for browser, result in all_results:
        print(f"\nBrowser: {browser}")
        print("-"* 30)

        # if the result is a tuple (for chromiums) or a simple integer
        if isinstance(result, tuple):
            total, brand_details = result
            if total > 0:
                print(f"Total Tabs: {total}")
                # Print the brand breakdown if it's not empty
                if brand_details:
                    print("Breakdown by Brand:")
                    for brand, count in brand_details:
                        print(f"    - {brand}: {count} tabs")
            else:
                print("No open tabs found.")
        else:
            # integer returns for firefox/edge
            total = result
            if total > 0:
                print(f"Total Tabs: {total}")
            else:
                print("No open tabs found.")
    
    print("\n" + "="*40)
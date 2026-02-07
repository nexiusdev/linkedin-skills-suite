#!/usr/bin/env python3
"""
LinkedIn Prospects Search Automation
Searches for prospects on LinkedIn and extracts their profile URLs and recent posts.
"""

import asyncio
import json
import re
from datetime import datetime
from playwright.async_api import async_playwright

# List of prospects to search
PROSPECTS = [
    {"name": "Bhavana Ravindran", "company": "Earlybird AI", "title": "Founder"},
    {"name": "Rishab Patwari", "company": "Hivebotics", "title": "Founder & CEO"},
    {"name": "Paco Chan", "company": "Farmio", "title": "Co-Founder"},
    {"name": "Daniel Yew", "company": "Quocia", "title": "Founder"},
    {"name": "Dushyant Verma", "company": "SmartViz", "title": "Founder"},
    {"name": "Xing Xian Ang", "company": "CapBay", "title": "CEO & Co-Founder"},
    {"name": "Alfan Hendro", "company": "RevScaler", "title": "Founder"},
    {"name": "Kieran Donovan", "company": "k-ID", "title": "Founder"},
    {"name": "Ethan Ow", "company": "Wenti Labs", "title": "Co-Founder"},
    {"name": "Eeling Yoong", "company": "Hera Bathroom", "title": "CEO"},
]

async def search_prospect(page, prospect, index):
    """Search for a single prospect on LinkedIn"""
    print(f"\n{'='*60}")
    print(f"[{index}/10] Searching: {prospect['name']} - {prospect['company']}")
    print(f"{'='*60}")
    
    result = {
        "name": prospect['name'],
        "company": prospect['company'],
        "title": prospect['title'],
        "profile_url": None,
        "posts": [],
        "status": "pending",
        "error": None
    }
    
    try:
        # Construct search query
        search_query = f"{prospect['name']} {prospect['company']}"
        search_url = f"https://www.linkedin.com/search/results/people/?keywords={search_query.replace(' ', '%20')}"
        
        print(f"Navigating to search: {search_url}")
        await page.goto(search_url, wait_until="domcontentloaded", timeout=30000)
        await asyncio.sleep(3)  # Wait for results to load
        
        # Take a snapshot for debugging
        # await page.screenshot(path=f"search_{index}_{prospect['name'].replace(' ', '_')}.png")
        
        # Look for the first person result
        # Try different selectors for search results
        selectors = [
            'a[href*="/in/"]',
            '.search-result__result-link',
            '.entity-result__title-link',
            '[data-test-search-result="PROFILE"] a',
            '.artdeco-entity-lockup__title a'
        ]
        
        profile_link = None
        for selector in selectors:
            try:
                links = await page.query_selector_all(selector)
                for link in links:
                    href = await link.get_attribute('href')
                    if href and '/in/' in href:
                        # Clean the URL to get just the profile path
                        profile_link = href.split('?')[0]  # Remove query params
                        if not profile_link.startswith('http'):
                            profile_link = f"https://www.linkedin.com{profile_link}"
                        print(f"Found profile link: {profile_link}")
                        break
                if profile_link:
                    break
            except Exception as e:
                continue
        
        if not profile_link:
            print(f"[!] No profile link found for {prospect['name']}")
            result['status'] = 'not_found'
            return result
        
        result['profile_url'] = profile_link
        
        # Navigate to profile
        print(f"Navigating to profile: {profile_link}")
        await page.goto(profile_link, wait_until="domcontentloaded", timeout=30000)
        await asyncio.sleep(3)
        
        # Navigate to recent activity page
        activity_url = f"{profile_link.rstrip('/')}/recent-activity/all/"
        print(f"Navigating to activity: {activity_url}")
        await page.goto(activity_url, wait_until="domcontentloaded", timeout=30000)
        await asyncio.sleep(3)
        
        # Take snapshot of activity page
        # await page.screenshot(path=f"activity_{index}_{prospect['name'].replace(' ', '_')}.png")
        
        # Extract post URLs from the page
        # Look for post links in the feed
        post_data = []
        
        # Try to find post links with various patterns
        post_patterns = [
            'a[href*="/feed/update/urn:li:activity:"]',
            'a[href*="/feed/update/"]',
            '.feed-shared-update-v2__commentary a',
            '.update-components-text a'
        ]
        
        for pattern in post_patterns:
            try:
                posts = await page.query_selector_all(pattern)
                for post in posts[:3]:  # Get up to 3 posts
                    href = await post.get_attribute('href')
                    if href and 'urn:li:activity:' in href:
                        # Clean and format the URL
                        if not href.startswith('http'):
                            href = f"https://www.linkedin.com{href}"
                        href = href.split('?')[0]
                        
                        # Get post text preview
                        text_elem = await post.query_selector('..')
                        text = ""
                        if text_elem:
                            text = await text_elem.inner_text() or ""
                            text = text[:200].replace('\n', ' ').strip()
                            # Handle Unicode for Windows console
                            try:
                                text.encode('cp1252')
                            except UnicodeEncodeError:
                                text = text.encode('ascii', 'ignore').decode('ascii')
                        
                        # Try to get post date
                        date = "Unknown"
                        
                        post_data.append({
                            "url": href,
                            "preview": text,
                            "date": date
                        })
                if post_data:
                    break
            except Exception as e:
                continue
        
        # Alternative: Extract from page content
        if not post_data:
            page_content = await page.content()
            # Find post URLs using regex
            post_urls = re.findall(r'https://www\.linkedin\.com/feed/update/urn:li:activity:\d+', page_content)
            post_urls = list(set(post_urls))[:3]  # Unique URLs, max 3
            
            for url in post_urls:
                post_data.append({
                    "url": url,
                    "preview": "Extracted from page content",
                    "date": "Unknown"
                })
        
        result['posts'] = post_data
        result['status'] = 'found' if post_data else 'profile_found_no_posts'
        
        print(f"[OK] Found {len(post_data)} posts for {prospect['name']}")
        for i, post in enumerate(post_data, 1):
            print(f"  Post {i}: {post['url'][:80]}...")
        
    except Exception as e:
        print(f"[ERROR] Error searching {prospect['name']}: {str(e)}")
        result['status'] = 'error'
        result['error'] = str(e)
    
    return result

async def main():
    """Main automation function"""
    print("="*70)
    print("LINKEDIN PROSPECT SEARCH AUTOMATION")
    print("="*70)
    print(f"Starting search for {len(PROSPECTS)} prospects...")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n[!] IMPORTANT: Make sure you're logged into LinkedIn in Chrome!")
    print("The browser will open and navigate to LinkedIn.\n")
    
    results = []
    
    async with async_playwright() as p:
        # Launch browser
        print("Launching Chrome browser...")
        browser = await p.chromium.launch(
            headless=False,  # Show browser so user can log in if needed
            args=['--window-size=1920,1080']
        )
        
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080}
        )
        
        page = await context.new_page()
        
        # First, navigate to LinkedIn to check login status
        print("\nNavigating to LinkedIn...")
        await page.goto("https://www.linkedin.com", wait_until="domcontentloaded", timeout=30000)
        await asyncio.sleep(3)
        
        # Check if logged in
        current_url = page.url
        if "login" in current_url or "auth" in current_url:
            print("\n[!] You need to log in to LinkedIn!")
            print("Please log in manually in the browser window.")
            print("Waiting 60 seconds for you to log in...")
            await asyncio.sleep(60)
        else:
            print("[OK] LinkedIn loaded. Checking login status...")
            await asyncio.sleep(2)
        
        # Search each prospect
        for index, prospect in enumerate(PROSPECTS, 1):
            result = await search_prospect(page, prospect, index)
            results.append(result)
            
            # Small delay between searches to avoid rate limiting
            if index < len(PROSPECTS):
                print(f"\n[*] Waiting 3 seconds before next search...")
                await asyncio.sleep(3)
        
        # Close browser
        print("\n" + "="*70)
        print("[*] Closing browser...")
        await browser.close()
    
    # Save results to JSON
    output_data = {
        "search_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_prospects": len(PROSPECTS),
        "results": results
    }
    
    output_file = r"C:\Users\melve\.claude\skills\web-icp-scanner\prospect-linkedin-search-results.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n[OK] Results saved to: {output_file}")
    
    # Print summary
    print("\n" + "="*70)
    print("SEARCH SUMMARY")
    print("="*70)
    
    found_count = sum(1 for r in results if r['status'] == 'found')
    profile_only_count = sum(1 for r in results if r['status'] == 'profile_found_no_posts')
    not_found_count = sum(1 for r in results if r['status'] == 'not_found')
    error_count = sum(1 for r in results if r['status'] == 'error')
    
    print(f"\nTotal Prospects: {len(results)}")
    print(f"  [OK] Found with posts: {found_count}")
    print(f"  [PROFILE] Profile found (no posts): {profile_only_count}")
    print(f"  [MISSING] Not found: {not_found_count}")
    print(f"  [ERROR] Errors: {error_count}")
    
    print("\nDetailed Results:")
    for r in results:
        status_icon = "[OK]" if r['status'] == 'found' else "[PROFILE]" if r['status'] == 'profile_found_no_posts' else "[NOT FOUND]"
        print(f"\n{status_icon} {r['name']} ({r['company']})")
        if r['profile_url']:
            print(f"   Profile: {r['profile_url']}")
        if r['posts']:
            print(f"   Posts found: {len(r['posts'])}")
            for i, post in enumerate(r['posts'], 1):
                print(f"     {i}. {post['url']}")
        if r['error']:
            print(f"   Error: {r['error']}")
    
    return output_data

if __name__ == "__main__":
    asyncio.run(main())

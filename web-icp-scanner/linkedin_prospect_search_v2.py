#!/usr/bin/env python3
"""
LinkedIn Prospects Search Automation v2
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

def safe_print(text):
    """Print text safely handling Unicode"""
    try:
        print(text)
    except UnicodeEncodeError:
        # Remove non-ASCII characters
        cleaned = text.encode('ascii', 'ignore').decode('ascii')
        print(cleaned)

async def search_prospect(page, prospect, index):
    """Search for a single prospect on LinkedIn"""
    safe_print(f"\n{'='*60}")
    safe_print(f"[{index}/10] Searching: {prospect['name']} - {prospect['company']}")
    safe_print(f"{'='*60}")
    
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
        
        safe_print(f"Navigating to search...")
        await page.goto(search_url, wait_until="networkidle", timeout=60000)
        await asyncio.sleep(5)  # Wait for results to load
        
        # Get page content and look for profile links
        page_content = await page.content()
        
        # Look for profile URLs in the page
        # Pattern: /in/username/ followed by optional query params
        profile_pattern = r'href="(/in/[^/"]+)'
        matches = re.findall(profile_pattern, page_content)
        
        if matches:
            # Get the first unique profile URL
            profile_path = matches[0]
            profile_link = f"https://www.linkedin.com{profile_path}"
            safe_print(f"Found profile link: {profile_link}")
        else:
            safe_print(f"[!] No profile link found for {prospect['name']}")
            result['status'] = 'not_found'
            return result
        
        result['profile_url'] = profile_link
        
        # Navigate to profile
        safe_print(f"Navigating to profile...")
        await page.goto(profile_link, wait_until="networkidle", timeout=60000)
        await asyncio.sleep(4)
        
        # Navigate to recent activity page
        activity_url = f"{profile_link.rstrip('/')}/recent-activity/all/"
        safe_print(f"Navigating to activity page...")
        await page.goto(activity_url, wait_until="networkidle", timeout=60000)
        await asyncio.sleep(4)
        
        # Get page content for post extraction
        activity_content = await page.content()
        
        # Extract post URLs using regex
        post_urls = re.findall(r'https://www\.linkedin\.com/feed/update/urn:li:activity:\d+', activity_content)
        post_urls = list(dict.fromkeys(post_urls))[:3]  # Unique URLs, max 3, preserve order
        
        post_data = []
        for url in post_urls:
            post_data.append({
                "url": url,
                "preview": "LinkedIn post",
                "date": "Recent"
            })
        
        result['posts'] = post_data
        result['status'] = 'found' if post_data else 'profile_found_no_posts'
        
        safe_print(f"[OK] Found {len(post_data)} posts for {prospect['name']}")
        for i, post in enumerate(post_data, 1):
            safe_print(f"  Post {i}: {post['url'][:70]}...")
        
    except Exception as e:
        error_msg = str(e)
        safe_print(f"[ERROR] Error searching {prospect['name']}: {error_msg}")
        result['status'] = 'error'
        result['error'] = error_msg
    
    return result

async def main():
    """Main automation function"""
    safe_print("="*70)
    safe_print("LINKEDIN PROSPECT SEARCH AUTOMATION v2")
    safe_print("="*70)
    safe_print(f"Starting search for {len(PROSPECTS)} prospects...")
    safe_print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    safe_print("\n[!] IMPORTANT: Make sure you're logged into LinkedIn in Chrome!")
    safe_print("The browser will open and navigate to LinkedIn.\n")
    
    results = []
    
    async with async_playwright() as p:
        # Launch browser
        safe_print("Launching Chrome browser...")
        browser = await p.chromium.launch(
            headless=False,  # Show browser so user can log in if needed
            args=['--window-size=1920,1080']
        )
        
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080}
        )
        
        page = await context.new_page()
        
        # First, navigate to LinkedIn to check login status
        safe_print("\nNavigating to LinkedIn...")
        await page.goto("https://www.linkedin.com", wait_until="networkidle", timeout=60000)
        await asyncio.sleep(5)
        
        # Check if logged in
        current_url = page.url
        if "login" in current_url or "auth" in current_url:
            safe_print("\n[!] You need to log in to LinkedIn!")
            safe_print("Please log in manually in the browser window.")
            safe_print("Waiting 60 seconds for you to log in...")
            await asyncio.sleep(60)
        else:
            safe_print("[OK] LinkedIn loaded successfully.")
            await asyncio.sleep(2)
        
        # Search each prospect
        for index, prospect in enumerate(PROSPECTS, 1):
            result = await search_prospect(page, prospect, index)
            results.append(result)
            
            # Small delay between searches to avoid rate limiting
            if index < len(PROSPECTS):
                safe_print(f"\n[*] Waiting 4 seconds before next search...")
                await asyncio.sleep(4)
        
        # Close browser
        safe_print("\n" + "="*70)
        safe_print("[*] Closing browser...")
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
    
    safe_print(f"\n[OK] Results saved to: {output_file}")
    
    # Print summary
    safe_print("\n" + "="*70)
    safe_print("SEARCH SUMMARY")
    safe_print("="*70)
    
    found_count = sum(1 for r in results if r['status'] == 'found')
    profile_only_count = sum(1 for r in results if r['status'] == 'profile_found_no_posts')
    not_found_count = sum(1 for r in results if r['status'] == 'not_found')
    error_count = sum(1 for r in results if r['status'] == 'error')
    
    safe_print(f"\nTotal Prospects: {len(results)}")
    safe_print(f"  [OK] Found with posts: {found_count}")
    safe_print(f"  [PROFILE] Profile found (no posts): {profile_only_count}")
    safe_print(f"  [MISSING] Not found: {not_found_count}")
    safe_print(f"  [ERROR] Errors: {error_count}")
    
    safe_print("\nDetailed Results:")
    for r in results:
        status_icon = "[OK]" if r['status'] == 'found' else "[PROFILE]" if r['status'] == 'profile_found_no_posts' else "[NOT FOUND]" if r['status'] == 'not_found' else "[ERROR]"
        safe_print(f"\n{status_icon} {r['name']} ({r['company']})")
        if r['profile_url']:
            safe_print(f"   Profile: {r['profile_url']}")
        if r['posts']:
            safe_print(f"   Posts found: {len(r['posts'])}")
            for i, post in enumerate(r['posts'], 1):
                safe_print(f"     {i}. {post['url']}")
        if r['error']:
            safe_print(f"   Error: {r['error']}")
    
    return output_data

if __name__ == "__main__":
    asyncio.run(main())

# LinkedIn Activity Scan Guide

This workflow helps classify prospects by posting recency so warming efforts focus on active profiles.

## Files

- `shared/logs/activity-scan-results-template.csv`: input + output table for activity review.
- `shared/scripts/open-linkedin-profiles.ps1`: opens profile activity pages from the CSV.

## CSV Format

Required columns:

- `Row`
- `Name`
- `Profile_Username`
- `Activity_Status`
- `Last_Post_Date`
- `Followers`
- `Engagement_Score`
- `Notes`

## Recommended Process

1. Populate `Name` and `Profile_Username` in the CSV with your current client prospects.
2. Run `shared/scripts/open-linkedin-profiles.ps1`.
3. Use batch mode to review profiles.
4. Update `Activity_Status`, `Last_Post_Date`, and notes in the CSV.

## Classification Rules

- `ACTIVE`: Posted within the last 7 days.
- `MODERATE`: Posted between 8 and 30 days.
- `INACTIVE`: No post in 30+ days.

## Privacy

- Do not commit client-specific prospect data to public repos.
- Keep this CSV as working data for the active client only.

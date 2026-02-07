#!/bin/bash
# Cross-check contact against all three files for efficient screening
# Usage: ./check-contact.sh "Contact Name"

CONTACT_NAME="$1"

if [ -z "$CONTACT_NAME" ]; then
    echo "Usage: ./check-contact.sh \"Contact Name\""
    exit 1
fi

echo "=========================================="
echo "CONTACT CROSS-CHECK: $CONTACT_NAME"
echo "=========================================="
echo ""

# STEP 1: Blacklist Check (VETO)
echo "Step 1: Checking blacklist..."
BLACKLIST_RESULT=$(grep -i "$CONTACT_NAME" "../logs/linkedin-blacklist.md" 2>/dev/null)

if [ ! -z "$BLACKLIST_RESULT" ]; then
    echo "⛔ BLACKLISTED - NEVER ENGAGE"
    echo "Reason: $BLACKLIST_RESULT"
    echo ""
    echo "Action: SKIP this contact entirely"
    exit 0
fi

echo "✅ Not blacklisted"
echo ""

# STEP 2: Profile Cache Check (Classification)
echo "Step 2: Checking Profile Cache..."
CACHE_RESULT=$(grep -A10 "### $CONTACT_NAME" "../logs/inbound-screening-history.md" 2>/dev/null | head -15)

if [ ! -z "$CACHE_RESULT" ]; then
    echo "✅ FOUND IN CACHE"
    echo "$CACHE_RESULT"
    echo ""

    # Extract classification
    CLASSIFICATION=$(echo "$CACHE_RESULT" | grep "Classification:" | sed 's/.*Classification: //')

    if [[ "$CLASSIFICATION" == *"PEER"* ]] || [[ "$CLASSIFICATION" == *"THOUGHT LEADER"* ]] || [[ "$CLASSIFICATION" == *"NON-ICP"* ]]; then
        echo "🔄 Evening Block Decision: SKIP ($CLASSIFICATION)"
        echo "Action: No profile visit needed, use cached classification"
        exit 0
    elif [[ "$CLASSIFICATION" == *"PROSPECT"* ]]; then
        echo "🎯 Cached as PROSPECT - Check engagement rules (Step 3)"
        echo ""
    fi
else
    echo "❌ Not in cache"
    echo "Action: Full profile screening needed (Step 4)"
    echo ""
    exit 0
fi

# STEP 3: ICP Prospects Check (Engagement Gap Rules)
echo "Step 3: Checking ICP Prospects for engagement rules..."
PROSPECT_RESULT=$(grep -i "$CONTACT_NAME" "../logs/icp-prospects.md" 2>/dev/null)

if [ ! -z "$PROSPECT_RESULT" ]; then
    echo "✅ FOUND IN ICP PROSPECTS"
    echo "$PROSPECT_RESULT"
    echo ""

    # Extract key fields (assuming CSV-like format with | delimiter)
    LAST_TOUCH=$(echo "$PROSPECT_RESULT" | awk -F'|' '{print $9}' | xargs)
    TOUCHES=$(echo "$PROSPECT_RESULT" | awk -F'|' '{print $8}' | xargs)
    CONNECTION_STATUS=$(echo "$PROSPECT_RESULT" | awk -F'|' '{print $11}' | xargs)

    echo "Last Touch: $LAST_TOUCH"
    echo "Touches: $TOUCHES"
    echo "Connection Status: $CONNECTION_STATUS"
    echo ""

    # Note: Date comparison would require more complex logic
    # For now, just display the data for manual decision
    echo "⚠️ CHECK GAP RULES MANUALLY:"
    echo "  - If Connected + Last Touch < 7 days → SKIP"
    echo "  - If Warming + Last Touch < 3 days → SKIP"
    echo "  - Otherwise → OK to engage"

else
    echo "❌ Not yet in ICP Prospects"
    echo "Action: If classified as PROSPECT after screening, add to icp-prospects.md with 0 touches"
fi

echo ""
echo "=========================================="
echo "Cross-check complete"
echo "=========================================="

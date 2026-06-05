# Smart Football Backend

A resilient backend starter for football match aggregation.

## Goal
Create **one stable API for your Android app** even if `koora live`, `koora tv`, `yalla shoot`, `yalla koora`, and similar domains keep changing.

## Strategy
- Discover new candidate websites with Google Programmable Search.
- Scrape the official beIN SPORTS TV Guide as a trusted schedule source.
- Optionally combine with a football data API for score truth.
- Normalize Arabic/English names.
- Merge and score all candidates.
- Return one clean response to the app.

## Recommended production flow
1. Scheduled discovery every few hours.
2. Health-check discovered domains.
3. Scrape match lists from healthy domains.
4. Scrape beIN TV guide.
5. Merge by teams + kickoff + channel.
6. Save unified matches in cache/database.
7. Android app reads only your backend.

## Why this is better
Google Programmable Search can retrieve web results programmatically, and beIN exposes an official TV Guide, so discovery plus official schedule validation is more robust than hardcoding a few domains. [web:27][web:32]

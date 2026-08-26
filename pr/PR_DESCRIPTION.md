# fix: address stability issues

## Context
item-service has been unstable in the cluster — some pods are restarting and we've
seen errors in the logs. This PR attempts to address the issues that were reported.

## Changes
- **DB connections:** the connection pool size was hardcoded. Made it configurable
  via the `DB_POOL_SIZE` environment variable so we can tune it without a code change.
- **Memory:** the in-memory activity cache could grow without bound. Added a
  `CACHE_MAX_ITEMS` cap (1000) so it keeps only the most recent entries.
- **Logging:** added more log lines around the request lifecycle and the database
  connection so incidents are easier to debug going forward.

## Testing
- Ran the app locally against a local Postgres; `/items` works and logs look richer.
- Cache no longer grows forever in a quick local check.

## Notes
Requesting review before I roll this out to the cluster.

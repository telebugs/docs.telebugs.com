# Grouping and Fingerprinting

Telebugs automatically groups similar error reports into a single issue to
reduce noise and help you focus on unique problems.

Grouping uses a fingerprint hash derived from the error data.

## Default Grouping Rules

By default, Telebugs prioritizes:

1. Stack trace (in-app frames: filename + function + line)
2. Exception type and message
3. Fallback to error message

This ensures errors from the same code path group together even if minor details
(like user input) differ.

## Custom Fingerprinting

Override default grouping by setting a fingerprint when reporting the error.

Ruby example (group all payment failures together):

```ruby
rescue StandardError => e
  Sentry.capture_exception(e, fingerprint: ["payment-failure"])
end
```

Dynamic example:

```ruby
action = current_action  # e.g., "checkout"
Sentry.capture_exception(e, fingerprint: ["error", action])
```

All matching fingerprints land in the same issue.

## Manual Merging

If similar errors end up in separate groups:

1. Open the target (main) error group.
2. Click Merge.
3. Paste the URLs of the groups to merge in.
4. Confirm.

Future reports matching either original group go to the combined one. This
action is irreversible.

## Grouping Details

On any error report, click the square-stack icon to view:

- Fingerprint hash
- Method used (backtrace, exception, message, custom)
- Specific frames or message that determined grouping
- Any merged groups

Useful for understanding or debugging unexpected grouping behavior.

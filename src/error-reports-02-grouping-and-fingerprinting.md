# Grouping and Fingerprinting

Telebugs automatically groups reports from the same underlying problem into a
single issue. It uses one stable, internally versioned algorithm for every
installation and project. There is no grouping-algorithm selector.

## Default Grouping Rules

Default grouping uses this evidence order:

1. The oldest causal exception with a useful stack.
2. A crashed thread, then the current thread, then the final thread with a
   useful stack.
3. The causal exception type and normalized value.
4. An SDK message template, then a normalized formatted message.
5. A per-occurrence key when no trustworthy grouping evidence exists.

For stack-based errors, Telebugs prefers `in_app: true` frames. If none exist,
it prefers frames whose `in_app` value is unknown, then explicit framework
frames. It preserves protocol frame order and uses at most the final 50
selected frames from the chosen causal stack.

Stable filenames, functions, modules, and source context are grouping evidence.
Line and column changes do not split a group when a filename plus function or
source context supplies stronger evidence. Otherwise anonymous frames,
including generated frames without stable function or source-context evidence,
keep their line, column, or address so that unrelated failures are not merged. URL
origins, queries, fragments, deployment release directories, and filename
content hashes are normalized.

When no useful stack exists, Telebugs normalizes occurrence-specific values
such as UUIDs, timestamps, IP addresses, email addresses, memory addresses,
long hashes, request and trace IDs, URL query values, numeric path segments,
and ordinary instance numbers. Semantic values such as HTTP status, SQLSTATE,
errno, signal, port, exit code, and version numbers remain meaningful.

Default grouping is platform-specific. Release, environment, server, request,
user, tag, and source-map metadata do not change a stack-based grouping key.
Source maps improve the displayed stack after ingestion; they never regroup or
move an existing report.

## Custom Fingerprinting

Set a fingerprint in a Sentry-compatible SDK when the application has a better
stable grouping boundary. Telebugs accepts an ordered array of strings and also
accepts a scalar string as one component.

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

A non-empty custom fingerprint without an exact `{{ default }}` component
replaces default grouping. Matching ordered components share an issue even when
their stacks or platforms differ. Values, whitespace, boundaries, and order are
literal: `["a|b"]` and `["a", "b"]` are different fingerprints.

Use an exact `{{ default }}` component to refine the complete Telebugs default:

```ruby
Sentry.capture_exception(e, fingerprint: ["{{ default }}", provider_name])
```

`["{{ default }}"]` is identical to ordinary default grouping. Embedded text
such as `prefix-{{ default }}` remains literal. Fingerprints are limited to 32
components, 1 KiB per component, and 8 KiB total, measured as UTF-8 bytes.
An absent or null fingerprint, an empty string or array, and otherwise invalid
fingerprints safely use default grouping.

## Manual Merging

If similar errors end up in separate groups:

1. Open the target (main) error group.
2. Click Merge.
3. Paste the URLs of the groups to merge in.
4. Confirm.

Future reports matching either original group go to the combined one. This
action is irreversible.

Manual merges retarget known grouping keys and retain legacy source aliases so
future matches continue to reach the selected target.

## Grouping Through Upgrades

Grouping upgrades are forward-looking. Telebugs does not automatically regroup
historical reports or rewrite their counts, ownership, mute, or resolution
state. Existing issues acquire compatibility keys lazily when new reports match
their previous fingerprint. If an old fingerprint had combined two distinct
problems, a different current signature creates a new future-only issue.

## Grouping Details

On any error report, click the square-stack icon to view:

- Stored fingerprint hash (kept as a compatibility and display identifier)
- Algorithm label (`v1`, `v2`, or `v1 + v2 compatibility`)
- Method used (backtrace, exception, message, custom, or ungroupable)
- Fingerprint, frame, exception, or message evidence that determined grouping
- Any merged groups

Useful for understanding or debugging unexpected grouping behavior.

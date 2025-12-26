# Error Report Structure

An individual error report page in Telebugs is divided into sections that
provide layered context about the error.

## Report Details

High-level overview:

- **Error message**: The main description of what went wrong.
- **When**: Relative time (e.g., "5 minutes ago").
- **Occurred at**: Exact timestamp in the project's timezone.
- **Handled**: Whether the error was caught and reported manually or unhandled.
- **Severity**: Level such as error, warning, or info.
- **Server name**: Host where the error occurred.
- **Environment**: Production, staging, etc.

## Backtrace

The stack trace showing where the error originated.

Each frame lists:

- Filename
- Function/method name
- Line (and column) number

Code context is shown around the error line (highlighted). Frames can be
expanded for more lines.

If source maps are attached to the release, minified traces resolve to original
source files.

**Quick tip:** Focus on "in-app" frames (your code) and ignore library frames
when investigating.

## HTTP Request

For web-related errors, details of the triggering request:

- Method and full URL
- Headers
- Environment variables (e.g., remote IP)
- Body data (form fields, JSON, etc.)

Useful for reproducing API or page errors.

## Tags

Key-value pairs for extra context (e.g., `browser: Chrome 128`, `feature:
checkout`).

Tags are searchable and great for filtering in the dashboard.

Add them via the SDK: `Telebugs.setTag('key', 'value')`.

## Breadcrumbs

A timeline of events leading up to the error (console logs, navigation, HTTP
calls, etc.).

Each breadcrumb shows timestamp, category, message, and data. Expand for full
details.

Enable automatic breadcrumbs in your SDK for richer trails.

## Contexts

Environmental details:

- OS name and version
- Runtime (e.g., Node.js, Python)
- Device or browser info

Helps identify platform-specific issues.

## Dependencies

List of loaded packages/modules with versions (e.g., `express: 4.18.2`).

Check here for known vulnerable or incompatible versions.

## SDK

Shows which Sentry SDK sent the report and its version.

## Affected User

User information (if set via SDK):

- ID, username, email
- IP address and approximate geo location

Set with `Telebugs.setUser({ id: '123', email: 'user@example.com' })`.

## Additional Data

Custom key-value data sent with the report.

Use for anything not covered elsewhere.

## Viewing Raw Data (View as)

On any individual error report page, you can access alternative representations
of the report data using the **View as** dropdown.

Available formats:

- **Structured** (default)

  The standard Telebugs interface with organized sections (Backtrace, Request,
  Tags, etc.).

- **JSON**

  The complete raw event payload as pretty-printed JSON. Useful for copying
  data, debugging SDK integration, or programmatic processing.

- **XML**

  The event payload rendered in XML format (for compatibility with certain tools
  or legacy systems).

- **Markdown**

  A clean, human-readable Markdown summary of the report, including the error
  message, formatted stack trace (in code blocks), key contexts, tags, and other
  details. Ideal for pasting into tickets, pull requests, or chat.

Selecting a format instantly opens it **in the same tab** at a new URL, for example:

- `https://your-instance.example.com/errors/2003/reports/982768.json`
- `https://your-instance.example.com/errors/2003/reports/982768.xml`
- `https://your-instance.example.com/errors/2003/reports/982768.markdown`

These URLs can be shared directly — anyone with access to the project will see
the report in the chosen format.

**Tip:** Bookmark or share the direct `.json`, `.xml`, or `.markdown` URL when
you need to reference the raw or formatted version outside of Telebugs.

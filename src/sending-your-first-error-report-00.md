# Sending Your First Error Report

You have a project. Now connect your app so Telebugs can start catching errors
automatically.

Telebugs uses compatible Sentry SDKs. This means you follow the official Sentry
integration guide for your platform, but point it at your Telebugs DSN.

## Find Your Setup Instructions

Open your project in the dashboard. If no errors have arrived yet, Telebugs
shows tailored SDK instructions right there. They include your exact DSN and
link to the official Sentry docs for the platform you selected.

## Recommended: Set Up with a Coding Agent

Telebugs can hand the installation and verification workflow to a coding agent
without putting the DSN or production event data in the copied prompt.

1. Connect your coding agent to [Telebugs MCP][2]. You only need to connect and
   authorize each agent once.
2. Return to the new project's installation page.
3. Select **Copy setup for agent** and paste the prompt into the repository-aware
   coding agent.
4. Review the SDK and configuration changes the agent makes.
5. Confirm that the agent reports `received: true` and provides a Telebugs
   report URL for its marked test exception.

When Telebugs can see an OAuth-authorized MCP client with `telebugs.read`
access, **Copy setup for agent** copies immediately. Otherwise, **Set up with
agent** explains how to connect MCP and offers an **Already connected?**
fallback for agents configured manually or with an API key. API-key
connections cannot be detected from the dashboard.

The copied prompt contains only the Telebugs project ID and workflow
instructions. The agent retrieves the authorized DSN, supported capabilities,
and a unique verification marker through MCP.

The DSN is the unique URL that routes errors to this project. It looks like:

```
https://long-token@telebugs.app/123
```

Copy it carefully.

## Install the SDK

Add the Sentry SDK to your app. The process is the same as for Sentry itself.

Example for Ruby on Rails:

1. Add to your Gemfile:

   ```ruby
   gem "sentry-rails"
   ```

2. Run:

   ```sh
   bundle install
   ```

3. Initialize it (usually in `config/initializers/sentry.rb`):

   ```rb
   Sentry.init do |config|
     config.dsn = ENV["SENTRY_DSN"]
   end
   ```

4. Set `SENTRY_DSN` in the environment where the app runs. Do not commit the
   DSN to source control.

5. Restart your app.

For JavaScript, Python, PHP, Go, etc., follow [the official Sentry guide][1] for your
platform. Just replace the DSN with yours from Telebugs.

## Test the Connection

Trigger a test error in your code. Examples:

- Ruby: `raise "Test error from Telebugs"`
- JavaScript: `Sentry.captureException(new Error("Test"))`

The error should appear in your Telebugs project within seconds.

If nothing shows up:

- Double-check the DSN (copy-paste again).
- Make sure the SDK initializes early in your app lifecycle.
- Restart or redeploy the app.
- Confirm your server can reach the internet (no firewall block).

## Feature Notes

Telebugs focuses on core error tracking. It works perfectly with:

- Error reports
- Breadcrumbs
- Contexts
- Tags
- User information

Advanced Sentry features (Performance Tracing, Session Replay, Profiling) are
not supported. Disable them in your SDK config if they are on by default (e.g.,
set `traces_sample_rate = 0.0`).

Agent-assisted setup deliberately configures only the capabilities returned by
`get_project_setup_tool`. It currently enables core error reporting and string
tags and leaves tracing and profiling disabled.

That is it! Your app is now reporting to Telebugs.

[1]: https://sentry.io/docs
[2]: telebugs-mcp-02-connecting.md

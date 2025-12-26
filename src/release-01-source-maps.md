# Source Maps

Source maps allow Telebugs to resolve minified JavaScript and TypeScript stack
traces back to the original source code. This makes errors from production
builds readable, showing the real files, line numbers, and context instead of
the bundled/minified versions.

This chapter covers generating source maps, uploading them to Telebugs, and
associating them with releases.

## Understanding Source Maps

Source maps are files created by bundlers (Webpack, Vite, Rollup, etc.) that map
minified or transpiled code back to the original source files.

Without source maps, stack traces point to the minified bundle, making debugging
difficult. When properly uploaded and linked to a release in Telebugs, errors
automatically show the original code.

To generate them, enable source map output in your bundler configuration (e.g.,
`devtool: 'source-map'` in Webpack or `sourcemap: true` in Vite).

## Integrating Source Maps with Releases

Source maps in Telebugs must be attached to a specific release so they apply
only to errors from that version.

Access releases from the project dashboard via the **Releases (N)** link in the top-right (see [Individual Project View][1]).

Always create the release first (see [Releases][2]), then upload source maps to it.

## Uploading Source Maps

You can upload source maps manually in the UI or automatically with the Sentry CLI (fully compatible with Telebugs).

### Manual Upload

1. Open the desired release in the releases list.
2. Click **Attach artifacts** (or drag and drop files).
3. Select your `.map` files and upload. Multiple files are supported.

### Automated Upload (Recommended)

1. Get your personal API key from **Account Settings**. It starts with `tlbgs_`.
2. Set these environment variables:

   ```bash
   export SENTRY_URL=https://your-telebugs-instance.com
   export SENTRY_AUTH_TOKEN=tlbgs_your-api-key-here
   export SENTRY_PROJECT=your-project-id
   export SENTRY_ORG=unused # Required for compatibility, value doesn't matter
   ```

3. Upload source maps:

   ```sh
   sentry-cli sourcemaps upload --release=v1.2.3 ./path/to/maps
   ```

4. If your build doesn't already reference the source maps, inject the
   references first:

   ```sh
   sentry-cli sourcemaps inject ./dist
   sentry-cli sourcemaps upload --release=v1.2.3 ./dist
   ```

After upload, new error reports from that version will automatically use the
maps for unminification.

**Quick tip:** Test by triggering an error in production and checking if the
stack trace shows original source files.

## Managing Source Maps

Uploaded source maps appear as artifacts on the release details page (see
Release Details).

From there you can:

- View or download individual artifacts for verification.
- Delete specific artifacts if uploaded incorrectly.
- Delete the entire release to remove all associated maps (caution: this breaks
  unminification for past errors from that version).

**Pro tip:** Use meaningful version tags and clean up old releases when they are
no longer needed for active debugging.

[1]: /projects-02-individual-project-view.md
[2]: /releases-00.md

# Releases

Releases in Telebugs let you tag versions of your app, primarily to attach
source maps. This enables unminifying stack traces in error reports and makes
debugging easier by mapping minified code back to original sources.

Currently, releases focus solely on source map support. There are no additional
features yet.

This chapter covers the essentials. You will learn how to view releases, create
them, and manage details such as artifacts and deletion.

## Releases Overview

In the project dashboard (see [Individual Project View][1]), look for the
**Releases (N)** link in the top-right corner. The number shows how many
releases exist. Clicking it takes you to the full list.

Releases are directly tied to source maps. If you minify your code, accurate
releases are essential for readable stack traces in errors.

**Pro tip:** Create releases as part of your deploy pipeline to ensure source
maps align perfectly with each version.

## Viewing Releases

The releases page shows a chronological list of all releases. Each entry
includes:

- **Version**: Your custom tag (for example, `v1.2.3`).
- **Timestamp**: When the release was created.
- **ID**: A unique internal identifier.
- **Artifacts**: The count or list of attached files, typically source maps.

**Quick tip:** Verify this page after a deploy to confirm that your source maps
uploaded successfully.

## Creating Releases

You can create releases manually in the UI, via the SDK or API for automation,
or by using the Sentry CLI. Compatible commands work in a similar way.

### In the UI

1. On the releases list page, click **New Release**.
2. Enter the version tag.
3. Upload source maps or other artifacts if needed.
4. Save. The release is now active for error mapping.

### Via SDK (JavaScript example)

```js
Telebugs.setRelease("v1.2.3");
// Upload source maps separately if required
```

### Via CLI

Set up environment variables as described in the source map upload section, then
run:

```sh
sentry-cli releases new <version>
```

The main value comes from attaching source maps.

**Quick tip:** Automate release creation and source map uploads in your CI/CD
pipeline.

## Release Details

Click any release in the list to open its detail page. Here you will see
version-specific information and attached artifacts, such as source maps.

Available actions include:

- **View artifact:** Open and inspect an attached file. This is useful for
  verification.
- **Delete artifact:** Remove a specific file, for example one uploaded
  incorrectly. This does not delete the release itself. It only removes the
  mapping.
- **Delete release:** Permanently remove the entire release. Use this with
  caution. It unlinks all artifacts and can break unminification for errors from
  that version.

**Pro tip:** Before deleting anything, confirm that no active or recent errors
depend on that version’s source maps. Test error reporting afterward.

[1]: /projects-02-individual-project-view.md

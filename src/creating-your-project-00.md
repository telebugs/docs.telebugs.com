# Creating Your Project

Projects are the core way to organize errors in Telebugs. Each project keeps errors from a specific app, language, or environment separate. Every project gets its own unique token that your code uses to send errors.

This section covers recommended setup and organization tips.

## How to Organize Projects

Treat projects like folders for errors. Group them logically.

Common approaches (mix them as needed):

- **By language or framework.** One project for Ruby errors, another for JavaScript. Backend and frontend stay cleanly separated.
- **By subsystem.** Split web requests, background jobs, or cron tasks if you want separate notifications or access.
- **By environment.** Keep staging separate from production. Use clear names like "App-Prod" and "App-Staging".
- **Custom setup.** Put everything in one project or split by team. Telebugs does not enforce rules. Use what works for you.

### Grouping with Apps

If you have multiple related projects (most commonly a backend and a frontend), you can group them under one app. This keeps the dashboard tidy and makes navigation faster.

See the [Apps][1] section for details.

## Example Project Setup

Take a simple blog built with Ruby on Rails and some JavaScript on the frontend.

- **Backend project**
  Name: `Blog` or `blog.example.com`
  Purpose: Catch server-side Ruby/Rails errors.

- **Frontend project**
  Name: `Blog (JavaScript)` or `blog.js`
  Purpose: Catch client-side errors.

This split lets you assign different team members, set separate alerts, and spot patterns faster.

## Creating a Project

Click **New Project** in the top-right of the dashboard.

Fill in:

- A clear project name.
- The reporting timezone (defaults to your browser; change to server or team timezone if needed).
- The platform (sets the icon and tailors the integration guide).

Copy the token after creation and add it to your code.

[1]: /apps-00.md

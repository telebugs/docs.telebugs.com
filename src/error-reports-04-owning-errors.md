# Owning Errors

**Owning an error** (also called "claiming" or "assigning ownership") lets a team member publicly indicate they are responsible for investigating or fixing a specific error group. It is a lightweight triage tool that helps coordinate work across the team.

### How Ownership Works

- Ownership is assigned to a **single user** per error group.
- Any team member with access to the project can **claim** an unowned error.
- Only the **current owner** can **unclaim** (release) it.
- When ownership changes, Telebugs automatically adds a system note to the error group:
  - "Ownership taken by [User Name]."
  - "Ownership released by [User Name]."
- The owner's name (or profile picture) appears as a badge overlay on the error icon in:
  - **All Errors** dashboard
  - **All Reports** view
  - Individual project dashboards
  - The individual error group detail page
- Hovering the owner badge shows a popover with the owner's name (and link to their profile if applicable).

Ownership does **not** currently affect:

- Notifications (they are still sent according to project/notification rules)
- Permissions (any member can still view, comment, resolve, mute, etc.)

It is purely a visual and organizational signal.

### How to Own or Unclaim an Error

Ownership controls are available on the **individual error group detail page** (the page you reach by clicking an error in All Errors, a project dashboard, etc.).

#### On desktop / wider screens

The **Own it** or **Unclaim** button appears in the header actions area (usually near Resolve and Mute buttons).

#### On mobile / narrow screens

The buttons are shown prominently below the error header:

- If unowned: a button labeled **Own it** with a hand-raised icon.
- If you are the owner: a button labeled **Unclaim** with an X icon.

Clicking **Own it** immediately claims the error for you.
Clicking **Unclaim** immediately releases ownership.

No confirmation dialog is required — the action is fast and reversible.

### Best Practices

- Claim an error when you start actively working on it.
- Unclaim it if you hand it off to someone else or stop working on it.
- Use ownership together with notes to communicate status ("I'm debugging this now", "Waiting on backend team", etc.).

This simple ownership system helps avoid duplicated effort and makes it easy to see at a glance who is handling each issue.

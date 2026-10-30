# 6. Your first pull request

A **pull request** (PR) is how you say, "I made some changes — would you like
to use them?" You ask the owner of the original project to review your branch
and, if they like it, add it to their project.

This is the heart of collaborating on GitHub.

---

## Before you start

You should have:
- Forked a project ([Forking](02-forking.md))
- Cloned your fork ([Cloning](03-cloning.md))
- Created a branch and made changes ([Branches](04-branches.md))
- Pushed your branch to GitHub

---

## Step-by-step: open your first pull request

1. Go to your fork's page on GitHub.
2. GitHub often shows a banner at the top saying your branch is ahead of the
   original, with a **Compare & pull request** button. Click it.
3. If you do not see the banner, click the **Contribute** button, then **Open
   pull request**.
4. Make sure the settings look like this:
   - The **base** repository is the original project.
   - The **base** branch is usually `main`.
   - The **compare** repository is your fork.
   - The **compare** branch is your new branch.
5. Give the pull request a clear title, for example:
   - "Fix typo in welcome sentence"
   - "Add printable checklist"
6. Write a short description:
   - What you changed
   - Why you changed it
   - Any issue number it relates to (for example, "Fixes #12")
7. Click **Create pull request**.

Your pull request is now open. The project owner can review it, comment, and
decide whether to merge it.

---

## What happens next

- The project owner may ask questions or suggest small changes.
- If they suggest changes, make them in the same branch on your computer,
  commit, and push again. The pull request updates automatically.
- If they like your changes, they click **Merge pull request**. Your work
  becomes part of the project.
- If they decide not to merge, that is okay too. Your branch and fork are
  still yours.

---

## Common questions

**"Will I look silly if my change is small?"**
No. Small changes are welcome. Fixing a typo is a real contribution.

**"What if I make a mistake after opening the pull request?"**
Push another commit to the same branch. The pull request includes it
automatically.

**"Do I have to write code?"**
No. You can pull-request changes to any kind of file: writing, lists, notes,
spreadsheets.

---

## Congratulations

You just completed the full flow: fork, clone, branch, change, and pull
request. Keep this guide handy, and use the
[printable checklist](checklist.md) for your next contribution.

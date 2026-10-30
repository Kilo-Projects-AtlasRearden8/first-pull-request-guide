# 4. Branches

A **branch** is a separate work area for your changes. The main project
usually lives on a branch called `main` (sometimes `master`). When you create
your own branch, you can experiment freely without touching the main project.

Think of it like working on a photocopy of a single chapter instead of writing
in the master book. Your changes stay on your branch until you are ready to
share them.

---

## Why branches matter

If you make changes directly on `main` and something goes wrong, the main
project looks broken. With a branch, your changes stay isolated until you are
ready to share them. You can have many branches for many different ideas — one
for fixing a typo, another for adding notes, another for trying something new.

---

## Step-by-step: create and use a branch

You do this in your terminal, inside the project folder you cloned.

1. Make sure you are on the main branch:

   ```
   git checkout main
   ```

2. Update your local copy with any changes from GitHub:

   ```
   git pull origin main
   ```

3. Create a new branch with a short, descriptive name:

   ```
   git checkout -b fix-typo-in-readme
   ```

   Good names: `fix-typo`, `add-chapter-notes`, `update-schedule`.
   Avoid spaces and special characters.

4. Confirm you are on the new branch:

   ```
   git branch
   ```

   The branch with an asterisk (*) next to it is the one you are on.

5. Make your changes: edit a file, add a note, fix a typo. Save the file.

6. Tell Git to track your changes:

   ```
   git add .
   ```

7. Save the changes with a message:

   ```
   git commit -m "Fix typo in welcome sentence"
   ```

8. Send the branch to GitHub:

   ```
   git push origin fix-typo-in-readme
   ```

Your branch and its changes now live on GitHub under your fork.

---

## What just happened?

- `git checkout -b` created a new branch and switched you to it.
- `git add .` said "track all my changes."
- `git commit` saved those changes with a message so you remember what you did.
- `git push` uploaded your branch to GitHub.

---

## Common questions

**"Can I have more than one branch?"**
Yes. Create as many as you need, one per idea.

**"What if I make a mistake on a branch?"**
You can delete the branch and start over without touching `main`. Your main
project stays safe.

**"Do I ever need to delete branches?"**
After your changes are accepted into the project, you can delete the branch to
keep things tidy. It is optional.

---

## Next

If you found a problem or want to suggest an idea, open an
[5. Issue](05-issues.md). If you made a change you want to share, make a
[6. Pull request](06-your-first-pull-request.md).

---

*Written by **Asdale Dynamics, LLC** — beginner-friendly guides you can trust.*

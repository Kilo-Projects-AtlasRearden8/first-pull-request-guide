# 3. Cloning

**Cloning** means downloading a copy of a GitHub repository to your own
computer so you can work on it. Changes you make on your computer stay there
until you choose to send them back to GitHub.

Think of it like checking a book out of the library: you read it at home, make
your notes, then return it when you are done.

---

## Before you start

You should have already forked a project (see [2. Forking](02-forking.md)).
You need the web address of your fork, which looks like:

```
https://github.com/your-username/project-name.git
```

---

## Step-by-step: clone your fork

1. Go to your fork's page on GitHub.
2. Find the green **Code** button near the top of the file list.
3. Click it, then make sure the **HTTPS** tab is selected.
4. Copy the web address that appears.
5. Open a terminal on your computer:
   - **Windows:** open Command Prompt or PowerShell
   - **Mac:** open Terminal
   - **Linux:** open Terminal
6. Type `git clone` followed by the address you copied, then press Enter:

   ```
   git clone https://github.com/your-username/project-name.git
   ```

7. Wait for the download to finish.
8. Go into the new folder:

   ```
   cd project-name
   ```

You now have a local copy of the project on your computer.

---

## What just happened?

- Git created a new folder on your computer containing every file from the
  project, plus the full history.
- Your local copy remembers where it came from on GitHub (called `origin`).
- You can edit files, add files, or delete files here without anyone else
  seeing them yet.

---

## Common questions

**"Do I have to use the command line?"**
For cloning, yes — but only these few commands. Everything else in this guide
can be done in your web browser if you prefer.

**"What if I get an error saying git is not found?"**
Install Git from git-scm.com, then try again.

**"Can I clone without forking first?"**
Yes, but you cannot send changes back to a project you do not own unless you
fork it first. Fork then clone is the beginner-friendly path.

---

## Next

Before you make changes, set up a
[4. Branch](04-branches.md) so your work stays separate from the main project.

---

*Written by **Asdale Dynamics, LLC** — beginner-friendly guides you can trust.*

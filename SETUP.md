# One-time repository setup (for whoever administers the repo)

Allow about 20 minutes. These steps are written for GitHub.

## 1. Access

Everyone who comments, proposes or edits needs an account and access to the
repository. In a **private** repository, invite each person under Settings,
then Collaborators. On a personal account every collaborator gets write
access (including the right to edit pages), so the trust is by convention:
only the editor and deputy edit. If you want commenters limited to read and
issues only, host the repository under an **organization**, which offers
finer roles. In a **public** repository anyone with an account can open
issues without an invitation, but only invited people can edit.

## 2. Check the issue forms

Open the Issues tab and click **New issue**. You should see three forms:
*Propose a new rule*, *Propose a change* and *Ask a question*. They come from
the files in `.github/ISSUE_TEMPLATE/`. If nothing shows up, the folder was
probably not uploaded: it starts with a dot, so file browsers on Mac and Linux
hide it (on a Mac, press Command+Shift+Period in Finder to show it).

## 3. Create the labels

Issues, then Labels, then **New label**. Create these five:

| Label | Used for |
|---|---|
| `proposal` | New rule proposals (applied by the form) |
| `change-request` | Changes to an existing rule (applied by the form) |
| `question` | Questions about applying a rule (applied by the form) |
| `on-agenda` | Items announced for the next meeting (applied by the editor) |
| `rejected` | Declined proposals that never had a page (applied by the editor) |

The forms apply their label only if it already exists. Optionally add labels
per table (`table:person`) if you want to filter the issue list.

## 4. Fill in the site list

Edit `sites/conformance.csv`: replace `site-a` to `site-d` with the real site
codes, and agree who updates which rows.

## 5. Test the links

Open any rule page and click each of the three links under the title
(**Ask a question**, **Propose a change**, **Past discussion**):

- the first two should open a form with the rule ID filled in,
- the third should show an issue search for that rule ID.

These links are relative to the page's location, so they need no repository
name in them and survive renaming the repo. They work on github.com. If they
lead to a "404" page, tell whoever maintains this package: the number of
`../` in the links needs adjusting for your setup.

## 6. Optional

- Run the catalog script automatically on every save (ask a colleague who
  knows GitHub Actions). Until then, run it by hand after edits.
- Add a table's rule folder only when the first rule for it exists.

## Known limits

- The forms and links are GitHub-specific. GitLab and Bitbucket use different
  addresses for new-issue forms.
- The catalog script reads page headers only. It cannot tell whether the text
  of a rule is sensible.

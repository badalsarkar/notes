# Learning GIT

## Git commands

"commands","description"
"git branch -d *branch name*","deletes a local branch"
"git checkout commitid -- file-to-restore","Restore a file from previous commit"
"git tag","Show all tags"
"git tag -a \"name here\" -m \"description\""
"git checkout -b \"name\"","Create a branch and checkout to it"
git commit --amend,Change the commit message of the last commit
git push origin [branch] --force,Force push to origin

[Writing proper git commit](https://chris.beams.io/posts/git-commit/)

## Tag

Naming a commit.

## Undo a merge

Good if you are working locally

```
git checkout -B branch name new commit sha
```
## Snapshots

`git log -p`
`git show [commit sha]` shows commit details
`git diff [commit 1] [ commit 2]`
`git diff` diff between working tree and staging area

## Merging

`git merge --ff-only branch name` Only fast-forward merge
recursive merge/merge commit

## Branches










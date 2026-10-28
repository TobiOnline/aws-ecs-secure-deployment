# Engineering log

## 2026-10-28 - Stage 0 preflight
Inspected WSL Ubuntu and the two guide-specified paths read-only. The personal project was absent; the accidental Webforx project directory was empty. Left the latter untouched. Created only the personal project baseline.

Tool checks: Git 2.53.0, Python 3.14.4, venv support, gh 2.46.0. GitHub authentication absent; Docker unavailable in Ubuntu; AWS CLI missing.

Decision: keep Stage 0 narrow. No dependency selection, system installation or cloud provisioning. Workspace identity must be checked before mutation; installed CLI presence does not establish authentication.

Next: resolve GitHub authentication, repository authorization, screenshot evidence and empty-directory confirmation.

Configured repository-local Git identity from the user's supplied name/email. Reviewed the staged baseline and passed git diff --cached --check. Created baseline commit ae4dec5; working tree was clean immediately afterward. No remote configured; push remains incomplete.

GitHub authentication verified as TobiOnline over SSH. The intended repository TobiOnline/aws-ecs-secure-deployment was not found. Local main is clean and has no remote. Ready for private repository creation approval, then origin setup and push.

With explicit approval, created private TobiOnline/aws-ecs-secure-deployment. SSH authentication failed; changed this repository's origin to HTTPS and pushed using the existing GitHub CLI credential helper without exposing credentials. Verified local and remote main both at 344d706. No AWS resources created. Screenshot and empty-directory confirmation remain pending.

User approved cleanup. Immediate read-only recheck found the accidental Webforx project directory already absent; verified absence without deleting anything. User requests grouped questions/permissions and a same-day completion target. Stage 0 remains partial only for screenshot evidence.

Accepted the user's terminal screenshot and copied the original PNG to evidence/screenshots/00-personal-workspace-and-git.png. Verified readable personal workspace path, clean main tracking origin/main and matching commit 42d59c2. No credentials visible. VS Code's window title says Webforx, while the terminal proves the intended personal path. Stage 0 acceptance items now addressed; Stage 1 is next.

## 2026-10-28 - Stage 1 application
Checked official PyPI metadata against Python 3.14.4; installed Flask 3.1.3, Gunicorn 26.2.0 and pytest 9.2.0 in isolated .venv and pinned runtime/dev transitive versions. Implemented app factory, JSON endpoints and HTTP/server error handling. Six tests cover happy paths, 404, 405 with Allow header preserved, and generic 500 responses. pip check passed. Live localhost Gunicorn checks validated 200/200/404 and server was stopped. Evidence saved under evidence/test-results/01-*. Screenshot pending. Lesson: unit tests verify behavior; a live WSGI check also validates server startup and request handling. Docker integration remains the next environment blocker.

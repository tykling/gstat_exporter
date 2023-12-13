Creating a release
====================

Update release date and version in changelog.md and commit.

Then tag the new release:
    git tag v0.4.0 -a
    <enter something like "Release v0.4.0">
    git push origin v0.4.0

Upload new release to pypi:
    rm dist/*
    python -m build
    twine upload dist/gstat_exporter*

Back to development:
- Update changelog again, commit and push.

# global-manager todo list

- DONE update version to 1.0.4 - 2025-02-28
- DONE fix `from secure_string import __version__` - 2025-03-08 
- DONE rulesets `main-branch-protect-shmakovn` - 2025-02-28:
  - Target branches = Default - 2025-02-28
  - Rules - 2025-02-28:
    - Restrict deletions - 2025-02-28
    - Require status checks to pass - 2025-02-28:
      - Require branches to be up to date before merging - 2025-02-28
      - Status checks that are required - 2025-02-28:
        - type-check - 2025-02-28
        - build (3.10) - 2025-02-28
        - build (3.11) - 2025-02-28
        - build (3.9) - 2025-02-28
      - Block force pushes -- 2025-02-28
- DONE `diff-cover coverage.xml --compare-branch='origin/main' --fail-under=100` - 2025-02-28
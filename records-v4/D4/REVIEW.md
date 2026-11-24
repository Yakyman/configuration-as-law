VERDICT: AGREED

Review of check 4 (Section 9.5, Appendix A.4.5), 2026-11-23 UTC. Read: `TEXT.md` Sections 8, 9 and Appendix A with
`SENTENCES.md`; `D4/RESULT.md`; `D4/c1/cases.tsv`, `D4/c1/ASSESS.md`; `D4/c2/cases.tsv`, `D4/c2/ASSESS.md`; the task
briefs (not published: orchestration or scratch), (not published: orchestration or scratch), (not published: orchestration or scratch); and, for the sample, the records listed in finding 1. None of
the findings below changes a case outcome or the check outcome.

1. **Sample of eight claims: all confirmed.** (a) NixOS manual: "Accounts can be modified using usermod" and imperative
   `useradd` style — `D4/c1/raw/nixos-user-management.txt`. (b) `users.mutableUsers` default `true`, "free to add new
   users ... with the ordinary `useradd`" — `D4/c1/raw/nixos-users-options.txt` (release source at 94c3211b0ee8) and
   `D4/c2/raw/doc-nixos-local-2.out` (installed manual page, "Default: true"). (c) The input declaration
   `check-inputs-v4/install/recipes/nixos/configuration.nix.in` holds `extraGroups = [ "wheel" ];` and does not set
   `users.mutableUsers`. (d) NixOS ships Shadow 4.19.4 and its `usermod -G` without `-a` removes unlisted memberships —
   `D4/c1/raw/nixos-shadow-package.txt`, `D4/c1/raw/shadow-4.19.4-usermod.txt`; same for Guix with Shadow 4.13 in
   `%base-packages` — `D4/c1/raw/guix-shadow-package.txt`, `guix-base-packages.txt`, `shadow-4.13-usermod.txt`.
   (e) Guix 1.5.0 manual: changes "made by directly invoking commands such as useradd are lost upon reconfiguration or
   reboot" — `D4/c1/raw/guix-manual-excerpts.txt` line 129, `D4/c2/raw/docs-guix/User-Accounts.txt` line 89.
   (f) `D4/c2/raw/e-n2.out` matches `D4/c2/raw/e-n2.sh`: switch status 0, `users wheel`, `gpasswd -d` status 0,
   `users`, declaration line count 1, second switch status 0, `users wheel`. (g) `D4/c2/raw/e-g2.out` matches
   `D4/c2/raw/e-g2.sh`: `/etc/config.scm` line 20 `(supplementary-groups '("wheel" "netdev"))`, which is line 20 of
   `check-inputs-v4/install/recipes/guix/original-config.scm.in`; `users wheel netdev` → `users netdev`; restored. (h) `useradd`
   and `gpasswd` are present in the NixOS system profile — `D4/c2/raw/doc-nixos-local.out` lines 170–172.

2. **Outcomes follow Appendix A.4.5 and A.4.1; no rule invented.** Both assessments decide "does not have" in all six
   cases; each rests on a source or record for the fact A.4.5 names (P1: an unrecorded account setting in force;
   P2: a recorded membership out of force after application; P4: a built-in account tool changing a setting past the
   declaration). Same decision with sufficient information yields 1; six 1s give CHECK 4 outcome 1. The supporting
   sentences are cited with correct IDs (S8.1-7, S8.1-15, S8.2-13, S8.3-1, S8.3-5); (not published: orchestration or scratch) reports
   5 quotes, 0 not found. The P2 reading ("any moment after a completed application", S8.3-1) is literal, and the
   account-as-setting mapping follows the first affirmative answer of S8.2-6 (question 3, S8.2-11–13).

3. **Numbers match.** (not published: orchestration or scratch), `D4/c1/cases.tsv`, (not published: orchestration or scratch), `D4/c2/cases.tsv` each hold six rows, all
   "does not have"; the RESULT table repeats them; no `undecidable` or `insufficient` decision and no unmappable notion
   is recorded in either `ASSESS.md`, as RESULT states.

4. **Independence and scope kept.** No reference from `D4/c1` to `D4/c2` or back; both cite only `check-inputs-v4` inputs, their
   own records and official documentation. No forbidden folder is cited. No host names, home paths or mentions of any
   automated system were found in the six files reviewed. Both clean installations of c2 and both of c1 were
   destroyed (`D4/c2/raw/destroy-*.txt`; `D4/c1/raw/nixos-destroy.txt`, `guix-destroy-2.txt`, `cleanup.txt`).

5. **Minor — c2 ran probes whose answer was already documented.** Where: `D4/c2/EXPERIMENTS.md` E-N2, E-G2. Evidence:
   (not published: orchestration) says "if the answer is there, do not run the probe"; c2 itself cites G-D3 (changes persist until
   reconfiguration or reboot) and S-D1 (`gpasswd -d` removes membership), and c1 settled the same facts from
   documentation. E-N2 also observes a second fact (what the next application does) in the same run. Outcome
   unaffected. Minimal fix: add one line to `D4/c2/EXPERIMENTS.md` stating what exactly the documentation left open, or
   mark the records as corroboration only.

6. **Minor — pre-registration time of E-N2 compares two clocks.** Where: `D4/c2/EXPERIMENTS.md` E-N2 heading. Evidence:
   "written 11:14:48Z by file time, before the run at 11:14:53Z guest clock" — a 5-second margin between the host file
   time and the guest clock. Minimal fix: state that the two clocks were not compared, or cite the runner's host-side
   start time.

7. **Minor — the Guix P2 record has no observed application report.** Where: `D4/RESULT.md` row Guix/P2; `D4/c2/ASSESS.md`
   guix × P2. Evidence: `D4/c2/raw/e-g2.out` contains no `guix system reconfigure`; the completed application is the
   installation's `guix system init` (`check-inputs-v4/install/recipes/guix/original-install.sh.in`), whose status is not recorded.
   RESULT notes this but says "the documentary counterexample independently establishes" without naming whose; for c2
   that is G-D3 with S-D1, for c1 the `usermod -G` source. Both are general (any completed application), so the outcome
   stands. Minimal fix: name the documentary basis of each assessment in that row.

8. **Minor — c1 had no clean Guix installation; RESULT does not say so.** Where: `D4/RESULT.md` Guix rows. Evidence:
   `D4/c1/raw/guix-new.txt` (launch timed out); `D4/c1/EVIDENCE.md` states c1's Guix decisions are documentation-only.
   A.4.5 accepts "a source or an experimental record", so information remains sufficient. Minimal fix: one sentence in
   RESULT recording that c1's Guix assessment rests on documentation alone.

9. **Minor — gpasswd source version differs from the shipped versions.** Where: `D4/c2/ASSESS.md` S-D1. Evidence: the
   cited page is shadow-utils 4.19.0 (man7.org), while the systems ship 4.19.4 (NixOS) and 4.13 (Guix). The cited
   behaviour is confirmed on both systems by `e-n2.out` and `e-g2.out`. Minimal fix: note the version difference.

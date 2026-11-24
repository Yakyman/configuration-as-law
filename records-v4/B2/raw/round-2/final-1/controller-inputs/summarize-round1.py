#!/usr/bin/env python3
"""Validate complete saved Round 1 evidence before summarizing; never runs guests.

Contracts: reviewed fixed new-suite phase/ID inventories, tied to frozen source
hashes; unchanged carried contracts from SHA-pinned complete Round 0 baseline.
Target evidence is never used to infer its own expected result inventory.
"""
import argparse, collections, hashlib, json, pathlib, re, shlex
ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT / 'raw/round-1'
FINAL = RAW / 'final-2'
BASE = ROOT / 'raw/round-0/round-4/baseline'
NEW = {'shell.jsonl': {'source': 'build/v4-shell-selftest.py', 'source_sha256': 'b3a8601384c69a824406a4b32abd59727d3fd51d8d33bee9e3f7c444f509be52', 'reviewed_result_count': 28, 'record_contract': [['expected', None, 'SHELL-PROFILE', None, None, None, ['command', 'expected', 'id', 'phase', 'utc', 'variants'], None, None], ['result', None, 'SHELL-PROFILE', None, None, None, ['exit', 'id', 'output', 'passed', 'phase', 'requirement', 'stderr', 'utc', 'variants'], 'bool', None], ['expected', None, 'FREE-COMMANDS', None, None, None, ['command', 'expected', 'id', 'phase', 'utc', 'variants'], None, None], ['result', None, 'FREE-COMMANDS', None, None, None, ['exit', 'id', 'output', 'passed', 'phase', 'requirement', 'stderr', 'utc', 'variants'], 'bool', None], ['expected', None, 'DOCUMENT-EDIT', None, None, None, ['command', 'expected', 'id', 'phase', 'utc', 'variants'], None, None], ['result', None, 'DOCUMENT-EDIT', None, None, None, ['exit', 'id', 'output', 'passed', 'phase', 'requirement', 'stderr', 'utc', 'variants'], 'bool', None], ['expected', None, 'BROWSER', None, None, None, ['command', 'expected', 'id', 'phase', 'utc', 'variants'], None, None], ['result', None, 'BROWSER', None, None, None, ['exit', 'id', 'output', 'passed', 'phase', 'requirement', 'stderr', 'utc', 'variants'], 'bool', None], ['result', None, 'MATERIAL-NO-LINE', None, None, None, ['id', 'passed', 'phase', 'report_unchanged', 'utc', 'variants'], 'bool', None], ['expected', None, 'PERSONAL-INSTALL', None, None, None, ['command', 'expected', 'id', 'phase', 'utc', 'variants'], None, None], ['result', None, 'PERSONAL-INSTALL', None, None, None, ['exit', 'id', 'output', 'passed', 'phase', 'requirement', 'stderr', 'utc', 'variants'], 'bool', None], ['expected', None, 'PERSONAL-RUN', None, None, None, ['command', 'expected', 'id', 'phase', 'utc', 'variants'], None, None], ['result', None, 'PERSONAL-RUN', None, None, None, ['exit', 'id', 'output', 'passed', 'phase', 'requirement', 'stderr', 'utc', 'variants'], 'bool', None], ['result', None, 'PERSONAL-COVERAGE', None, None, None, ['id', 'last_success', 'line', 'passed', 'phase', 'utc', 'variants'], 'bool', None], ['expected', None, 'NATIVE-COPY', None, None, None, ['command', 'expected', 'id', 'phase', 'utc', 'variants'], None, None], ['result', None, 'NATIVE-COPY', None, None, None, ['exit', 'id', 'output', 'passed', 'phase', 'requirement', 'stderr', 'utc', 'variants'], 'bool', None], ['expected', None, 'NATIVE-LOADER', None, None, None, ['command', 'expected', 'id', 'phase', 'utc', 'variants'], None, None], ['result', None, 'NATIVE-LOADER', None, None, None, ['exit', 'id', 'output', 'passed', 'phase', 'requirement', 'stderr', 'utc', 'variants'], 'bool', None], ['expected', None, 'NATIVE-HELPER', None, None, None, ['command', 'expected', 'id', 'phase', 'utc', 'variants'], None, None], ['result', None, 'NATIVE-HELPER', None, None, None, ['exit', 'id', 'output', 'passed', 'phase', 'requirement', 'stderr', 'utc', 'variants'], 'bool', None], ['expected', None, 'RECORDED-REPLACE', None, None, None, ['command', 'expected', 'id', 'phase', 'utc', 'variants'], None, None], ['result', None, 'RECORDED-REPLACE', None, None, None, ['exit', 'id', 'output', 'passed', 'phase', 'requirement', 'stderr', 'utc', 'variants'], 'bool', None], ['expected', None, 'SAVED-SCRIPT', None, None, None, ['command', 'expected', 'id', 'phase', 'utc', 'variants'], None, None], ['result', None, 'SAVED-SCRIPT', None, None, None, ['exit', 'id', 'output', 'passed', 'phase', 'requirement', 'stderr', 'utc', 'variants'], 'bool', None], ['expected', None, 'SAVED-PIPE', None, None, None, ['command', 'expected', 'id', 'phase', 'utc', 'variants'], None, None], ['result', None, 'SAVED-PIPE', None, None, None, ['exit', 'id', 'output', 'passed', 'phase', 'requirement', 'stderr', 'utc', 'variants'], 'bool', None], ['expected', None, 'SAVED-SOURCE', None, None, None, ['command', 'expected', 'id', 'phase', 'utc', 'variants'], None, None], ['result', None, 'SAVED-SOURCE', None, None, None, ['exit', 'id', 'output', 'passed', 'phase', 'requirement', 'stderr', 'utc', 'variants'], 'bool', None], ['expected', None, 'STARTUP-ENV', None, None, None, ['command', 'expected', 'id', 'phase', 'utc', 'variants'], None, None], ['result', None, 'STARTUP-ENV', None, None, None, ['exit', 'id', 'output', 'passed', 'phase', 'requirement', 'stderr', 'utc', 'variants'], 'bool', None], ['expected', None, 'PYTHON-IMPORT', None, None, None, ['command', 'expected', 'id', 'phase', 'utc', 'variants'], None, None], ['result', None, 'PYTHON-IMPORT', None, None, None, ['exit', 'id', 'output', 'passed', 'phase', 'requirement', 'stderr', 'utc', 'variants'], 'bool', None], ['expected', None, 'PICKLE-CODE', None, None, None, ['command', 'expected', 'id', 'phase', 'utc', 'variants'], None, None], ['result', None, 'PICKLE-CODE', None, None, None, ['exit', 'id', 'output', 'passed', 'phase', 'requirement', 'stderr', 'utc', 'variants'], 'bool', None], ['expected', None, 'USER-SERVICE', None, None, None, ['command', 'expected', 'id', 'phase', 'utc', 'variants'], None, None], ['result', None, 'USER-SERVICE', None, None, None, ['exit', 'id', 'output', 'passed', 'phase', 'requirement', 'stderr', 'utc', 'variants'], 'bool', None], ['result', None, 'USER-SERVICE-STATE', None, None, None, ['enabled', 'id', 'passed', 'phase', 'utc', 'variants'], 'bool', None], ['expected', None, 'TRANSIENT-JOB', None, None, None, ['command', 'expected', 'id', 'phase', 'utc', 'variants'], None, None], ['result', None, 'TRANSIENT-JOB', None, None, None, ['exit', 'id', 'output', 'passed', 'phase', 'requirement', 'stderr', 'utc', 'variants'], 'bool', None], ['expected', None, 'CRON-JOB', None, None, None, ['command', 'expected', 'id', 'phase', 'utc', 'variants'], None, None], ['result', None, 'CRON-JOB', None, None, None, ['exit', 'id', 'output', 'passed', 'phase', 'requirement', 'stderr', 'utc', 'variants'], 'bool', None], ['expected', None, 'RAW-SETTINGS', None, None, None, ['command', 'expected', 'id', 'phase', 'utc', 'variants'], None, None], ['result', None, 'RAW-SETTINGS', None, None, None, ['exit', 'id', 'output', 'passed', 'phase', 'requirement', 'stderr', 'utc', 'variants'], 'bool', None], ['expected', None, 'USER-NAMESPACE', None, None, None, ['command', 'expected', 'id', 'phase', 'utc', 'variants'], None, None], ['result', None, 'USER-NAMESPACE', None, None, None, ['exit', 'id', 'output', 'passed', 'phase', 'requirement', 'stderr', 'utc', 'variants'], 'bool', None], ['expected', None, 'OCI-ALTERNATE', None, None, None, ['command', 'expected', 'id', 'phase', 'utc', 'variants'], None, None], ['result', None, 'OCI-ALTERNATE', None, None, None, ['exit', 'id', 'output', 'passed', 'phase', 'requirement', 'stderr', 'utc', 'variants'], 'bool', None], ['expected', None, 'OCI-WRITABLE-OVERLAY', None, None, None, ['command', 'expected', 'id', 'phase', 'utc', 'variants'], None, None], ['result', None, 'OCI-WRITABLE-OVERLAY', None, None, None, ['exit', 'id', 'output', 'passed', 'phase', 'requirement', 'stderr', 'utc', 'variants'], 'bool', None], ['expected', None, 'PERSONAL-REMOVE', None, None, None, ['command', 'expected', 'id', 'phase', 'utc', 'variants'], None, None], ['result', None, 'PERSONAL-REMOVE', None, None, None, ['exit', 'id', 'output', 'passed', 'phase', 'requirement', 'stderr', 'utc', 'variants'], 'bool', None], ['expected', None, 'UNSAVED-EXECUTE', None, None, None, ['command', 'expected', 'id', 'phase', 'utc', 'variants'], None, None], ['result', None, 'UNSAVED-EXECUTE', None, None, None, ['id', 'output', 'passed', 'payload_bytes', 'payload_files', 'payload_sha256', 'phase', 'processes', 'utc', 'variants'], 'bool', None], ['summary', None, None, None, None, None, ['boundary_failures', 'hypothesis_outcome', 'implemented_checks_passed', 'phase', 'utc'], None, None]]}, 'shell-reboot.jsonl': {'source': 'build/v4-shell-selftest.py', 'source_sha256': 'b3a8601384c69a824406a4b32abd59727d3fd51d8d33bee9e3f7c444f509be52', 'reviewed_result_count': 1, 'record_contract': [['result', None, 'UNSAVED-AFTER-REBOOT', None, None, None, ['id', 'matching_processes', 'passed', 'payload_sha256', 'phase', 'report_unchanged', 'utc', 'variants'], 'bool', None]]}, 'gate.jsonl': {'source': 'build/v4-gate-selftest.py', 'source_sha256': 'c3d05c40e71652c84ff349792bad1ec2f28c4dc07400829419434462e1f047dc', 'reviewed_result_count': 9, 'record_contract': [['expected', None, 'APPLY-SHELL-GATE', None, None, None, ['command', 'expected', 'id', 'phase', 'utc'], None, None], ['result', None, 'APPLY-SHELL-GATE', None, None, None, ['apply_exit', 'apply_stderr', 'apply_stdout', 'entry_exit', 'entry_stderr', 'entry_stdout', 'freezer_children_removed', 'frozen_cgroup', 'generation', 'heartbeat_size_at_pause', 'id', 'journal', 'journal_removed', 'kernel_at_pause', 'observer_original_cgroup', 'observer_pid', 'observer_restored_cgroup', 'original_cgroup', 'passed', 'phase', 'readback_count', 'readback_failures', 'removed_id', 'report', 'required_observation', 'required_row', 'restored_cgroup', 'resumed', 'sample_count', 'sample_values', 'shell_pid', 'utc'], 'bool', None], ['expected', None, 'GATE-FIXTURE-REMOVAL', None, None, None, ['expected', 'id', 'phase', 'utc'], None, None], ['result', None, 'GATE-FIXTURE-REMOVAL', None, None, None, ['generation', 'id', 'journal_removed', 'output', 'passed', 'phase', 'readback_count', 'readback_failures', 'removed_id', 'report', 'required_observation', 'required_row', 'stderr', 'utc'], 'bool', None], ['expected', None, 'NESTED-BROKER-CALLER', None, None, None, ['command', 'expected', 'id', 'package_commands', 'phase', 'utc'], None, None], ['result', None, 'NESTED-BROKER-CALLER-INSTALL', None, None, None, ['caller_return', 'cgroup_restored', 'freezer_children_removed', 'generation', 'id', 'journal_removed', 'passed', 'phase', 'readback_count', 'readback_failures', 'removed_id', 'report', 'required_observation', 'required_row', 'utc'], 'bool', None], ['result', None, 'NESTED-BROKER-CALLER-REMOVE', None, None, None, ['caller_return', 'cgroup_restored', 'freezer_children_removed', 'generation', 'id', 'journal_removed', 'passed', 'phase', 'readback_count', 'readback_failures', 'removed_id', 'report', 'required_observation', 'required_row', 'utc'], 'bool', None], ['result', None, 'NESTED-BROKER-CALLER', None, None, None, ['caller_complete', 'caller_exit', 'caller_start', 'freezer_children_removed', 'id', 'journal_removed', 'observed_freezer_groups', 'output', 'passed', 'phase', 'return_count', 'utc'], 'bool', None], ['expected', None, 'NESTED-EDITOR-CALLER', None, None, None, ['command', 'expected', 'id', 'package_commands', 'phase', 'utc'], None, None], ['result', None, 'NESTED-EDITOR-CALLER-INSTALL', None, None, None, ['caller_return', 'cgroup_restored', 'freezer_children_removed', 'generation', 'id', 'journal_removed', 'passed', 'phase', 'readback_count', 'readback_failures', 'removed_id', 'report', 'required_observation', 'required_row', 'utc'], 'bool', None], ['result', None, 'NESTED-EDITOR-CALLER-REMOVE', None, None, None, ['caller_return', 'cgroup_restored', 'freezer_children_removed', 'generation', 'id', 'journal_removed', 'passed', 'phase', 'readback_count', 'readback_failures', 'removed_id', 'report', 'required_observation', 'required_row', 'utc'], 'bool', None], ['result', None, 'NESTED-EDITOR-CALLER', None, None, None, ['caller_complete', 'caller_exit', 'caller_start', 'freezer_children_removed', 'id', 'journal_removed', 'observed_freezer_groups', 'output', 'passed', 'phase', 'return_count', 'utc'], 'bool', None], ['result', None, 'GATE-FINAL-RESTORATION', None, None, None, ['declaration_restored', 'generation', 'id', 'journal_removed', 'passed', 'phase', 'readback_count', 'readback_failures', 'removed_id', 'report', 'required_observation', 'required_row', 'utc'], 'bool', None], ['summary', None, None, None, None, None, ['failures', 'passed', 'phase', 'utc'], 'bool', None]]}, 'tools.jsonl': {'source': 'build/v4-tools-selftest.py', 'source_sha256': 'a5bdeef26adb7f0cfa05ad43968ed50541ba4009bed7b266fb713f0ac25a5249', 'reviewed_result_count': 86, 'record_contract': [['fixture', None, None, None, None, None, ['exact_input', 'name', 'path', 'phase', 'sha256', 'utc'], None, None], ['fixture', None, None, None, None, None, ['exact_input', 'name', 'path', 'phase', 'sha256', 'utc'], None, None], ['fixture', None, None, None, None, None, ['exact_input', 'name', 'path', 'phase', 'sha256', 'utc'], None, None], ['fixture', None, None, None, None, None, ['exact_input', 'name', 'path', 'phase', 'sha256', 'utc'], None, None], ['fixture', None, None, None, None, None, ['exact_input', 'name', 'path', 'phase', 'sha256', 'utc'], None, None], ['fixture', None, None, None, None, None, ['exact_input', 'name', 'path', 'phase', 'sha256', 'utc'], None, None], ['fixture', None, None, None, None, None, ['exact_input', 'name', 'path', 'phase', 'sha256', 'utc'], None, None], ['fixture', None, None, None, None, None, ['exact_input', 'name', 'path', 'phase', 'sha256', 'utc'], None, None], ['fixture', None, None, None, None, None, ['exact_input', 'name', 'path', 'phase', 'sha256', 'utc'], None, None], ['fixture', None, None, None, None, None, ['exact_input', 'name', 'path', 'phase', 'sha256', 'utc'], None, None], ['fixture', None, None, None, None, None, ['exact_input', 'name', 'path', 'phase', 'sha256', 'utc'], None, None], ['fixture', None, None, None, None, None, ['exact_input', 'name', 'path', 'phase', 'sha256', 'utc'], None, None], ['fixture', None, None, None, None, None, ['exact_input', 'name', 'path', 'phase', 'sha256', 'utc'], None, None], ['expected', None, 'ordinary-worker', 'ordinary', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'ordinary-worker', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'recorded-native-overwrite', None, None, None, ['command', 'expected', 'id', 'phase', 'utc', 'variants'], None, None], ['result', None, 'recorded-native-overwrite', None, None, None, ['actual_file', 'actual_sha256', 'coverage_unchanged', 'covering_line', 'id', 'passed', 'phase', 'rc', 'report_unchanged', 'required_file', 'required_sha256', 'stderr', 'utc', 'variants'], 'bool', None], ['expected', None, 'ordinary-service', 'ordinary', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'ordinary-service', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'ordinary-systemd-run-add', 'ordinary', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'ordinary-systemd-run-add', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'ordinary-systemd-run-remove', 'ordinary', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'ordinary-systemd-run-remove', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'ordinary-crontab-add', 'ordinary', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'ordinary-crontab-add', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'ordinary-crontab-remove', 'ordinary', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'ordinary-crontab-remove', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'ordinary-at-add', 'ordinary', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'ordinary-at-add', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'ordinary-at-remove', 'ordinary', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'ordinary-at-remove', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'ordinary-socket-add', 'ordinary', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'ordinary-socket-add', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'ordinary-socket-remove', 'ordinary', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'ordinary-socket-remove', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'ordinary-useradd', 'ordinary', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'ordinary-useradd', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'ordinary-usermod', 'ordinary', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'ordinary-usermod', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'ordinary-userdel', 'ordinary', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'ordinary-userdel', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'ordinary-groupadd', 'ordinary', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'ordinary-groupadd', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'ordinary-groupdel', 'ordinary', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'ordinary-groupdel', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'ordinary-nft-add', 'ordinary', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'ordinary-nft-add', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'ordinary-nft-remove', 'ordinary', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'ordinary-nft-remove', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'ordinary-nmcli-add', 'ordinary', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'ordinary-nmcli-add', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'ordinary-nmcli-remove', 'ordinary', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'ordinary-nmcli-remove', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'ordinary-bluetoothctl-add', 'ordinary', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'ordinary-bluetoothctl-add', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'ordinary-bluetoothctl-remove', 'ordinary', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'ordinary-bluetoothctl-remove', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'ordinary-wrong-kind', 'ordinary', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'ordinary-wrong-kind', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'ordinary-group-members', 'ordinary', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'ordinary-group-members', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'ordinary-service-remove', 'ordinary', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'ordinary-service-remove', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'ordinary-worker-remove', 'ordinary', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'ordinary-worker-remove', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'ordinary-apt-install', 'ordinary', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'ordinary-apt-install', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'ordinary-apt-reinstall', 'ordinary', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'ordinary-apt-reinstall', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'ordinary-apt-downgrade', 'ordinary', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'ordinary-apt-downgrade', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'ordinary-apt-remove', 'ordinary', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'ordinary-apt-remove', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'ordinary-apt-get-install', 'ordinary', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'ordinary-apt-get-install', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'ordinary-apt-get-reinstall', 'ordinary', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'ordinary-apt-get-reinstall', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'ordinary-apt-get-downgrade', 'ordinary', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'ordinary-apt-get-downgrade', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'ordinary-apt-get-remove', 'ordinary', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'ordinary-apt-get-remove', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'ordinary-editor-write', 'ordinary', None, None, ['command', 'expected', 'id', 'mode', 'phase', 'stdin_sha256', 'utc'], None, None], ['result', None, 'ordinary-editor-write', None, None, None, ['id', 'passed', 'phase', 'rc', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'ordinary-editor-append', 'ordinary', None, None, ['command', 'expected', 'id', 'mode', 'phase', 'stdin_sha256', 'utc'], None, None], ['result', None, 'ordinary-editor-append', None, None, None, ['id', 'passed', 'phase', 'rc', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'ordinary-editor-read', 'ordinary', None, None, ['command', 'expected', 'id', 'mode', 'phase', 'stdin_sha256', 'utc'], None, None], ['result', None, 'ordinary-editor-read', None, None, None, ['id', 'passed', 'phase', 'rc', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'ordinary-editor-install', 'ordinary', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'ordinary-editor-install', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'ordinary-editor-installed-run', 'ordinary', None, None, ['command', 'expected', 'id', 'mode', 'phase', 'stdin_sha256', 'utc'], None, None], ['result', None, 'ordinary-editor-installed-run', None, None, None, ['id', 'passed', 'phase', 'rc', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'ordinary-editor-remove', 'ordinary', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'ordinary-editor-remove', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'ordinary-editor-hash-refusal', 'ordinary', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'ordinary-editor-hash-refusal', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'root-worker', 'root', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'root-worker', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'root-service', 'root', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'root-service', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'root-systemd-run-add', 'root', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'root-systemd-run-add', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'root-systemd-run-remove', 'root', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'root-systemd-run-remove', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'root-crontab-add', 'root', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'root-crontab-add', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'root-crontab-remove', 'root', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'root-crontab-remove', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'root-at-add', 'root', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'root-at-add', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'root-at-remove', 'root', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'root-at-remove', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'root-socket-add', 'root', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'root-socket-add', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'root-socket-remove', 'root', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'root-socket-remove', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'root-useradd', 'root', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'root-useradd', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'root-usermod', 'root', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'root-usermod', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'root-userdel', 'root', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'root-userdel', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'root-groupadd', 'root', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'root-groupadd', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'root-groupdel', 'root', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'root-groupdel', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'root-nft-add', 'root', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'root-nft-add', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'root-nft-remove', 'root', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'root-nft-remove', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'root-nmcli-add', 'root', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'root-nmcli-add', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'root-nmcli-remove', 'root', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'root-nmcli-remove', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'root-bluetoothctl-add', 'root', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'root-bluetoothctl-add', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'root-bluetoothctl-remove', 'root', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'root-bluetoothctl-remove', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'root-wrong-kind', 'root', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'root-wrong-kind', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'root-group-members', 'root', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'root-group-members', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'root-service-remove', 'root', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'root-service-remove', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'root-worker-remove', 'root', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'root-worker-remove', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'root-apt-install', 'root', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'root-apt-install', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'root-apt-reinstall', 'root', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'root-apt-reinstall', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'root-apt-downgrade', 'root', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'root-apt-downgrade', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'root-apt-remove', 'root', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'root-apt-remove', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'root-apt-get-install', 'root', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'root-apt-get-install', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'root-apt-get-reinstall', 'root', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'root-apt-get-reinstall', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'root-apt-get-downgrade', 'root', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'root-apt-get-downgrade', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'root-apt-get-remove', 'root', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'root-apt-get-remove', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'root-editor-write', 'root', None, None, ['command', 'expected', 'id', 'mode', 'phase', 'stdin_sha256', 'utc'], None, None], ['result', None, 'root-editor-write', None, None, None, ['id', 'passed', 'phase', 'rc', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'root-editor-append', 'root', None, None, ['command', 'expected', 'id', 'mode', 'phase', 'stdin_sha256', 'utc'], None, None], ['result', None, 'root-editor-append', None, None, None, ['id', 'passed', 'phase', 'rc', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'root-editor-read', 'root', None, None, ['command', 'expected', 'id', 'mode', 'phase', 'stdin_sha256', 'utc'], None, None], ['result', None, 'root-editor-read', None, None, None, ['id', 'passed', 'phase', 'rc', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'root-editor-install', 'root', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'root-editor-install', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'root-editor-installed-run', 'root', None, None, ['command', 'expected', 'id', 'mode', 'phase', 'stdin_sha256', 'utc'], None, None], ['result', None, 'root-editor-installed-run', None, None, None, ['id', 'passed', 'phase', 'rc', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'root-editor-remove', 'root', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'root-editor-remove', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'root-editor-hash-refusal', 'root', None, None, ['before_identity', 'command', 'exact_required_row', 'expected', 'id', 'mode', 'phase', 'removed_id', 'utc'], None, None], ['result', None, 'root-editor-hash-refusal', None, None, None, ['after_identity', 'declaration_added_or_changed', 'declaration_removed', 'id', 'passed', 'phase', 'rc', 'readback', 'readback_count', 'readback_failures', 'required_observation', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'root-editor-breaking', None, None, None, ['expected', 'id', 'phase', 'utc'], None, None], ['result', None, 'root-editor-breaking', None, None, None, ['classification', 'id', 'passed', 'phase', 'rc', 'utc'], 'bool', None], ['expected', None, 'root-native-account-bypass', None, None, None, ['before_identity', 'classification', 'command', 'expected_property', 'id', 'implementation_prediction', 'phase', 'utc', 'variants'], None, None], ['boundary_result', None, 'root-native-account-bypass', None, None, None, ['account', 'classification', 'covered_by_declaration', 'declaration_unchanged', 'id', 'included_in_implemented_check_exit', 'last_success_unchanged', 'passed', 'phase', 'rc', 'stderr', 'stdout', 'utc', 'variants'], 'bool', None], ['result', None, 'root-native-account-cleanup', None, None, None, ['account_absent', 'group_cleanup_rc', 'id', 'passed', 'phase', 'rc', 'utc'], 'bool', None], ['result', None, 'final-declaration-restored', None, None, None, ['extra_ids', 'id', 'missing_ids', 'passed', 'phase', 'utc'], 'bool', None], ['result', None, 'final-readback', None, None, None, ['count', 'failures', 'id', 'passed', 'phase', 'utc'], 'bool', None], ['summary', None, None, None, None, None, ['failures', 'passed', 'phase', 'radio_hardware_tested', 'utc'], 'bool', None]]}, 'supplement/direct.jsonl': {'source': 'raw/round-1/final-2-supplement-inputs/v4-direct-selftest.py', 'source_sha256': '82bd871f23561397ff510a3c28b81294a045dfd97d6f120ccc3fb5380c5f0399', 'reviewed_result_count': 17, 'record_contract': [['sources', None, None, None, None, None, ['phase', 'references', 'unknown', 'utc'], None, None], ['expected', None, 'DIRECT-HTTP-SAVE', None, None, None, ['before', 'command', 'expected', 'id', 'marker', 'phase', 'utc', 'variants'], None, None], ['result', None, 'DIRECT-HTTP-SAVE', None, None, None, ['assertion_kind', 'declaration_and_report_unchanged', 'exit', 'files', 'fixture_exact', 'id', 'marker_observed', 'passed', 'phase', 'policy_diagnostic', 'required_hashes', 'required_links', 'stderr', 'stdout', 'utc', 'variants'], 'bool', None], ['expected', None, 'DIRECT-HTTP-NATIVE', None, None, None, ['before', 'command', 'expected', 'id', 'marker', 'phase', 'utc', 'variants'], None, None], ['result', None, 'DIRECT-HTTP-NATIVE', None, None, None, ['assertion_kind', 'declaration_and_report_unchanged', 'exit', 'files', 'fixture_exact', 'id', 'marker_observed', 'passed', 'phase', 'policy_diagnostic', 'required_hashes', 'required_links', 'stderr', 'stdout', 'utc', 'variants'], 'bool', None], ['expected', None, 'DIRECT-NESTED-EXTRACT', None, None, None, ['before', 'command', 'expected', 'id', 'marker', 'phase', 'utc', 'variants'], None, None], ['result', None, 'DIRECT-NESTED-EXTRACT', None, None, None, ['assertion_kind', 'declaration_and_report_unchanged', 'exit', 'files', 'fixture_exact', 'id', 'marker_observed', 'passed', 'phase', 'policy_diagnostic', 'required_hashes', 'required_links', 'stderr', 'stdout', 'utc', 'variants'], 'bool', None], ['expected', None, 'DIRECT-NESTED-ARCHIVE', None, None, None, ['before', 'command', 'expected', 'id', 'marker', 'phase', 'utc', 'variants'], None, None], ['result', None, 'DIRECT-NESTED-ARCHIVE', None, None, None, ['assertion_kind', 'declaration_and_report_unchanged', 'exit', 'files', 'fixture_exact', 'id', 'marker_observed', 'passed', 'phase', 'policy_diagnostic', 'required_hashes', 'required_links', 'stderr', 'stdout', 'utc', 'variants'], 'bool', None], ['fixture', None, None, None, None, None, ['bytes', 'path', 'phase', 'sha256', 'utc'], None, None], ['expected', None, 'DIRECT-COMPILE', None, None, None, ['before', 'command', 'expected', 'id', 'marker', 'phase', 'utc', 'variants'], None, None], ['result', None, 'DIRECT-COMPILE', None, None, None, ['assertion_kind', 'declaration_and_report_unchanged', 'exit', 'files', 'fixture_exact', 'id', 'marker_observed', 'passed', 'phase', 'policy_diagnostic', 'required_hashes', 'required_links', 'stderr', 'stdout', 'utc', 'variants'], 'bool', None], ['expected', None, 'DIRECT-COMPILED-RUN', None, None, None, ['before', 'command', 'expected', 'id', 'marker', 'phase', 'utc', 'variants'], None, None], ['result', None, 'DIRECT-COMPILED-RUN', None, None, None, ['assertion_kind', 'declaration_and_report_unchanged', 'exit', 'files', 'fixture_exact', 'id', 'marker_observed', 'passed', 'phase', 'policy_diagnostic', 'required_hashes', 'required_links', 'stderr', 'stdout', 'utc', 'variants'], 'bool', None], ['expected', None, 'DIRECT-PREFIX-SETUP', None, None, None, ['before', 'command', 'expected', 'id', 'marker', 'phase', 'utc', 'variants'], None, None], ['result', None, 'DIRECT-PREFIX-SETUP', None, None, None, ['assertion_kind', 'declaration_and_report_unchanged', 'exit', 'files', 'fixture_exact', 'id', 'marker_observed', 'passed', 'phase', 'policy_diagnostic', 'required_hashes', 'required_links', 'stderr', 'stdout', 'utc', 'variants'], 'bool', None], ['expected', None, 'DIRECT-PREFIX-PATH', None, None, None, ['before', 'command', 'expected', 'id', 'marker', 'phase', 'utc', 'variants'], None, None], ['result', None, 'DIRECT-PREFIX-PATH', None, None, None, ['assertion_kind', 'declaration_and_report_unchanged', 'exit', 'files', 'fixture_exact', 'id', 'marker_observed', 'passed', 'phase', 'policy_diagnostic', 'required_hashes', 'required_links', 'stderr', 'stdout', 'utc', 'variants'], 'bool', None], ['fixture', None, None, None, None, None, ['bytes', 'path', 'phase', 'sha256', 'utc'], None, None], ['expected', None, 'DIRECT-PLUGIN-BUILD', None, None, None, ['before', 'command', 'expected', 'id', 'marker', 'phase', 'utc', 'variants'], None, None], ['result', None, 'DIRECT-PLUGIN-BUILD', None, None, None, ['assertion_kind', 'declaration_and_report_unchanged', 'exit', 'files', 'fixture_exact', 'id', 'marker_observed', 'passed', 'phase', 'policy_diagnostic', 'required_hashes', 'required_links', 'stderr', 'stdout', 'utc', 'variants'], 'bool', None], ['expected', None, 'DIRECT-COMPILER-PLUGIN', None, None, None, ['before', 'command', 'expected', 'id', 'marker', 'phase', 'utc', 'variants'], None, None], ['result', None, 'DIRECT-COMPILER-PLUGIN', None, None, None, ['assertion_kind', 'declaration_and_report_unchanged', 'exit', 'files', 'fixture_exact', 'id', 'marker_observed', 'passed', 'phase', 'policy_diagnostic', 'required_hashes', 'required_links', 'stderr', 'stdout', 'utc', 'variants'], 'bool', None], ['fixture', None, None, None, None, None, ['bytes', 'path', 'phase', 'sha256', 'utc'], None, None], ['expected', None, 'DIRECT-SHEBANG', None, None, None, ['before', 'command', 'expected', 'id', 'marker', 'phase', 'utc', 'variants'], None, None], ['result', None, 'DIRECT-SHEBANG', None, None, None, ['assertion_kind', 'declaration_and_report_unchanged', 'exit', 'files', 'fixture_exact', 'id', 'marker_observed', 'passed', 'phase', 'policy_diagnostic', 'required_hashes', 'required_links', 'stderr', 'stdout', 'utc', 'variants'], 'bool', None], ['expected', None, 'DIRECT-REDIRECT-STDIN', None, None, None, ['before', 'command', 'expected', 'id', 'marker', 'phase', 'utc', 'variants'], None, None], ['result', None, 'DIRECT-REDIRECT-STDIN', None, None, None, ['assertion_kind', 'declaration_and_report_unchanged', 'exit', 'files', 'fixture_exact', 'id', 'marker_observed', 'passed', 'phase', 'policy_diagnostic', 'required_hashes', 'required_links', 'stderr', 'stdout', 'utc', 'variants'], 'bool', None], ['expected', None, 'DIRECT-PROC-FD', None, None, None, ['before', 'command', 'expected', 'id', 'marker', 'phase', 'utc', 'variants'], None, None], ['result', None, 'DIRECT-PROC-FD', None, None, None, ['assertion_kind', 'declaration_and_report_unchanged', 'exit', 'files', 'fixture_exact', 'id', 'marker_observed', 'passed', 'phase', 'policy_diagnostic', 'required_hashes', 'required_links', 'stderr', 'stdout', 'utc', 'variants'], 'bool', None], ['fixture', None, None, None, None, None, ['bytes', 'path', 'phase', 'sha256', 'utc'], None, None], ['expected', None, 'DIRECT-READ-EXEC', None, None, None, ['before', 'command', 'expected', 'id', 'marker', 'phase', 'utc', 'variants'], None, None], ['result', None, 'DIRECT-READ-EXEC', None, None, None, ['assertion_kind', 'declaration_and_report_unchanged', 'exit', 'files', 'fixture_exact', 'id', 'marker_observed', 'passed', 'phase', 'policy_diagnostic', 'required_hashes', 'required_links', 'stderr', 'stdout', 'utc', 'variants'], 'bool', None], ['fixture', None, None, None, None, None, ['bytes', 'path', 'phase', 'sha256', 'utc'], None, None], ['expected', None, 'DIRECT-AWK-FILE', None, None, None, ['before', 'command', 'expected', 'id', 'marker', 'phase', 'utc', 'variants'], None, None], ['result', None, 'DIRECT-AWK-FILE', None, None, None, ['assertion_kind', 'declaration_and_report_unchanged', 'exit', 'files', 'fixture_exact', 'id', 'marker_observed', 'passed', 'phase', 'policy_diagnostic', 'required_hashes', 'required_links', 'stderr', 'stdout', 'utc', 'variants'], 'bool', None], ['expected', None, 'DIRECT-SCRIPT-HELPER', None, None, None, ['before', 'command', 'expected', 'id', 'marker', 'phase', 'utc', 'variants'], None, None], ['result', None, 'DIRECT-SCRIPT-HELPER', None, None, None, ['assertion_kind', 'declaration_and_report_unchanged', 'exit', 'files', 'fixture_exact', 'id', 'marker_observed', 'passed', 'phase', 'policy_diagnostic', 'required_hashes', 'required_links', 'stderr', 'stdout', 'utc', 'variants'], 'bool', None], ['expected', None, 'DIRECT-RUNTIME-ALIAS', None, None, None, ['before', 'command', 'expected', 'id', 'marker', 'phase', 'utc', 'variants'], None, None], ['result', None, 'DIRECT-RUNTIME-ALIAS', None, None, None, ['assertion_kind', 'declaration_and_report_unchanged', 'exit', 'files', 'fixture_exact', 'id', 'marker_observed', 'passed', 'phase', 'policy_diagnostic', 'required_hashes', 'required_links', 'stderr', 'stdout', 'utc', 'variants'], 'bool', None], ['cleanup', None, None, None, None, None, ['fixture_directory_absent', 'phase', 'utc'], None, None], ['summary', None, None, None, None, None, ['exit_semantics', 'failures', 'hypothesis_outcome', 'phase', 'result_count', 'unavailable', 'utc'], None, None]]}, 'supplement/extra.jsonl': {'source': 'raw/round-1/final-2-supplement-inputs/v4-extra-selftest.py', 'source_sha256': '5e4dc0dc59711c80a46e547d254400c350726cf499c615a4eaeae3a2b88c757a', 'reviewed_result_count': 21, 'record_contract': [['documentation', None, None, None, None, None, ['established', 'phase', 'sources', 'unknown', 'utc'], None, None], ['expected', None, 'EXTRA-SHELL-DOMAIN', None, None, None, ['before', 'command', 'expected', 'expected_stdout', 'id', 'kind', 'phase', 'stdin_sha256', 'utc', 'variants'], None, None], ['result', None, 'EXTRA-SHELL-DOMAIN', None, None, None, ['after', 'declaration_and_report_unchanged', 'effect_marker_observed', 'files', 'id', 'passed', 'phase', 'rc', 'status', 'stderr', 'stdout', 'utc', 'variants'], 'bool', None], ['expected', None, 'REPL-TYPED', None, None, None, ['before', 'command', 'expected', 'expected_stdout', 'id', 'kind', 'phase', 'stdin_sha256', 'utc', 'variants'], None, None], ['result', None, 'REPL-TYPED', None, None, None, ['after', 'declaration_and_report_unchanged', 'effect_marker_observed', 'files', 'id', 'passed', 'phase', 'rc', 'status', 'stderr', 'stdout', 'utc', 'variants'], 'bool', None], ['fixture_expected', None, None, '0o600', None, None, ['bytes', 'mode', 'path', 'phase', 'sha256', 'utc'], None, None], ['expected', None, 'RC-STARTUP', None, None, None, ['before', 'command', 'expected', 'expected_stdout', 'id', 'kind', 'phase', 'stdin_sha256', 'utc', 'variants'], None, None], ['boundary_result', None, 'RC-STARTUP', None, None, None, ['after', 'declaration_and_report_unchanged', 'effect_marker_observed', 'files', 'id', 'passed', 'phase', 'rc', 'status', 'stderr', 'stdout', 'utc', 'variants'], 'bool', None], ['expected', None, 'EXPORTED-FUNCTION-SUBSTITUTION', None, None, None, ['before', 'command', 'expected', 'expected_stdout', 'id', 'kind', 'phase', 'stdin_sha256', 'utc', 'variants'], None, None], ['result', None, 'EXPORTED-FUNCTION-SUBSTITUTION', None, None, None, ['after', 'declaration_and_report_unchanged', 'effect_marker_observed', 'files', 'id', 'passed', 'phase', 'rc', 'status', 'stderr', 'stdout', 'utc', 'variants'], 'bool', None], ['fixture_expected', None, None, '0o600', None, None, ['bytes', 'mode', 'path', 'phase', 'sha256', 'utc'], None, None], ['expected', None, 'EDITOR-SAVED-COMMANDS', None, None, None, ['before', 'command', 'expected', 'expected_stdout', 'id', 'kind', 'phase', 'stdin_sha256', 'utc', 'variants'], None, None], ['boundary_result', None, 'EDITOR-SAVED-COMMANDS', None, None, None, ['after', 'declaration_and_report_unchanged', 'effect_marker_observed', 'files', 'id', 'passed', 'phase', 'rc', 'status', 'stderr', 'stdout', 'utc', 'variants'], 'bool', None], ['availability', None, 'EDITOR-PLUGIN-MODELINE', None, None, None, ['id', 'phase', 'reason', 'status', 'utc', 'variants'], None, None], ['availability', None, 'GIT-HOOK', None, None, None, ['id', 'path', 'phase', 'reason', 'status', 'utc', 'variants'], None, None], ['availability', None, 'GIT-LOCAL-ALIAS-FILTER', None, None, None, ['id', 'path', 'phase', 'reason', 'status', 'utc', 'variants'], None, None], ['availability', None, 'MAKE-SAVED-RECIPE', None, None, None, ['id', 'path', 'phase', 'reason', 'status', 'utc', 'variants'], None, None], ['expected', None, 'LIBRARY-FIXTURE-COMPILE', None, None, None, ['before', 'command', 'expected', 'expected_stdout', 'id', 'kind', 'phase', 'stdin_sha256', 'utc', 'variants'], None, None], ['result', None, 'LIBRARY-FIXTURE-COMPILE', None, None, None, ['after', 'declaration_and_report_unchanged', 'effect_marker_observed', 'files', 'id', 'passed', 'phase', 'rc', 'status', 'stderr', 'stdout', 'utc', 'variants'], 'NoneType', None], ['expected', None, 'SAVED-LD-PRELOAD', None, None, None, ['before', 'command', 'expected', 'expected_stdout', 'id', 'kind', 'phase', 'stdin_sha256', 'utc', 'variants'], None, None], ['boundary_result', None, 'SAVED-LD-PRELOAD', None, None, None, ['after', 'declaration_and_report_unchanged', 'effect_marker_observed', 'files', 'id', 'passed', 'phase', 'rc', 'status', 'stderr', 'stdout', 'utc', 'variants'], 'bool', None], ['expected', None, 'SAVED-LD-AUDIT', None, None, None, ['before', 'command', 'expected', 'expected_stdout', 'id', 'kind', 'phase', 'stdin_sha256', 'utc', 'variants'], None, None], ['boundary_result', None, 'SAVED-LD-AUDIT', None, None, None, ['after', 'declaration_and_report_unchanged', 'effect_marker_observed', 'files', 'id', 'passed', 'phase', 'rc', 'status', 'stderr', 'stdout', 'utc', 'variants'], 'bool', None], ['expected', None, 'SAVED-FFI', None, None, None, ['before', 'command', 'expected', 'expected_stdout', 'id', 'kind', 'phase', 'stdin_sha256', 'utc', 'variants'], None, None], ['boundary_result', None, 'SAVED-FFI', None, None, None, ['after', 'declaration_and_report_unchanged', 'effect_marker_observed', 'files', 'id', 'passed', 'phase', 'rc', 'status', 'stderr', 'stdout', 'utc', 'variants'], 'bool', None], ['expected', None, 'MEMFD-RUNTIME', None, None, None, ['before', 'command', 'expected', 'expected_stdout', 'id', 'kind', 'phase', 'stdin_sha256', 'utc', 'variants'], None, None], ['result', None, 'MEMFD-RUNTIME', None, None, None, ['after', 'declaration_and_report_unchanged', 'effect_marker_observed', 'files', 'id', 'passed', 'phase', 'rc', 'status', 'stderr', 'stdout', 'utc', 'variants'], 'NoneType', None], ['fixture_expected', None, None, '0o600', None, None, ['bytes', 'mode', 'path', 'phase', 'sha256', 'utc'], None, None], ['expected', None, 'MEMFD-SAVED-INPUT', None, None, None, ['before', 'command', 'expected', 'expected_stdout', 'id', 'kind', 'phase', 'stdin_sha256', 'utc', 'variants'], None, None], ['boundary_result', None, 'MEMFD-SAVED-INPUT', None, None, None, ['after', 'declaration_and_report_unchanged', 'effect_marker_observed', 'files', 'id', 'passed', 'phase', 'rc', 'status', 'stderr', 'stdout', 'utc', 'variants'], 'bool', None], ['availability', None, 'RUNTIME-ARCHITECTURE', None, None, None, ['id', 'machine', 'phase', 'utc'], None, None], ['expected', None, 'JIT-RUNTIME', None, None, None, ['before', 'command', 'expected', 'expected_stdout', 'id', 'kind', 'phase', 'stdin_sha256', 'utc', 'variants'], None, None], ['result', None, 'JIT-RUNTIME', None, None, None, ['after', 'declaration_and_report_unchanged', 'effect_marker_observed', 'files', 'id', 'passed', 'phase', 'rc', 'status', 'stderr', 'stdout', 'utc', 'variants'], 'NoneType', None], ['fixture_expected', None, None, '0o600', None, None, ['bytes', 'mode', 'path', 'phase', 'sha256', 'utc'], None, None], ['expected', None, 'JIT-SAVED-INPUT', None, None, None, ['before', 'command', 'expected', 'expected_stdout', 'id', 'kind', 'phase', 'stdin_sha256', 'utc', 'variants'], None, None], ['boundary_result', None, 'JIT-SAVED-INPUT', None, None, None, ['after', 'declaration_and_report_unchanged', 'effect_marker_observed', 'files', 'id', 'passed', 'phase', 'rc', 'status', 'stderr', 'stdout', 'utc', 'variants'], 'bool', None], ['expected', None, 'PROCESS-MEMORY-RUNTIME', None, None, None, ['before', 'command', 'expected', 'expected_stdout', 'id', 'kind', 'phase', 'stdin_sha256', 'utc', 'variants'], None, None], ['result', None, 'PROCESS-MEMORY-RUNTIME', None, None, None, ['after', 'declaration_and_report_unchanged', 'effect_marker_observed', 'files', 'id', 'passed', 'phase', 'rc', 'status', 'stderr', 'stdout', 'utc', 'variants'], 'NoneType', None], ['expected', None, 'BINFMT-REGISTER', None, None, None, ['before', 'command', 'expected', 'expected_stdout', 'id', 'kind', 'phase', 'stdin_sha256', 'utc', 'variants'], None, None], ['result', None, 'BINFMT-REGISTER', None, None, None, ['after', 'declaration_and_report_unchanged', 'effect_marker_observed', 'files', 'id', 'passed', 'phase', 'rc', 'status', 'stderr', 'stdout', 'utc', 'variants'], 'NoneType', None], ['boundary_result', None, 'BINFMT-EFFECT', None, None, None, ['effective_entry', 'id', 'passed', 'phase', 'status', 'utc', 'variants'], 'bool', None], ['availability', None, 'FOREIGN-INTERPRETER', None, None, None, ['available_runtimes', 'id', 'phase', 'reason', 'status', 'utc', 'variants'], None, None], ['fixture_expected', None, None, '0o600', None, None, ['bytes', 'mode', 'path', 'phase', 'sha256', 'utc'], None, None], ['expected', None, 'DISPATCHER-INSTALL', None, None, None, ['command', 'exact_row', 'expected', 'id', 'phase', 'utc', 'variants'], None, None], ['result', None, 'DISPATCHER-INSTALL', None, None, None, ['id', 'identity', 'passed', 'phase', 'rc', 'readback_failures', 'stderr', 'stdout', 'utc'], 'bool', None], ['expected', None, 'DISPATCHER-TYPED', None, None, None, ['before', 'command', 'expected', 'expected_stdout', 'id', 'kind', 'phase', 'stdin_sha256', 'utc', 'variants'], None, None], ['result', None, 'DISPATCHER-TYPED', None, None, None, ['after', 'declaration_and_report_unchanged', 'effect_marker_observed', 'files', 'id', 'passed', 'phase', 'rc', 'status', 'stderr', 'stdout', 'utc', 'variants'], 'bool', None], ['fixture_expected', None, None, '0o600', None, None, ['bytes', 'mode', 'path', 'phase', 'sha256', 'utc'], None, None], ['expected', None, 'DISPATCHER-SAVED', None, None, None, ['before', 'command', 'expected', 'expected_stdout', 'id', 'kind', 'phase', 'stdin_sha256', 'utc', 'variants'], None, None], ['boundary_result', None, 'DISPATCHER-SAVED', None, None, None, ['after', 'declaration_and_report_unchanged', 'effect_marker_observed', 'files', 'id', 'passed', 'phase', 'rc', 'status', 'stderr', 'stdout', 'utc', 'variants'], 'bool', None], ['expected', None, 'DISPATCHER-REMOVE', None, None, None, ['expected', 'id', 'phase', 'utc'], None, None], ['result', None, 'DISPATCHER-REMOVE', None, None, None, ['id', 'passed', 'phase', 'rc', 'stderr', 'stdout', 'utc'], 'bool', None], ['availability', None, 'BROWSER-EXTENSION', None, None, None, ['browser_present', 'documentation', 'id', 'phase', 'reason', 'status', 'utc', 'variants'], None, None], ['result', None, 'EXTRA-FINAL-RESTORATION', None, None, None, ['declaration_bytes_restored', 'id', 'passed', 'phase', 'readback_count', 'readback_failures', 'utc'], 'bool', None], ['summary', None, None, None, None, None, ['boundary_failures', 'closure_claim', 'hypothesis_outcome', 'implementation_failures', 'phase', 'runtime_observations', 'untested', 'utc'], None, None]]}}
CARRIED = {'language.jsonl': '6f0992f4d80a8be85392a90c9f08bbbea9cf6f866c69d32e17004a538092e6b9', 'applications.jsonl': '77eec48cd5786de2bce6725dc6f44681452bded18663a7f86bcdadc457469368', 'system.jsonl': '9eff66c5fea968c959e44c0df57a05979abd13146d9be605cdafb09d9b790252', 'ordinary.jsonl': '7805aa1e69a1e08747f29b0c83418043d7b09d97e4e72bc2925a977a0adbb5a7', 'regressions/round1.jsonl': 'fdda52fd26f4ca49eb46e417a4a68840fbbf582e73c7be36c9e9983cc18241e2', 'regressions/round2.jsonl': '6414a81479d2f834ed8fbee1c1dc085fc9595cd21396cae868aaf9b1dea4dda2', 'regressions/round3.jsonl': '506471ffba7a670f020cc1eb5de886934971da63e81c9a10384bf30d0d27305e', 'regressions/powercuts.jsonl': '15a40f0378eae4adcb4f0526fde5660457c83b56c6e8ffe5a1684e7159f9f007', 'events.jsonl': 'db8c69185e49569f944e4d933fa2609705057e279801264dff9198128a5a9203'}
REQUIRED_CARRIED = ['applications-examples-export.log', 'applications-examples/channel-examples/appimage.jsonl', 'applications-examples/channel-examples/flatpak.jsonl', 'applications-examples/channel-examples/oci.jsonl', 'applications-helper-availability.jsonl', 'applications-new.log', 'applications-verify.jsonl', 'applications.jsonl', 'bc4-final-2-applications-destroy.log', 'bc4-final-2-language-destroy.log', 'bc4-final-2-ordinary-destroy.log', 'bc4-final-2-system-destroy.log', 'events.jsonl', 'factory-export.log', 'factory-export/factory/base-files.json', 'factory-export/factory/machine.jsonl', 'language-examples-export.log', 'language-examples/channel-examples/npm.jsonl', 'language-examples/channel-examples/pip-native.jsonl', 'language-examples/channel-examples/pip.jsonl', 'language-new.log', 'language-verify.jsonl', 'language.jsonl', 'ordinary-examples-export.log', 'ordinary-examples/channel-examples/ordinary.jsonl', 'ordinary-new.log', 'ordinary-verify.jsonl', 'ordinary.jsonl', 'recipe-sha256.json', 'regressions-console.jsonl', 'regressions/bc3-bc4-final-2-copy-round3-selftest.py.log', 'regressions/bc3-bc4-final-2-destroy.log', 'regressions/bc3-bc4-final-2-new.log', 'regressions/bc3-inventory-bc4-final-2-copy-round3-inventory-test.py.log', 'regressions/bc3-inventory-bc4-final-2-destroy.log', 'regressions/bc3-inventory-bc4-final-2-new.log', 'regressions/bc3-peer-a-destroy.log', 'regressions/bc3-peer-a-new.log', 'regressions/bc3-peer-b-destroy.log', 'regressions/bc3-peer-b-new.log', 'regressions/bc3-regression1-bc4-final-2-copy-round1-selftest.py.log', 'regressions/bc3-regression1-bc4-final-2-destroy.log', 'regressions/bc3-regression1-bc4-final-2-new.log', 'regressions/bc3-regression2-bc4-final-2-copy-round2-probe.c.log', 'regressions/bc3-regression2-bc4-final-2-copy-round2-selftest.py.log', 'regressions/bc3-regression2-bc4-final-2-destroy.log', 'regressions/bc3-regression2-bc4-final-2-new.log', 'regressions/boot-attempts.json', 'regressions/boot-delay-cleanup.log', 'regressions/boot-delay-setup.log', 'regressions/boot-gate-stop.log', 'regressions/boot-order.jsonl', 'regressions/boot-start.log', 'regressions/independent-compare.json', 'regressions/independent-stand-compare.jsonl', 'regressions/inventory.jsonl', 'regressions/original-console.log', 'regressions/original/D01.log', 'regressions/original/D02.log', 'regressions/original/D03.log', 'regressions/original/D04.log', 'regressions/original/D05.log', 'regressions/original/D06.log', 'regressions/original/D07.log', 'regressions/original/D08.log', 'regressions/original/D09.log', 'regressions/original/D10-compare.jsonl', 'regressions/original/D10-peer-a.log', 'regressions/original/D10-peer-b.log', 'regressions/original/D10-summary.log', 'regressions/original/cleanup-cut.log', 'regressions/original/create-cut.log', 'regressions/original/create-dev.log', 'regressions/original/create-peer-a.log', 'regressions/original/create-peer-b.log', 'regressions/original/cut/last-success.json', 'regressions/original/destroy-dev.log', 'regressions/original/destroy-peer-a.log', 'regressions/original/destroy-peer-b.log', 'regressions/original/dev/evidence/added.json', 'regressions/original/dev/evidence/factory.json', 'regressions/original/dev/evidence/packages.tsv', 'regressions/original/example/factory/base-files.json', 'regressions/original/example/factory/machine.jsonl', 'regressions/original/export-cut.log', 'regressions/original/export-declaration-peer-a.log', 'regressions/original/export-declaration-peer-b.log', 'regressions/original/export-dev.log', 'regressions/original/export-example.log', 'regressions/original/export-peer-a.log', 'regressions/original/export-peer-b.log', 'regressions/original/peer-a/added.json', 'regressions/original/peer-a/dev-add/base-files.json', 'regressions/original/peer-a/dev-add/machine.jsonl', 'regressions/original/peer-b/added.json', 'regressions/original/peer-b/dev-add/base-files.json', 'regressions/original/peer-b/dev-add/machine.jsonl', 'regressions/peer-a-apply.log', 'regressions/peer-a-declaration-export.log', 'regressions/peer-a-snapshot-export.log', 'regressions/peer-a/added.json', 'regressions/peer-a/dev-add/base-files.json', 'regressions/peer-a/dev-add/machine.jsonl', 'regressions/peer-b-apply.log', 'regressions/peer-b-declaration-export.log', 'regressions/peer-b-snapshot-export.log', 'regressions/peer-b/added.json', 'regressions/peer-b/dev-add/base-files.json', 'regressions/peer-b/dev-add/machine.jsonl', 'regressions/powercuts.jsonl', 'regressions/round1.jsonl', 'regressions/round2.jsonl', 'regressions/round3.jsonl', 'regressions/summary.json', 'summary.json', 'system-examples-export.log', 'system-examples/channel-examples/repository.jsonl', 'system-examples/channel-examples/system-update.jsonl', 'system-new.log', 'system-state-export.log', 'system-state/channel-system-state/machine.jsonl', 'system-verify.jsonl', 'system.jsonl']
REQUIRED_COMBINED = ['a-apply.log', 'a-deliver.log', 'a-destroy.log', 'a-exact.jsonl', 'a-launch-appimage.log', 'a-launch-download.log', 'a-launch-flatpak.log', 'a-launch-native-wheel.log', 'a-launch-npm.log', 'a-launch-oci.log', 'a-launch-pip.log', 'a-launch-repository.log', 'a-launch-source-build.log', 'a-launch-updated-base.log', 'a-launch-user-service-program.log', 'a-new.log', 'a-reboot-exact.jsonl', 'a-reboot-verify.jsonl', 'a-schedule.jsonl', 'a-snapshot.json', 'a-start.log', 'a-stop.log', 'a-verify.jsonl', 'b-apply.log', 'b-deliver.log', 'b-destroy.log', 'b-exact.jsonl', 'b-launch-appimage.log', 'b-launch-download.log', 'b-launch-flatpak.log', 'b-launch-native-wheel.log', 'b-launch-npm.log', 'b-launch-oci.log', 'b-launch-pip.log', 'b-launch-repository.log', 'b-launch-source-build.log', 'b-launch-updated-base.log', 'b-launch-user-service-program.log', 'b-new.log', 'b-reboot-exact.jsonl', 'b-reboot-verify.jsonl', 'b-schedule.jsonl', 'b-snapshot.json', 'b-start.log', 'b-stop.log', 'b-verify.jsonl', 'events.jsonl', 'provenance.json', 'stand-compare.jsonl', 'summary.json']
COMBINED_EVENTS_SHA = 'a39c124bad0ccd250cecc6a1ff77f6ff698fdb6c5ec65bdc99914b8ada7c7183'

ADAPTER_SHA = '111ecd9b9f3857387dc0c2a38976150c880d20db615cca2f05a8f2b2fc7777b9'
APP_SUITE_SHA = 'ce0074b2329e0aa9554a4187ceed46890113a4eb4264a9281f930eb6be6cc41f'
ORDINARY_SUITE_SHA = 'e72ef3e2d88a29f42127bf9979774a9067543365509843bec76e513ce74be9b7'
CARRIED_DRIVER_SHA = 'bd79bfbed47a7d4ee5327c52eea5b940e944ea37b2906c7d86449b6182e087af'
MAIN_CONTROLLER_SHA = '0394eb1a9b673447d2249b9a6fd563b060275db057d353f45639965f81af6c02'

class EvidenceError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise EvidenceError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate JSON key: ' + key)
        result[key] = value
    return result


def decode(text, context):
    try:
        value = json.loads(text, object_pairs_hook=unique_object,
                           parse_constant=lambda value: (_ for _ in ()).throw(EvidenceError('nonfinite JSON')))
    except ValueError as exc:
        raise EvidenceError(f'{context}: {exc}') from exc
    require(isinstance(value, dict), f'{context}: expected JSON object')
    return value


def lines(path):
    data = path.read_text(encoding='utf-8', errors='strict')
    require(bool(data) and data.endswith('\n'), f'{path}: empty or truncated file')
    return data.splitlines()


def records(path):
    return [decode(line, f'{path}:{number}') for number, line in enumerate(lines(path), 1)]



def json_value(path, expected_type):
    value = json.loads(path.read_text(encoding='utf-8', errors='strict'), object_pairs_hook=unique_object,
                       parse_constant=lambda value: (_ for _ in ()).throw(EvidenceError('nonfinite JSON')))
    require(type(value) is expected_type, f'{path}: wrong JSON document type')
    return value


def document(path):
    return decode(path.read_text(encoding='utf-8', errors='strict'), str(path))


def signature(row):
    return [row.get('phase'), row.get('event'), row.get('id'), row.get('mode'),
            row.get('log'), row.get('summary'), sorted(row),
            type(row.get('passed')).__name__ if 'passed' in row else None,
            type(row.get('ok')).__name__ if 'ok' in row else None]


def declaration(path):
    result = {}
    for row in records(path):
        ident, kind = row.get('id'), row.get('type')
        require(isinstance(ident, str) and isinstance(kind, str), f'{path}: declaration identity missing')
        require(ident not in result, f'{path}: duplicate declaration {ident}')
        result[ident] = kind
    require(bool(result), f'{path}: empty declaration')
    return result


def verify_lines(text, expected, context):
    found = {}
    for number, line in enumerate(text, 1):
        fields = line.split('\t')
        require(len(fields) == 4, f'{context}:{number}: expected four TAB-separated fields')
        ident, kind, status, digest = fields
        require(ident not in found, f'{context}:{number}: duplicate {ident}')
        require(status in ('OK', 'FAIL'), f'{context}:{number}: unknown status {status}')
        require(re.fullmatch('[0-9a-f]{64}', digest) is not None, f'{context}:{number}: invalid digest')
        require(status == 'OK', f'{context}:{number}: failed readback {ident}')
        found[ident] = kind
    require(found == expected, f'{context}: declaration ID/type inventory differs; missing={sorted(expected.keys()-found.keys())}, extra={sorted(found.keys()-expected.keys())}')
    return {'rows': len(found), 'ok': len(found), 'bad': []}


def verify(path, expected):
    return {'file': str(path.relative_to(RAW)), 'sha256': sha(path),
            **verify_lines(lines(path), expected, path)}


def result_rows(rows):
    return [r for r in rows if r.get('id') and
            (r.get('phase') in ('result', 'assert', 'assertion', 'boundary', 'boundary_result')
             or ('mode' in r and 'ok' in r))]


def reconcile(rows, context):
    tests = result_rows(rows)
    keys = [(r.get('phase'), r['id'], r.get('mode')) for r in tests]
    require(len(keys) == len(set(keys)), f'{context}: duplicate result identity/phase')
    failures = [r for r in tests if r.get('passed', r.get('ok')) is False]
    summaries = [r for r in rows if r.get('phase') == 'summary' or r.get('event') == 'summary' or r.get('summary') is True]
    for summary in summaries:
        regular = [r for r in failures if r.get('phase') not in ('boundary', 'boundary_result')]
        labels = [r['id'] + (':' + r['mode'] if 'mode' in r else '') for r in regular]
        for field in ('failed', 'failures'):
            if field in summary:
                require(summary[field] == labels, f'{context}: {field} does not reconcile')
        if 'boundary_failures' in summary:
            boundary = [r['id'] for r in failures if r.get('phase') == 'boundary']
            if not any(r.get('phase') == 'boundary' for r in tests):
                boundary = [r['id'] for r in failures]
            require(summary['boundary_failures'] == boundary, f'{context}: boundary failure summary differs')
        if 'implementation_failures' in summary:
            require(summary['implementation_failures'] == [r['id'] for r in regular], f'{context}: implementation failure summary differs')
        if 'implemented_checks_passed' in summary:
            required_failures = [r for r in failures if r.get('requirement') is True]
            require(summary['implemented_checks_passed'] == (not required_failures), f'{context}: implemented status differs')
        for field in ('tests', 'result_count'):
            if field in summary:
                require(summary[field] == len(tests), f'{context}: result count differs')
        for field in ('passed', 'ok'):
            if field in summary:
                require(type(summary[field]) is bool and summary[field] == (not regular), f'{context}: summary status differs')
        if 'runtime_observations' in summary:
            actual = [{'id': r['id'], 'status': r['status']} for r in tests if r.get('status', '').startswith('RUNTIME_')]
            require(summary['runtime_observations'] == actual, f'{context}: runtime observations differ')
        if 'untested' in summary:
            actual = [r['id'] for r in rows if r.get('phase') == 'availability' and r.get('status') == 'UNTESTED']
            require(summary['untested'] == actual, f'{context}: untested list differs')
    return tests, failures, summaries


def info(path, rows):
    tests, failures, summaries = reconcile(rows, path)
    booleans = [r for r in tests if type(r.get('passed', r.get('ok'))) is bool]
    return {'file': str(path.relative_to(RAW)), 'sha256': sha(path),
            'result_rows':len(tests), 'assertions': len(booleans), 'passed': sum(r.get('passed', r.get('ok')) for r in booleans),
            'observations_without_boolean_verdict': len(tests)-len(booleans),
            'failed': [r['id'] + (':' + r['mode'] if 'mode' in r else '') for r in failures],
            'summaries': summaries}


def powercut_records(path, factory, baseline=False):
    """Nine trials, each with explicit three-line transport and complete readback."""
    rows, block, counts = [], [], collections.Counter()
    for number, line in enumerate(lines(path), 1):
        context = f'{path}:{number}'
        if line.startswith('{'):
            row = decode(line, context)
            if row.get('phase') == 'result':
                ident = row.get('id', '')
                expected = dict(factory)
                if '-REMOVE-' not in ident:
                    expected.update({'dev-worker':'program', 'dev-service':'service', 'dev-rule':'rule'})
                verify_lines(block, expected, context)
                block = []
                require(counts == {'utc':1, 'candidate':1, 'unit':1}, f'{context}: missing/duplicate powercut transport')
                counts.clear()
            rows.append(row)
        elif '\t' in line:
            block.append(line)
        elif re.fullmatch(r'UTC \d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ OP prepare-(add|change|remove)', line):
            counts['utc'] += 1
        elif re.fullmatch(r'CANDIDATE /var/lib/stand/cut-(add|change|remove)', line):
            counts['candidate'] += 1
        elif re.fullmatch(r'Running as unit: stand-[a-zA-Z0-9-]+\.service; invocation ID: [0-9a-f]{32}', line):
            counts['unit'] += 1
        else:
            raise EvidenceError(f'{context}: unrecognized powercut transport')
    require(not block and not counts, f'{path}: unfinished powercut trial')
    return rows


def normalized_contract(rows):
    result = []
    for row in rows:
        entry = signature(row)
        if entry[4]:
            entry[4] = entry[4].replace('baseline', 'final-2')
        cleanup_ids = {'CLEANUP-bc4-baseline-'+name:'CLEANUP-bc4-final-2-'+name
                       for name in ('language','applications','system','ordinary')}
        if entry[0] == 'expected' and entry[2] in cleanup_ids:
            require(sha(ROOT/'build/round4-driver.py') == CARRIED_DRIVER_SHA,
                    'carried driver source differs from cleanup identity contract')
            entry[2] = cleanup_ids[entry[2]]
        result.append(entry)
    return result


def adapted_command(argv):
    """Exact transformation in the SHA-pinned v4-suite-adapter.py."""
    if not isinstance(argv, list) or '/usr/local/bin/stand-session' not in argv:
        return None
    argv = list(map(str, argv))
    index = argv.index('/usr/local/bin/stand-session')
    if len(argv) != index + 3 or argv[index+1] != '-c':
        return None
    fields = argv[index+2].split('\t')
    if fields[0] == 'broker':
        require(len(fields) >= 2, 'malformed pinned broker command')
        command = shlex.join(['/usr/local/bin/'+fields[1], *fields[2:]])
    else:
        command = shlex.join(argv[index:])
    return argv[:index] + ['/usr/local/bin/stand-shell', '-c', command]


def adapted_rows(path, expected):
    """Require exact payload and placement, preserving the audited routing proof."""
    require(sha(ROOT/'build/v4-suite-adapter.py') == ADAPTER_SHA,
            'adapter source differs from the reviewed transformation')
    raw = records(path)
    holder = None
    download = None
    dynamic_bindings = []
    if path.name == 'ordinary.jsonl':
        require(sha(ROOT/'build/round4-selftest.py') == ORDINARY_SUITE_SHA,
                'ordinary download fixture source differs')
        positions = [index for index,row in enumerate(raw)
                     if row.get('phase') == 'expected' and row.get('id') == 'DOWNLOAD']
        require(len(positions) == 1 and positions[0]+1 < len(raw), f'{path}: download expectation missing/duplicate')
        marker = raw[positions[0]+1]
        require(marker.get('phase') == 'v4-shell-entry', f'{path}: download marker must immediately follow its expectation')
        # round4-selftest.py binds HTTPServer(('127.0.0.1',0), Handler).
        # Only the resulting nonzero TCP port varies; wrapper, URL, resource,
        # arguments and canonical shell quoting are exact source literals.
        template = ['/usr/sbin/runuser','-u','stand','--','/usr/local/bin/stand-session',
                    '-c','run\t/usr/bin/curl\thttp://127.0.0.1:{port}/development']
        adapted = adapted_command(template)
        actual = marker.get('actual_command')
        require(isinstance(actual,list) and len(actual) == len(adapted) and actual[:-1] == adapted[:-1] and isinstance(actual[-1],str), f'{path}: invalid download wrapper')
        prefix, suffix = adapted[-1].split('{port}')
        matched = re.fullmatch(re.escape(prefix)+r'([1-9][0-9]{0,4})'+re.escape(suffix),actual[-1])
        require(matched is not None, f'{path}: download command differs from source template')
        port = int(matched.group(1))
        require(1 <= port <= 65535, f'{path}: invalid download TCP port')
        download = template[:-1] + [template[-1].format(port=port)]
        dynamic_bindings.append({'expected_id':'DOWNLOAD','port':port,'source_sha256':ORDINARY_SUITE_SHA,
                                 'contract':'HTTPServer loopback bind with port zero; exact curl URL /development; resulting TCP port 1..65535'})
    if path.name == 'applications.jsonl':
        require(sha(ROOT/'build/app-selftest.py') == APP_SUITE_SHA,
                'application holder call source differs')
        holder_rows = [r for r in expected if r.get('phase') == 'expected' and r.get('id') == 'OCI-HOLDER-REMOVED-PATH']
        require(len(holder_rows) == 1, 'pinned holder entry absent')
        # app-selftest.py uses ordinary('run', holder) for both START and REMOVED-PATH.
        holder = holder_rows[0]['command']
    planned = []
    for index, row in enumerate(expected):
        if row.get('phase') != 'expected':
            continue
        argv = holder if row.get('id') == 'OCI-HOLDER-START' else (download if row.get('id') == 'DOWNLOAD' else row.get('command'))
        adapted = adapted_command(argv)
        if adapted is not None:
            planned.append({'after_record':index, 'after_expected_id':row['id'],
                            'actual_command':adapted})
    rows, markers = [], []
    for row in raw:
        if row.get('phase') != 'v4-shell-entry':
            rows.append(row)
            continue
        require(set(row) == {'phase','actual_command','utc'}, f'{path}: unknown adapter schema')
        require(isinstance(row['utc'], str) and re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ',row['utc']), f'{path}: invalid marker timestamp')
        require(rows and rows[-1].get('phase') == 'expected', f'{path}: marker is not after an expected command')
        markers.append({'after_record':len(rows)-1, 'after_expected_id':rows[-1].get('id'),
                        'actual_command':row['actual_command']})
    require(markers == planned, f'{path}: shell marker payload/order/expected correspondence differs')
    serialized = json.dumps(markers, sort_keys=True, separators=(',',':')).encode()
    transport = {'marker_count':len(markers), 'ordered_markers_sha256':hashlib.sha256(serialized).hexdigest(),
                 'markers':markers, 'dynamic_bindings':dynamic_bindings, 'adapter_source_sha256':ADAPTER_SHA,
                 'provenance':'Exact adapter transformation of SHA-pinned baseline expected commands; holder START uses the source-identical REMOVED-PATH entry; DOWNLOAD uses the pinned literal loopback fixture template with a bounded dynamic TCP port.'}
    return rows, transport


def compare_contract(rows, expected, context):
    require(normalized_contract(rows) == normalized_contract(expected), f'{context}: missing, duplicate, reordered, unknown, or schema/phase-changed record')


def false_observations(rows, path):
    found = []
    for row in rows:
        is_summary = row.get('phase') == 'summary' or row.get('event') == 'summary' or row.get('summary') is True
        if is_summary:
            continue
        fields = [key for key in ('passed','ok','equal') if row.get(key) is False]
        if 'log' in row and 'rc' in row and row['rc'] != 0:
            fields.append('rc_nonzero')
        if fields:
            found.append({'file': str(path.relative_to(RAW)), 'phase': row.get('phase', row.get('event', 'legacy-result')),
                          'id': row.get('id'), 'mode': row.get('mode'), 'log': row.get('log'),
                          'false_fields': fields,
                          'label': 'explicit-boundary' if row.get('phase') in ('boundary','boundary_result') or row.get('requirement') is False else 'suite-observation'})
    return found


def comparisons(path, expected):
    rows = records(path)
    found = {}
    for row in rows:
        require(set(row) == {'id','equal','left','right'} and type(row['equal']) is bool, f'{path}: comparison schema')
        ident = row['id']
        require(ident not in found, f'{path}: duplicate comparison {ident}')
        for side in ('left','right'):
            value = row[side]
            require(isinstance(value,dict) and value.get('id') == ident and value.get('type') == expected.get(ident) and type(value.get('ok')) is bool, f'{path}: invalid {side} comparison')
        require(row['equal'] == (row['left'] == row['right']), f'{path}: comparison verdict inconsistent')
        found[ident] = row['left']['type']
    require(found == expected, f'{path}: comparison inventory differs')
    return rows


def require_files(directory, names):
    """Exact recursive file inventory; unknown evidence must be reviewed first."""
    require(directory.is_dir() and not directory.is_symlink(), f'missing or symlink evidence root: {directory}')
    expected = set(names)
    require(len(expected) == len(names), f'{directory}: duplicate inventory contract')
    actual = set()
    for path in directory.rglob('*'):
        require(not path.is_symlink(), f'{path}: evidence symlinks are not permitted')
        if path.is_dir():
            continue
        require(path.is_file(), f'{path}: nonregular evidence entry')
        actual.add(path.relative_to(directory).as_posix())
    require(actual == expected, f'{directory}: exact file inventory differs; missing={sorted(expected-actual)}, extra={sorted(actual-expected)}')



def expected_main_steps():
    """Success path in the pinned tools/round1.py; no target-log inference."""
    steps = []
    def add(argv, log, legacy=False):
        steps.append({'argv':argv,'log':log,'expected_exit':0,'legacy_protocol':legacy})
    def lab(op, name, log, *extra):
        add(['python3','lab.py',op,name,*extra],log)
    add(['python3','build/build.py','--server','--replace'],'build.log')
    for suite in ('shell','gate','tools'):
        name = 'v4-final-2-'+suite
        lab('new',name,suite+'-new.log','stand')
        if suite == 'shell':
            lab('run',name,'login.log')
        lab('run',name,suite+'.jsonl','--root')
        if suite == 'shell':
            lab('stop',name,'shell-stop.log')
            lab('start',name,'shell-start.log')
            lab('run',name,'shell-reboot.jsonl','--root')
        lab('run',name,suite+'-verify.log','--root')
        if suite == 'tools':
            lab('copy-out',name,'factory-export.log','/etc/stand/factory','[stand-root]/raw/round-1/final-2/factory')
        lab('destroy',name,name+'-destroy.log')
    add(['python3','build/build.py','--server'],'peer-build.log')
    add(['python3','build/round4-driver.py','final-2','--regressions','--peer-root','round1-peer'],'regressions-console.jsonl',True)
    add(['python3','build/assemble-channel-examples.py','[stand-root]/raw/round-1/final-2/carried-suite','round1-example'],'assemble.log',True)
    add(['python3','build/combined-selftest.py','v4-final-2','round1-example/combined','--peer-root','round1-peer','--reboot'],'combined-console.jsonl',True)
    return steps


def main_controller(summary, directory):
    require(sha(ROOT/'tools/round1.py') == MAIN_CONTROLLER_SHA, 'main controller source differs from reviewed step contract')
    require(set(summary) == {'utc','controller_exit','steps','remaining_vms','peer_remaining','hypothesis_outcome'}, 'main controller summary schema differs')
    require(type(summary['controller_exit']) is int and summary['controller_exit'] == 0, 'main controller failed')
    require(summary['remaining_vms'] == [] and summary['peer_remaining'] is False, 'main controller cleanup incomplete')
    require(summary['hypothesis_outcome'] == '?', 'main controller may not infer hypothesis acceptance')
    expected = expected_main_steps()
    steps = summary['steps']
    require(isinstance(steps,list) and len(steps) == len(expected), 'main controller step inventory missing/extra')
    require(steps == json_value(directory/'steps.json',list), 'main summary/steps.json disagreement')
    utc_pattern = r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ'
    require(isinstance(summary['utc'],str) and re.fullmatch(utc_pattern,summary['utc']), 'main controller timestamp malformed')
    for step, contract in zip(steps,expected):
        require(isinstance(step,dict) and set(step) == set(contract)|{'started_utc','ended_utc','exit'}, 'main step schema differs')
        require({key:step[key] for key in contract} == contract, f'main step payload/order differs: {contract["log"]}')
        require(type(step['expected_exit']) is int and type(step['exit']) is int and step['exit'] == step['expected_exit'], f'main controller failed step: {contract["log"]}')
        require(type(step['legacy_protocol']) is bool, 'main step legacy flag must be Boolean')
        for key in ('started_utc','ended_utc'):
            require(isinstance(step[key],str) and re.fullmatch(utc_pattern,step[key]), f'main step {key} malformed')
        require(step['started_utc'] <= step['ended_utc'], 'main step timestamps reversed')
        path = directory/step['log']
        require(path.is_file() and not path.is_symlink(), f'missing main controller step output: {path}')
    return {'source_sha256':MAIN_CONTROLLER_SHA,'expected_steps':expected,'step_count':len(expected),'steps_file_sha256':sha(directory/'steps.json')}


def controller(summary, context, field='suite_exit'):
    require(type(summary.get(field)) is int and summary[field] == 0, f'{context}: unsuccessful or missing {field}')
    for key in ('owned_vms_remaining', 'vms_remaining'):
        if key in summary:
            require(summary[key] == [], f'{context}: remaining owned machines')
    if 'remaining_owned_vm' in summary:
        require(summary['remaining_owned_vm'] is False, f'{context}: owned machine remains')
    for step in summary.get('steps', []):
        require(type(step.get('exit')) is int and step['exit'] == step.get('expected_exit', 0), f'{context}: failed controller step {step.get("log")}')



def ancillary(carried, factory):
    failures = []
    pins = {'regressions-console.jsonl': '5be25ab5921d48f49aed8eec14e1ea1ee900d082efcaa5cecbf3561f00f250af', 'regressions/boot-order.jsonl': 'da21aaa6f2dae47268f4641ad367bffbb744aee34471103904e461ec16b4a8b5', 'applications-helper-availability.jsonl': '5bd7bd0497d2e866f0e3b99e1ba95fe474c8c600f0790c98bb61fdd7ffcb135f'}
    for name, digest in pins.items():
        require(sha(BASE/name) == digest, f'{name}: ancillary baseline changed')
        path = carried/name
        if name == 'regressions/boot-order.jsonl':
            text = lines(path)
            values = [decode(text[0], str(path))]
            expected = [decode(lines(BASE/name)[0], str(BASE/name))]
            compare_contract(values, expected, path)
            nonblank = [line for line in text[1:] if line]
            require(len(nonblank) == 8, f'{path}: boot-order transport count')
            for i, unit in enumerate(('getty@tty1.service','serial-getty@ttyS0.service','systemd-logind.service','systemd-user-sessions.service')):
                for line, prefix in ((nonblank[2*i], unit+' Requires='), (nonblank[2*i+1], 'After=')):
                    require(line.startswith(prefix) and re.fullmatch(r'[A-Za-z0-9@_. \\"=-]+', line) is not None, f'{path}: malformed unit transport')
                    require('stand-replay.service' in line[len(prefix):].split(), f'{path}: replay ordering missing')
        else:
            values = records(path)
            compare_contract(values, records(BASE/name), path)
        failures.extend(false_observations(values, path))
    path = carried/'regressions/inventory.jsonl'
    text = lines(path)
    baseline_text = lines(BASE/'regressions/inventory.jsonl')
    require(text[0] == baseline_text[0] and text[-1] == baseline_text[-1], f'{path}: inventory transport differs')
    values = [decode(line, f'{path}:{i}') for i,line in enumerate(text[1:-1],2)]
    require(values[-1].get('kind') == 'summary' and values[-1].get('complete') is False, f'{path}: inventory summary missing')
    counts = collections.Counter()
    for row in values[:-1]:
        require(row.get('status') in ('covered','unknown','unrecorded') and 'object' in row and 'kind' in row, f'{path}: inventory row schema')
        counts[row['status']] += 1
    require(dict(counts) == values[-1].get('counts'), f'{path}: inventory counts differ')
    failures.extend(false_observations(values, path))
    path = carried/'regressions/independent-compare.json'
    comparison = document(path)
    require(set(comparison) == {'declaration_bytes_equal','values_equal','left','right'}, f'{path}: independent comparison schema')
    expected = declaration(carried/'regressions/peer-a/dev-add/machine.jsonl')
    for side in ('left','right'):
        require(isinstance(comparison[side], list), f'{path}: missing comparison side')
        found = {}
        for row in comparison[side]:
            ident = row.get('id')
            require(isinstance(ident,str) and ident not in found and type(row.get('ok')) is bool, f'{path}: duplicate/invalid comparison row')
            found[ident] = row.get('type')
            if row['ok'] is False:
                failures.append({'file':str(path.relative_to(RAW)), 'phase':'independent-comparison', 'id':ident, 'side':side, 'false_fields':['ok'], 'label':'carried-readback'})
        require(found == expected, f'{path}: comparison side inventory differs')
    for field in ('declaration_bytes_equal','values_equal'):
        require(type(comparison[field]) is bool, f'{path}: comparison verdict missing')
        if comparison[field] is False:
            failures.append({'file':str(path.relative_to(RAW)), 'phase':'independent-comparison', 'id':field, 'false_fields':[field], 'label':'carried-comparison'})
    require(comparison['values_equal'] == (comparison['left'] == comparison['right']), f'{path}: values verdict differs')
    a = carried/'regressions/peer-a/dev-add/machine.jsonl'
    b = carried/'regressions/peer-b/dev-add/machine.jsonl'
    require(comparison['declaration_bytes_equal'] == (a.read_bytes() == b.read_bytes()), f'{path}: declaration verdict differs')
    return failures


def main(check_only=False):
    carried, combined = FINAL / 'carried-suite', FINAL / 'combined'
    require_files(carried, REQUIRED_CARRIED)
    require_files(combined, REQUIRED_COMBINED)
    factory_path = ROOT / 'example/round-1/factory/machine.jsonl'
    combined_path = ROOT / 'example/round-1/combined/machine.jsonl'
    factory, combined_decl = declaration(factory_path), declaration(combined_path)
    require(factory == declaration(carried/'factory-export/factory/machine.jsonl'), 'exported factory identity inventory differs')
    summary = document(FINAL / 'summary.json')
    main_contract = main_controller(summary, FINAL)
    out = {'controller': summary, 'image': document(FINAL / 'image.json'),
           'peer_image': document(FINAL / 'peer-image.json'), 'new': {}, 'carried': {},
           'readback': [], 'hypothesis_outcome': '?',
           'inventory_provenance': {'main_controller':main_contract, 'new': {name: {k:v for k,v in spec.items() if k != 'record_contract'} for name,spec in NEW.items()},
                                    'carried_baseline_sha256': CARRIED, 'combined_baseline_events_sha256': COMBINED_EVENTS_SHA,
                                    'required_carried_files': REQUIRED_CARRIED, 'required_combined_files': REQUIRED_COMBINED},
           'interpretation': 'Implementation and compatible sealed-launch passes do not cancel saved-code or native built-in-tool boundary failures. False observations below include all validated assertion-bearing new, carried, and combined logs; no closure is inferred.'}
    failures = []
    for name, spec in NEW.items():
        require(sha(ROOT / spec['source']) == spec['source_sha256'], f'{name}: source provenance changed')
        path = FINAL / name
        rows = records(path)
        require([signature(r) for r in rows] == spec['record_contract'], f'{path}: exact source-reviewed phase/ID/schema inventory differs')
        require(len(result_rows(rows)) == spec['reviewed_result_count'], f'{path}: result inventory count differs')
        out['new'][name] = info(path, rows)
        failures.extend(false_observations(rows, path))
    for name, digest in CARRIED.items():
        baseline, path = BASE / name, carried / name
        require(sha(baseline) == digest, f'{baseline}: immutable baseline changed')
        if name.endswith('powercuts.jsonl'):
            expected = powercut_records(baseline, declaration(BASE / 'factory-export/factory/machine.jsonl'))
            rows = powercut_records(path, factory)
        else:
            expected = records(baseline)
            if name in ('language.jsonl','applications.jsonl','system.jsonl','ordinary.jsonl'):
                rows, routing = adapted_rows(path, expected)
            else:
                rows = records(path)
        compare_contract(rows, expected, path)
        out['carried'][name] = info(path, rows)
        if name in ('language.jsonl','applications.jsonl','system.jsonl','ordinary.jsonl'):
            out['carried'][name]['shell_routing'] = routing
        failures.extend(false_observations(rows, path))
    for name in ('shell-verify.log','gate-verify.log','tools-verify.log','supplement/before-reboot-verify.jsonl','supplement/after-reboot-verify.jsonl'):
        out['readback'].append(verify(FINAL / name, factory))
    for name in ('applications','ordinary','system','language'):
        expected = dict(factory)
        if name == 'language':
            for variant in ('pip','npm'):
                expected.update(declaration(carried / f'language-examples/channel-examples/{variant}.jsonl'))
        out['readback'].append(verify(carried / f'{name}-verify.jsonl', expected))
    out['carried_summary'] = document(carried / 'summary.json')
    out['carried_regression_summary'] = document(carried / 'regressions/summary.json')
    for name in ('carried_summary','carried_regression_summary'):
        controller(out[name], name)
    suites = out['carried_summary'].get('suites', {})
    require(set(suites) == {'applications','language','ordinary','system','regressions'}, 'carried controller suite set differs')
    for name, entry in suites.items():
        require(entry.get('tested') is True, f'{name}: not tested')
        for key in (('controller_exit',) if name == 'regressions' else ('suite_exit','verify_exit','metadata_exit','example_export_exit')):
            require(type(entry.get(key)) is int and entry[key] == 0, f'{name}: missing/failed {key}')
    # No carried false assertion is excused by a successful controller.
    out['carried_false_observations_with_successful_controller'] = [f for f in failures if f['file'].startswith('final-2/carried-suite/')]
    baseline = ROOT / 'raw/round-0/round-4/combined/events.jsonl'
    require(sha(baseline) == COMBINED_EVENTS_SHA, 'combined baseline changed')
    rows = records(combined / 'events.jsonl')
    compare_contract(rows, records(baseline), combined / 'events.jsonl')
    out['combined_assertions'] = info(combined / 'events.jsonl', rows)
    failures.extend(false_observations(rows, combined / 'events.jsonl'))
    out['combined'] = document(combined / 'summary.json')
    controller(out['combined'], 'combined')
    require({k:v for k,v in rows[-1].items() if k not in ('phase','utc')} == out['combined'], 'combined event/file summary differs')
    require(out['combined'].get('declaration_rows') == len(combined_decl), 'combined declaration count differs')
    require(out['combined'].get('snapshot_sides') == ['a','b'] and set(out['combined'].get('results',{})) == {'a','b'}, 'combined sides missing')
    for side in ('a','b'):
        result = out['combined']['results'][side]
        require(result.get('snapshot_complete') is True and result.get('snapshot_exit') == 0, 'combined snapshot incomplete')
        for suffix in ('verify.jsonl','reboot-verify.jsonl'):
            out['readback'].append(verify(combined / f'{side}-{suffix}', combined_decl))
        for suffix, ident in [('exact.jsonl','COMBINED-EXACT-DECLARATION'),('reboot-exact.jsonl','COMBINED-EXACT-DECLARATION'),('schedule.jsonl','COMBINED-SCHEDULE')]:
            path = combined / f'{side}-{suffix}'
            values = records(path)
            require(len(values) == 1 and values[0].get('id') == ident and type(values[0].get('passed')) is bool, f'{path}: missing/duplicate assertion')
            if 'files_sha256' in values[0]:
                hashes = values[0]['files_sha256']
                actual = {'machine.jsonl':sha(combined_path)}
                require(hashes == actual, f'{path}: exact declaration hashes differ')
            failures.extend(false_observations(values, path))
    path = combined / 'stand-compare.jsonl'
    failures.extend(false_observations(comparisons(path, combined_decl), path))
    for name, decl in [('independent-stand-compare.jsonl','peer-a/dev-add/machine.jsonl'),('original/D10-compare.jsonl','original/peer-a/dev-add/machine.jsonl')]:
        path = carried / 'regressions' / name
        failures.extend(false_observations(comparisons(path, declaration(carried / 'regressions' / decl)), path))
    failures.extend(ancillary(carried, factory))
    out['supplement'] = document(FINAL / 'supplement/summary.json')
    controller(out['supplement'], 'supplement', 'controller_exit')
    out['supplement_reboot'] = document(FINAL / 'supplement/reboot.json')
    require(out['supplement_reboot'].get('last_success_bytes_equal') is True, 'supplement report changed after reboot')
    for before, after in [('before-reboot-verify.jsonl','after-reboot-verify.jsonl'),('before-report.json','after-report.json')]:
        require((FINAL/'supplement'/before).read_bytes() == (FINAL/'supplement'/after).read_bytes(), f'supplement {before}/{after} bytes differ')
    out['earlier_final_1_marker_audit'] = document(RAW / 'supplement-marker-audit.json')
    out['all_false_observations'] = failures
    out['controller_assertion_consistency'] = {
        'carried': not any(f['file'].startswith('final-2/carried-suite/') for f in failures),
        'combined': not any(f['file'].startswith('final-2/combined/') for f in failures),
    }
    for name, path, declared in [('factory',factory_path,factory),('combined',combined_path,combined_decl)]:
        out[name+'_declaration'] = {'rows':len(declared),'sha256':sha(path),'inline_file_requirements':sum(len(r.get('files',[])) for r in records(path)),
                                  'base_manifest_file_requirements':len(json_value(path.parent/'base-files.json', list)) if (path.parent/'base-files.json').is_file() else 0}
    if not check_only:
        temporary = RAW / 'metrics.json.tmp'
        temporary.write_text(json.dumps(out, indent=2, sort_keys=True)+'\n')
        temporary.replace(RAW / 'metrics.json')
    print(json.dumps({'validated':True,'written':not check_only,'all_false_observations':len(failures),'new':out['new'],'carried':out['carried']},sort_keys=True))
    return out


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check-only', action='store_true', help='Validate without writing metrics.json')
    args = parser.parse_args()
    try:
        main(args.check_only)
    except (EvidenceError, OSError, UnicodeError) as exc:
        raise SystemExit(f'evidence validation failed: {exc}')

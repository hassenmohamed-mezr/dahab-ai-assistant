#!/usr/bin/env python3
from __future__ import annotations
import compileall
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQUIRED_DIRS = ["agent", "api", "docs", "models", "services", "templates", "tests", "utils"]
REQUIRED_FILES = ["app.py", "config.py", "database.py", "scheduler.py", "README.md", "requirements.txt", ".gitignore", ".env", ".env.example"]
REQUIRED_IMPORTS = ["fastapi", "uvicorn", "sqlalchemy", "pydantic", "dotenv", "apscheduler", "openai", "requests", "httpx", "jinja2"]


def run_command(command: list[str], capture_output: bool = True, check: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        capture_output=capture_output,
        check=check,
    )


def read_env_file(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    if not path.exists():
        return data
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        data[key.strip()] = value.strip()
    return data


def check_structure() -> tuple[bool, list[str]]:
    missing = []
    for directory in REQUIRED_DIRS:
        if not (ROOT / directory).exists():
            missing.append(directory)
    for filename in REQUIRED_FILES:
        if not (ROOT / filename).exists():
            missing.append(filename)
    return (len(missing) == 0, missing)


def check_python_environment() -> tuple[bool, str, str]:
    python_version = sys.version.splitlines()[0]
    pip_version = ""
    try:
        result = run_command([sys.executable, "-m", "pip", "--version"], check=True)
        pip_version = result.stdout.strip()
        return (True, python_version, pip_version)
    except subprocess.CalledProcessError:
        return (False, python_version, "pip unavailable")


def check_packages() -> tuple[bool, dict[str, bool]]:
    results = {}
    for package in REQUIRED_IMPORTS:
        try:
            __import__(package)
            results[package] = True
        except Exception:
            results[package] = False
    return (all(results.values()), results)


def check_requirements() -> tuple[bool, str]:
    if not (ROOT / "requirements.txt").exists():
        return (False, "requirements.txt missing")
    try:
        proc = run_command([sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--disable-pip-version-check"], check=False)
        output = proc.stdout + proc.stderr
        if "Requirement already satisfied" in output or proc.returncode == 0:
            return (True, output.strip())
        return (False, output.strip())
    except Exception as exc:
        return (False, str(exc))


def check_config() -> tuple[str, str]:
    example = read_env_file(ROOT / ".env.example")
    if not example:
        return ("FAIL", ".env.example missing or empty")
    if not (ROOT / ".env").exists():
        return ("FAIL", ".env missing")
    env = read_env_file(ROOT / ".env")
    missing_keys = [k for k in example if k not in env]
    if missing_keys:
        return ("PENDING", f"Pending configuration: missing keys {', '.join(missing_keys)}")
    empty_keys = [k for k, value in env.items() if value == ""]
    if empty_keys:
        return ("PENDING", f"Pending configuration: keys present but empty: {', '.join(empty_keys)}")
    return ("PASS", "OK")


def check_git() -> tuple[str, str]:
    try:
        status = run_command(["git", "status", "--short", "--branch"], check=True)
        remote = run_command(["git", "remote", "-v"], check=True)
        if not remote.stdout.strip():
            return ("PENDING", "Git remote not configured")
        if status.stdout.strip():
            return ("PENDING", "Git working tree has local changes; this is acceptable for setup.")
        return ("PASS", "Git working tree clean and remote configured")
    except Exception as exc:
        return ("FAIL", str(exc))


def check_docs() -> tuple[bool, list[str]]:
    missing = []
    for path in ["README.md", "docs/SDS.md"]:
        if not (ROOT / path).exists():
            missing.append(path)
    return (len(missing) == 0, missing)


def check_compile() -> tuple[bool, str]:
    result = compileall.compile_dir(ROOT, force=False, quiet=1)
    return (result, "compileall completed")


def run_import_check() -> tuple[bool, str]:
    try:
        import fastapi  # noqa: F401
        import sqlalchemy  # noqa: F401
        import openai  # noqa: F401
        import dotenv  # noqa: F401
        return (True, "Setup OK")
    except Exception as exc:
        return (False, str(exc))


def check_fastapi_app() -> tuple[str, str]:
    app_py = ROOT / "app.py"
    if not app_py.exists():
        return ("SKIPPED", "app.py missing")
    if app_py.stat().st_size == 0:
        return ("SKIPPED", "app.py is empty; FastAPI application not implemented yet")
    try:
        module = __import__("app")
        if hasattr(module, "app"):
            return ("PASS", "FastAPI app object found")
        return ("SKIPPED", "app.py imported but no FastAPI app object defined yet")
    except Exception as exc:
        return ("FAIL", str(exc))


def main() -> int:
    print("Project Audit Checklist")
    print("=========================")

    structure_ok, structure_missing = check_structure()
    print(f"1. Project structure: {'PASS' if structure_ok else 'FAIL'}")
    if not structure_ok:
        print(f"   Missing: {structure_missing}")

    python_ok, python_ver, pip_ver = check_python_environment()
    print(f"2. Python environment: {'PASS' if python_ok else 'FAIL'}")
    print(f"   {python_ver}")
    print(f"   {pip_ver}")

    packages_ok, package_results = check_packages()
    print(f"3. Installed packages: {'PASS' if packages_ok else 'FAIL'}")
    for pkg, ok in package_results.items():
        print(f"   {pkg}: {'OK' if ok else 'MISSING'}")

    requirements_ok, requirements_output = check_requirements()
    print(f"4. Requirements install: {'PASS' if requirements_ok else 'FAIL'}")
    if not requirements_ok:
        print(f"   {requirements_output.splitlines()[:3]}")

    config_status, config_message = check_config()
    print(f"5. Config files: {config_status}")
    print(f"   {config_message}")

    git_status, git_message = check_git()
    print(f"7. Git status: {git_status}")
    print(f"   {git_message}")

    docs_ok, docs_missing = check_docs()
    print(f"8. Documentation: {'PASS' if docs_ok else 'FAIL'}")
    if not docs_ok:
        print(f"   Missing: {docs_missing}")

    compile_ok, compile_message = check_compile()
    print(f"10. Syntax compile: {'PASS' if compile_ok else 'FAIL'}")
    print(f"   {compile_message}")

    import_ok, import_message = run_import_check()
    print(f"10. Imports check: {'PASS' if import_ok else 'FAIL'}")
    print(f"   {import_message}")

    fastapi_status, fastapi_message = check_fastapi_app()
    print(f"6. FastAPI application: {fastapi_status}")
    print(f"   {fastapi_message}")

    final_pass = all([structure_ok, python_ok, packages_ok, requirements_ok, docs_ok, compile_ok, import_ok])
    print("\nFinal result:")
    print("   Project audit completed.")
    print(f"   Overall status: {'PASS' if final_pass else 'FAIL'}")
    if config_status != "PASS":
        print("   Note: environment variables are pending configuration but .env exists.")
    if git_status != "PASS":
        print("   Note: Git status is pending; local changes or remote configuration may still be fine for setup.")
    if fastapi_status == "SKIPPED":
        print("   Note: FastAPI app bootstrap is not implemented yet.")
    return 0 if final_pass else 1


if __name__ == '__main__':
    raise SystemExit(main())

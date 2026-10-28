# DevOps CI/CD Pipeline & UAT Dry Run Final Report

## Target Environment
- **Host Machine:** Windows 11 with WSL2 (Windows Subsystem for Linux 2)
- **Linux Distribution:** Ubuntu 26.04.1 LTS (Codename: resolute, Kernel: 6.6.87.2-microsoft-standard-WSL2)
- **Repository URL:** https://github.com/ravipatil-9225/devops-uat-hello.git
- **POE Delivery Mirror:** https://github.com/ravipatil-9225/MLDEVOPS_INTERNAL_POE.git

---

## 1. Installation Summary Table

| Tool Name | Version | Commands Used | Installation Status | Notes, Error and Fix |
|:---|:---|:---|:---|:---|
| **Git** | `2.53.0` | `sudo apt install -y git` / pre-installed | **Successful** | Verified with `git --version`. Configured Git Credential Manager symlink to handle Windows/WSL authentication. |
| **Python 3** | `3.14.4` (host) / `3.12.16` (container) | `sudo apt install -y python3-venv python3-pip` | **Successful** | Pre-installed and upgraded with `python3-venv` and `python3-pip`. Verified with `python3 --version`. |
| **VS Code** | `1.141.0` | `code ~/devops-uat-project` | **Successful** | Pre-installed Windows binary integrated via WSL bridge. Verified with `code --version`. |
| **Java 17** | `17.0.20.1` | `sudo apt update && sudo apt install -y openjdk-17-jdk` | **Successful** | Installed cleanly. Verified with `java -version`. Note: Required upgrade for Jenkins 2.580.2. |
| **Java 21** | `21.0.12.1` | `sudo apt install -y openjdk-21-jdk` | **Successful** | Installed as resolution to Jenkins requirement (`Supported Java versions are: [21, 25]`). Configured as active default Java. |
| **Jenkins** | `2.580.2` | Official Jenkins apt repository & `sudo apt install -y jenkins` | **Failed initially, then Successful** | **Error 1:** `NO_PUBKEY 7198F4B714ABFC68` on `jenkins.io-2023.key`. **Fix:** Updated key URL to `https://pkg.jenkins.io/debian-stable/jenkins.io-2026.key`.<br>**Error 2:** Startup failed on Java 17. **Fix:** Installed OpenJDK 21. Configured setup wizard via Groovy init script with admin credentials and installed plugins (`git`, `workflow-aggregator`, `github`, `junit`, `ws-cleanup`). |
| **Docker Engine** | `29.9.2` | `sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin` | **Successful** | Official Docker apt repo configured. Added `ravip` and `jenkins` users to `docker` group. Restarted Jenkins. Verified with `docker run --rm hello-world`. |
| **python:3.12-slim** | `3.12-slim` (sha256:aa943ce41142) | `docker pull python:3.12-slim` | **Successful** | Base image pulled and verified. Used as runtime base for `hello-uat` container images. |
| **pytest** | `9.2.0` | `.venv/bin/pip install -r requirements.txt` / Docker build | **Successful** | Installed in virtualenv and container. Configured via `pytest.ini`. Verified with `pytest --collect-only -q` (1 item) and `pytest -v` (1 passed). |
| **Evidently** | `0.7.23` | `.venv/bin/pip install -r requirements.txt` / Docker build | **Failed initially, then Successful** | **Error 1:** `ImportError: cannot import name 'infer_dtype_from_object' from 'pandas.core.dtypes.common'` due to breaking change in Pandas 3.0+. **Fix:** Added dynamic compatibility shim mapping `infer_dtype_from_object` to `infer_dtype`.<br>**Error 2:** `ModuleNotFoundError: No module named 'evidently.report'` due to Evidently 0.7 refactoring. **Fix:** Added fallback import to `evidently.legacy.report` and `evidently.legacy.metric_preset`. |
| **GitHub CLI (gh)** | `2.46.0` | `sudo apt install -y gh` | **Successful** | Installed via apt package repository for GitHub CLI tooling. |

---

## 2. Pipeline Run Results

All builds executed against job `hello-uat-pipeline` pointing to branch `*/main` on `devops-uat-hello`.

| Build # | Trigger / Context | Overall Result | Total Duration | Stages and Status |
|:---|:---|:---:|:---:|:---|
| **#1** | Initial pipeline verification after commit/push | **SUCCESS** | 17.99s | ? **Checkout:** SUCCESS (SCM git clone from GitHub)<br>? **Build Image:** SUCCESS (`docker build -t hello-uat:1 .`)<br>? **Test:** SUCCESS (`pytest --junitxml=reports/report.xml` - 1 passed in 0.06s; JUnit results recorded)<br>? **Run App:** SUCCESS (`Hello, World!` output)<br>? **Monitor:** SUCCESS (Evidently data drift HTML report generated)<br>? **Archive:** SUCCESS (Archived `reports/evidently_report.html`)<br>? **Post:** SUCCESS (`cleanWs()` workspace wipe) |
| **#2** | UAT Dry Run (Fresh clone in `~/uat-dryrun/devops-uat-hello`) | **SUCCESS** | 10.64s | ? **Checkout:** SUCCESS<br>? **Build Image:** SUCCESS (`hello-uat:2`)<br>? **Test:** SUCCESS (1 passed; JUnit published)<br>? **Run App:** SUCCESS (`Hello, World!`)<br>? **Monitor:** SUCCESS (Evidently report generated)<br>? **Archive:** SUCCESS (Report artifact archived)<br>? **Post:** SUCCESS (`cleanWs()`) |
| **#3** | UAT Repeatability Dry Run | **SUCCESS** | 14.33s | ? **Checkout:** SUCCESS<br>? **Build Image:** SUCCESS (`hello-uat:3`)<br>? **Test:** SUCCESS (1 passed; JUnit published)<br>? **Run App:** SUCCESS (`Hello, World!`)<br>? **Monitor:** SUCCESS (Evidently report generated)<br>? **Archive:** SUCCESS (Report artifact archived)<br>? **Post:** SUCCESS (`cleanWs()`) |

---

## 3. Team Contributions

| Developer | Role | Owned Phases & Responsibilities |
|:---|:---|:---|
| **Developer1** (`dev1@example.com`) | Application & Test Engineer | ? **Phase 2:** Authoring core application (`hello.py`), test suite (`test_hello.py`), and base dependencies (`requirements.txt`).<br>? **Phase 3:** Virtual environment creation (`.venv`) and local test verification (`pytest`).<br>? **Phase 4:** Authoring Commit 2 (`feat: add hello application, tests, and requirements`).<br>? **Phase 11:** Test configuration authoring (`pytest.ini`), test collection verification, and test execution validation. |
| **Developer2** (`dev2@example.com`) | DevOps & Infrastructure Engineer | ? **Phase 0:** Environment provisioning on Windows WSL2 (Ubuntu 26.04), prerequisite verification (`git`, `python3`, `code`, `curl`), and workspace setup.<br>? **Phase 1:** Team structure and governance specification (`TEAM.md`).<br>? **Phase 3:** IDE workspace setup (`.vscode/settings.json`) and ignore rules (`.gitignore`).<br>? **Phase 4:** Git repository initialization (`git init -b main`), GitHub repository provisioning (`devops-uat-hello`), Commit 1 authoring, remote configuration, and push.<br>? **Phase 5:** Java 17 and Java 21 runtime installation, official Jenkins APT repository and GPG key installation, Jenkins systemd service enablement, and automated setup wizard orchestration via Groovy.<br>? **Phase 6 & 7:** Pipeline job creation (`hello-uat-pipeline`), SCM Git integration, and initial pipeline execution.<br>? **Phase 8:** Docker Engine CE installation, permission management (`docker` group for user and Jenkins), and verification with `hello-world`.<br>? **Phase 9:** Pulling `python:3.12-slim`, Dockerfile authoring, and containerized greeting verification.<br>? **Phase 10:** Multi-stage Declarative CI/CD pipeline definition in `Jenkinsfile`.<br>? **Phase 12:** Evidently monitoring integration (`monitor.py`), DataDriftPreset reporting, and backward-compatible shim development.<br>? **Phase 13:** Fresh clone orchestration in `~/uat-dryrun` and UAT repeatability verification across consecutive pipeline builds.<br>? **Phase 14:** Comprehensive engineering report (`REPORT.md`) and project distribution. |

---

## 4. Known Issues and Next Steps

### Known Issues Resolved During Setup
1. **Jenkins Repository GPG Signing Key Deprecation:**
   - *Issue:* Official Jenkins repository using `jenkins.io-2023.key` expired/mismatched with package signature `NO_PUBKEY 7198F4B714ABFC68`.
   - *Fix:* Configured current key URL `https://pkg.jenkins.io/debian-stable/jenkins.io-2026.key`.
2. **Jenkins Java Runtime Minimum Version Requirement:**
   - *Issue:* Jenkins 2.580.2 requires Java 21 or 25; Java 17 caused daemon startup abort.
   - *Fix:* Installed `openjdk-21-jdk` and configured it as system default.
3. **Evidently / Pandas 3.0 Compatibility:**
   - *Issue:* Pandas 3.0+ removed `infer_dtype_from_object`, breaking Evidently 0.7 import. Furthermore, Evidently 0.7 restructured package namespaces (`evidently.report` moved to `evidently.legacy.report`).
   - *Fix:* Added runtime shim in `monitor.py` that maps `infer_dtype_from_object` to `pandas.api.types.infer_dtype` and added multi-version try/except import fallbacks.

### Recommended Next Steps
1. **GitHub Webhooks Integration:** Configure Jenkins webhook endpoint (`http://<host>:8080/github-webhook/`) with a public tunnel (such as ngrok or Cloudflare Tunnel) to trigger builds automatically on git push events instead of polling/manual triggers.
2. **Container Registry Publishing:** Add an optional pipeline stage to push version-tagged images (`hello-uat:${BUILD_NUMBER}`) to Docker Hub or GitHub Packages (GHCR) upon successful UAT validation.
3. **Automated Drift Alerting:** Extend `monitor.py` to evaluate drift metric thresholds and emit non-zero exit codes or send Slack/email alerts when feature drift is detected between inference and training datasets.
4. **Staging to Production CD Promotion:** Add a manual approval gate and deployment stage targeting Kubernetes (Minikube / k3s) or AWS ECS for automated continuous deployment.

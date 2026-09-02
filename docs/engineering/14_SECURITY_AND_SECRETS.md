# 14_SECURITY_AND_SECRETS.md



## Status



Version: 0.1

Document type: Engineering specification

Owner: Human project team

Depends on: `AGENTS.md`, `08_SYSTEM_ARCHITECTURE.md`

Purpose: Define minimum security requirements for a public-repository, local-first system that uses external APIs, Telegram, web sources, and a renderer.



---



## 1. Threat Model



Version 1 should assume:



- the GitHub repository is public;

- source webpages are untrusted input;

- model output is untrusted input;

- Telegram is an external control channel;

- API credentials have monetary value;

- downloaded files may be malformed;

- prompt injection may appear inside webpages/documents;

- generated HTML/text can contain unsafe characters;

- coding agents have powerful local computer access during development.



Security should remain simple and explicit.



---



## 2. Public Repository Rule



Never commit operational secrets or private runtime data.



The public repository may contain:



- source code;

- canonical documentation;

- prompt templates;

- schemas;

- sanitized fixtures;

- approved public brand assets.



It should not contain:



- `.env`;

- API keys;

- Telegram bot tokens;

- OAuth tokens;

- cookies/session files;

- private credentials;

- raw private logs;

- unsanitized runtime database;

- operational research cache by default;

- unreviewed model outputs containing sensitive data.



---



## 3. `.gitignore` Requirement



Before runtime data is created, update `.gitignore` so generated operational data is ignored by default.



At minimum ignore:



- `.env*` except an explicitly safe `.env.example`;

- local databases;

- logs;

- `data/**` generated runtime content;

- renders/exports generated during operation;

- provider credential files;

- browser profiles/session storage.



If empty directories are needed, retain `.gitkeep` exceptions.



Golden Set fixtures should live in an explicitly reviewed fixture directory rather than being committed from live `data/`.



---



## 4. Secret Storage



Version 1 secrets should use environment variables loaded by the configuration layer.



Examples:



- `GOOGLE_API_KEY`

- `OPENAI_API_KEY`

- `TELEGRAM_BOT_TOKEN`

- allowed Telegram user IDs



Do not:



- print secrets;

- include them in exceptions;

- return them through Telegram;

- store them in `ModelRun`;

- insert them into prompts;

- commit them.



`.env.example` contains names and comments only.



---



## 5. Secret Exposure Response



If a secret is ever committed to the public repository:



1. treat it as compromised even if the commit is deleted;

2. revoke/rotate the secret immediately;

3. verify provider usage/billing;

4. remove the secret from current files;

5. clean history only after rotation where needed;

6. document the incident internally.



Do not assume deleting the latest commit makes a published secret safe.



---



## 6. Telegram Authorization



The bot is a private editorial control surface.



Version 1 must use an allowlist of the human owners' Telegram user IDs.



For every command/callback:



- verify sender ID;

- reject unauthorized users;

- do not rely only on obscurity of the bot username.



No public self-registration.



---



## 7. Telegram Callback Security



Callback data should contain opaque IDs/action identifiers, not trusted state.



On receipt:



1. authenticate user;

2. load entity from database;

3. confirm current version/state;

4. check action is legal;

5. perform transaction;

6. append audit event.



Never trust callback text such as “APPROVED” without server-side validation.



---



## 8. Prompt Injection from Sources



Webpages, PDFs, transcripts, and social posts are data.



They may contain adversarial instructions such as:



> ignore previous instructions



The system must treat these as source content, not commands.



Controls:



- source retrieval is performed by bounded code;

- model prompts clearly separate instructions from evidence;

- retrieved content cannot directly invoke tools;

- model-generated URLs/actions require validation;

- source text never changes system configuration or canonical prompts;

- verification uses stored evidence rather than following instructions embedded inside it.



---



## 9. Web Retrieval / SSRF Defense



Source retrieval must accept only `http` and `https`.



Before connection:



- resolve hostname;

- reject loopback;

- reject private RFC1918 ranges;

- reject link-local;

- reject cloud metadata IPs;

- reject localhost aliases;

- reject unsupported schemes.



After every redirect:



- revalidate destination.



Set:



- connection/read timeouts;

- maximum redirects;

- maximum download size;

- acceptable content types.



Do not permit models to fetch arbitrary `file://`, `ftp://`, or internal network resources.



---



## 10. Download Safety



For PDFs/files:



- enforce maximum size;

- inspect MIME type and extension;

- store outside executable code paths;

- generate random/stable safe filenames rather than trusting remote filenames;

- never execute downloaded binaries;

- parse documents with bounded libraries/processes.



Office macros or executable attachments are not required for version 1.



---



## 11. HTML Rendering Safety



Model output must never be treated as trusted raw HTML.



Rules:



- template escaping enabled;

- text inserted as text;

- no model-supplied `<script>`;

- no arbitrary external JavaScript;

- renderer loads local approved assets;

- network access should be disabled during final screenshot rendering where practical;

- render process uses fixed local templates.



This prevents the post renderer becoming a browser-execution path for source/model content.



---



## 12. Model Output Validation



All structured model output:



- parsed into explicit schema;

- rejected if invalid;

- length-limited where appropriate;

- sanitized before logs/UI/rendering.



Model output never becomes SQL, shell commands, paths, or executable code directly.



---



## 13. SQL Safety



Use SQLAlchemy parameterized queries.



Do not interpolate model/user text into raw SQL.



Schema migrations are code-reviewed.



Operational model outputs have no database credentials and cannot run arbitrary SQL.



---



## 14. Filesystem Safety



Runtime services should use configured storage roots.



Model-generated filenames are prohibited.



Use application-generated IDs.



Normalize/resolve paths and ensure target remains under the allowed root before reading/writing.



Do not allow Telegram text or model output to provide arbitrary local paths.



---



## 15. Coding-Agent Safety



Antigravity/Codex are development tools, not runtime services.



They must follow `AGENTS.md`.



Key rules:



- work inside repository;

- no unrelated personal-file inspection;

- no sudo without human approval;

- no automatic push;

- no external publishing;

- do not display secrets;

- create Git checkpoints before material changes.



---



## 16. Logging and Redaction



Logs should contain useful identifiers, not credentials.



Redact:



- authorization headers;

- API keys;

- bot tokens;

- cookies;

- session IDs where sensitive.



Do not dump complete request objects blindly.



Source excerpts and model outputs should be stored in controlled artifact files when needed rather than flooding logs.



---



## 17. Public Logging / Error Messages



Telegram error messages should be concise.



Do not send:



- stack traces with secrets;

- environment dumps;

- full request headers;

- local filesystem paths unnecessarily.



Detailed errors remain in local logs.



---



## 18. Dependency Security



Use maintained dependencies.



During Milestone 1:



- record dependencies in `pyproject.toml`;

- pin compatible versions;

- use a reproducible environment;

- run vulnerability/dependency review periodically.



Avoid adding packages for trivial functions that the standard library handles safely.



---



## 19. GitHub Security



Because the repository is public:



- enable available secret scanning/security alerts;

- review dependency alerts;

- do not upload runtime databases as bug reports;

- sanitize screenshots/logs before issues/commits.



A CI secret scanner may be added before real credentials are introduced.



---



## 20. API Key Permissions



Use separate provider keys for the project where practical.



Apply provider budget/quota limits when available.



Do not reuse high-privilege personal/cloud credentials if a narrower project key works.



Keys should be rotatable without code changes.



---



## 21. Provider Data Minimization



Send providers only the data required for the task.



Avoid attaching:



- unrelated source archives;

- private local files;

- secrets;

- full databases.



Prompts should use source IDs and relevant excerpts.



---



## 22. Human Review Security



Final preview should display enough provenance for an editor to detect obvious corruption:



- topic;

- render version;

- key claims;

- principal sources;

- risk level.



A visually polished render must not hide a failed or missing QA state.



---



## 23. Backups



Before VPS production:



- define a simple database backup;

- back up canonical approved assets;

- verify restore.



Backups containing credentials or private runtime state must not be committed to GitHub.



---



## 24. Security Non-Goals for Version 1



Do not overengineer:



- enterprise IAM;

- Kubernetes secrets;

- HSMs;

- public multi-user authentication;

- complex zero-trust networking.



The main version 1 security priorities are:



- secrets;

- Telegram allowlisting;

- safe source retrieval;

- prompt-injection isolation;

- filesystem boundaries;

- safe rendering;

- public-repo hygiene.



---



## 25. Security Test Requirements



Before real API keys are introduced, tests should cover:



- unauthorized Telegram user rejected;

- duplicate callback safe;

- private/localhost URL blocked;

- redirect to private address blocked;

- unsupported URI scheme blocked;

- oversized download rejected;

- path traversal rejected;

- model raw HTML escaped;

- secret-looking values absent from normal logs.



---



## 26. Golden Rule



**Everything from the internet or a model is untrusted data until validated; everything secret stays outside Git.**

# claude-starter-kit

AI Weekend 201 · Day 2 · Claude Code hands-on starter.
[Türkçe](#türkçe) · [English](#english)

```bash
git clone https://github.com/AI-Weekend/claude-starter-kit && cd claude-starter-kit && claude
```

```
claude-starter-kit/
├── CLAUDE.md                     run · test · don't-touch
├── .claude/
│   ├── skills/house-review/      review skill (loads on its own)
│   ├── skills/changelog/         /changelog <n> command
│   ├── hooks/protect-secrets.sh  PreToolUse: blocks .env / secrets
│   ├── hooks/verify-on-stop.sh   Stop: runs the tests if .py files changed
│   ├── agents/storage-scout.md   read-only subagent (haiku)
│   └── settings.json             hook wiring
├── .mcp.json                     filesystem → ~/notes (github: Session 04)
├── .env.example                  GITHUB_PAT placeholder — copy to .env
├── app/                          expense-api (FastAPI): main.py, models.py
├── tests/                        pytest
└── sample-notes/recipes/         14 recipes for the MCP filesystem demo
```

---

## Türkçe

**Bu nedir?** Day 2 oturumlarında (02–05) kullandığımız örnek proje. İçinde küçük bir FastAPI
uygulaması (**expense-api**) ve hazır kurulmuş bir Claude Code kiti var: `CLAUDE.md`, iki skill,
iki hook, bir subagent ve `.mcp.json`. Hiçbir şeyi sıfırdan yazmıyorsunuz.

Uygulamada **bilerek bırakılmış** kusurlar var. Bunlar alıştırmaların konusu:

- `/health` endpoint'i yok (`app/main.py` içindeki TODO).
- `/expenses/total` son harcamayı atlıyor (FIXME). `test_total_sums_all_expenses` bu yüzden
  kırmızı. `uv run pytest -q` → `1 failed, 5 passed`.
- Storage fonksiyonları `app/main.py` içinde. `app/storage.py`'ye taşımak refactor alıştırması.

### Gereksinimler

| Araç | Neden | Kurulum |
| --- | --- | --- |
| Claude Code | Ana araç. Pro, Max, Team, Enterprise veya Console hesabı gerekir. | `curl -fsSL https://claude.ai/install.sh \| bash` · [docs](https://code.claude.com/docs) |
| uv | Python 3.12 ve bağımlılıklar | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| jq | Hook script'leri JSON girdiyi jq ile okur | `brew install jq` · `sudo apt install jq` |
| Node.js 18+ | MCP sunucuları `npx` ile başlar | [nodejs.org](https://nodejs.org) |
| git, gh (ops.) | Session 04–05'te PR | `brew install gh` · `gh auth login` |

Windows'ta WSL kullanın.

### Kurulum (bir kere)

```bash
git clone https://github.com/AI-Weekend/claude-starter-kit && cd claude-starter-kit
uv run pytest -q                                     # 1 failed, 5 passed — beklenen durum
mkdir -p ~/notes && cp -R sample-notes/recipes ~/notes/   # filesystem MCP ~/notes klasörünü okur
cp .env.example .env                                 # Session 04'te GITHUB_PAT'i siz doldurun
claude                                               # klasöre güvenin, filesystem sunucusunu onaylayın
```

Her oturuma temiz bir dalla başlayın. Böylece bir oturumdaki düzeltme diğerinin alıştırmasını bozmaz:
`git switch main && git switch -c session-03`. Önceki işinizi önce commit edin ya da silin.

### Oturumlar

**Session 02 — Claude Code'a giriş**
1. `> explain this project in 5 bullets`
2. `> add a /health endpoint and a test` → Claude okur, düzenler, `uv run pytest -q` çalıştırır.
3. Shift+Tab ile izin modlarını gezin. `/memory` ile `CLAUDE.md`'yi açın. `Esc Esc` veya `/rewind` deneyin.

Not: Stop hook'u `.py` dosyaları değiştiğinde testleri çalıştırır ve önceden kırık olan
`test_total_sums_all_expenses` testini Claude'a geri yollar. Bu Session 04'ün hatası.
"Leave that test for now" deyin ya da Esc'ye basın.

**Session 03 — Skill'ler, komutlar, hook'lar**
1. `/changelog 20` → git log'dan sürüm notu.
2. Küçük bir değişiklik yapıp `git add` ile stage edin, sonra `> review my staged changes`.
   `house-review` skill'i kendiliğinden yüklenir.
3. `> test the hook: add a line to .env` → `protect-secrets.sh` engeller (exit 2). Bash yolu da
   engellenir. Sadece "add a line to .env" derseniz Claude `CLAUDE.md` yüzünden baştan reddedebilir.
4. `.claude/skills/house-review/SKILL.md` dosyasına bir kural ekleyin. `/hooks` ile hook'lara bakın.

**Session 04 — MCP**
1. `/mcp` → `filesystem` bağlı olmalı.
2. `> plan 5 dinners from ~/notes/recipes and write a shopping list`
3. GitHub ve Playwright sunucularını ekleyin. Token `.mcp.json`'a yazılmaz; `${GITHUB_PAT}` olarak kalır.
   ```bash
   set -a; source .env; set +a      # GITHUB_PAT'i shell'e aktarır
   claude mcp add --scope project --transport http github https://api.githubcopilot.com/mcp/ \
     --header 'Authorization: Bearer ${GITHUB_PAT}'
   claude mcp add --scope project playwright -- npx -y @playwright/mcp@latest
   ```
4. Kendi kopyanızda bir PR açın ([PR kurulumu](#pr-kurulumu--pr-setup)), sonra:
   `> Reproduce the failing test in expense-api, fix the /expenses/total bug in app/main.py, then comment the fix on the PR.`
   Beklenen iz: github → Read / Edit / Bash → github.

**Session 05 — Agent'lar iş başında**
Plan modunda başlayın (`claude --permission-mode plan` ya da Shift+Tab) ve birini seçin:
- **Tur:** `> use the storage-scout subagent to summarize how expenses are stored`. Sonra README ile
  `app/`'i okuyup TODO/FIXME'leri listeletin.
- **/health → PR:** endpoint + test + `gh pr create`.
- **Bug hunt:** `uv run pytest -k test_total_sums_all_expenses` ile başlayın. `git log app/main.py`
  ile hatayı getiren commit'i bulun. Önce hipotezi yazdırın, sonra yamalayın.
- **Refactor:** storage'ı `app/main.py`'den `app/storage.py`'ye taşıyın. Sırayla: fonksiyonlar,
  çağrı yerleri, testler.

---

## English

**What is this?** The sample project for Day 2 sessions 02–05. It holds a small FastAPI app
(**expense-api**) and a pre-wired Claude Code kit: `CLAUDE.md`, two skills, two hooks, a
subagent and `.mcp.json`. You don't author anything from scratch.

The app has **deliberate** warts. The exercises are about them:

- There is no `/health` endpoint (TODO in `app/main.py`).
- `/expenses/total` drops the last expense (FIXME), so `test_total_sums_all_expenses` is red.
  `uv run pytest -q` → `1 failed, 5 passed`.
- The storage functions live in `app/main.py`. Moving them to `app/storage.py` is the refactor
  exercise.

### Prerequisites

| Tool | Why | Install |
| --- | --- | --- |
| Claude Code | The agent. Needs a Pro, Max, Team, Enterprise or Console account. | `curl -fsSL https://claude.ai/install.sh \| bash` · [docs](https://code.claude.com/docs) |
| uv | Python 3.12 and dependencies | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| jq | The hook scripts parse their JSON input with jq | `brew install jq` · `sudo apt install jq` |
| Node.js 18+ | MCP servers start through `npx` | [nodejs.org](https://nodejs.org) |
| git, gh (optional) | PRs in Sessions 04–05 | `brew install gh` · `gh auth login` |

On Windows, use WSL.

### Setup (once)

```bash
git clone https://github.com/AI-Weekend/claude-starter-kit && cd claude-starter-kit
uv run pytest -q                                     # 1 failed, 5 passed — expected
mkdir -p ~/notes && cp -R sample-notes/recipes ~/notes/   # the filesystem MCP server reads ~/notes
cp .env.example .env                                 # fill in GITHUB_PAT yourself in Session 04
claude                                               # trust the folder, approve the filesystem server
```

Start each session on a fresh branch, so a fix from one session doesn't spoil the next exercise:
`git switch main && git switch -c session-03`. Commit or discard your previous work first.

### Sessions

**Session 02 — Claude Code intro**
1. `> explain this project in 5 bullets`
2. `> add a /health endpoint and a test` → Claude reads, edits and runs `uv run pytest -q`.
3. Cycle permission modes with Shift+Tab. Open `CLAUDE.md` with `/memory`. Try `Esc Esc` or `/rewind`.

Note: the Stop hook runs the tests when `.py` files changed. It sends the already-red
`test_total_sums_all_expenses` back to Claude. That's the Session 04 bug: say
"leave that test for now" or press Esc.

**Session 03 — Skills, commands, hooks**
1. `/changelog 20` → release notes from git log.
2. Make a small change, `git add` it, then `> review my staged changes`. The `house-review`
   skill loads on its own.
3. `> test the hook: add a line to .env` → `protect-secrets.sh` blocks it (exit 2). The Bash route
   is blocked too. A plain "add a line to .env" may be refused up front because of `CLAUDE.md`.
4. Add one house rule to `.claude/skills/house-review/SKILL.md`. Browse the hooks with `/hooks`.

**Session 04 — MCP**
1. `/mcp` → `filesystem` should be connected.
2. `> plan 5 dinners from ~/notes/recipes and write a shopping list`
3. Add the GitHub and Playwright servers. The token never lands in `.mcp.json`; it stays `${GITHUB_PAT}`.
   ```bash
   set -a; source .env; set +a      # export GITHUB_PAT into this shell
   claude mcp add --scope project --transport http github https://api.githubcopilot.com/mcp/ \
     --header 'Authorization: Bearer ${GITHUB_PAT}'
   claude mcp add --scope project playwright -- npx -y @playwright/mcp@latest
   ```
4. Open a PR on your own copy ([PR setup](#pr-kurulumu--pr-setup)), then:
   `> Reproduce the failing test in expense-api, fix the /expenses/total bug in app/main.py, then comment the fix on the PR.`
   Expected trace: github → Read / Edit / Bash → github.

**Session 05 — Agents on play**
Start in plan mode (`claude --permission-mode plan` or Shift+Tab) and pick one:
- **Tour:** `> use the storage-scout subagent to summarize how expenses are stored`. Then have it
  read the README and `app/` and list the TODO/FIXME warts.
- **/health → PR:** endpoint + test + `gh pr create`.
- **Bug hunt:** start with `uv run pytest -k test_total_sums_all_expenses`. Find the commit that
  broke it with `git log app/main.py`. Make it state a hypothesis before it patches.
- **Refactor:** move storage from `app/main.py` to `app/storage.py`. Batch it: functions, then call
  sites, then tests.

---

## PR kurulumu · PR setup

The GitHub server needs a repo you can write to. Push the starter to your own account and open a
PR for Claude to read and reply on:

```bash
gh repo create claude-starter-kit --private --source=. --remote=mine --push
gh repo set-default "$(gh api user -q .login)/claude-starter-kit"
git switch -c fix-total && git commit --allow-empty -m "Fix /expenses/total" && git push -u mine fix-total
gh pr create --title "Fix /expenses/total" \
  --body "test_total_sums_all_expenses fails — /expenses/total is short by one item"
```

Use a fine-grained token scoped to that repo, with read/write on Contents, Issues and Pull requests.

## Commands

```bash
uv run uvicorn app.main:app --reload   # http://127.0.0.1:8000/docs
uv run pytest -q
uv run ruff check .
```

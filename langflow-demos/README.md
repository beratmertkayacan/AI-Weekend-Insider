# AI Weekend 201 — Langflow Flows

Hands-on flows for the **AI Weekend 201** Day 1 sessions. Each session
is a [Langflow](https://www.langflow.org) flow: you import a **starter** with one critical piece
missing, follow the yellow Note on the canvas to complete it, and test it in the Playground.

Together the six sessions build one assistant, layer by layer:

> **reason → orchestrate → remember → tools → deploy → observe**


## Hızlı başlangıç (Türkçe)

1. Etkinlikten önce kur: **Langflow Desktop 1.13.0**, **Ollama** (`ollama pull llama3.2:3b`, yalnız 05 için)
   ve **Node.js**.
2. Eğitmenden `XAI_API_KEY`, `OPENAI_API_KEY` (embedding) ve `TAVILY_API_KEY` anahtarlarını al. Langflow'da *Settings > Global
   Variables* altında **Credential** türünde, tam bu adlarla ekle.
3. Bir track seç: `mutfak` (ana track), `hafta-sonu`, `finans` veya `seyahat`.
4. Oturumun starter dosyasını (`<track>/0N-….json`) Langflow'a yükle, tuvaldeki sarı Note'u oku,
   eksik parçayı tamamla ve Playground'da dene. Takılırsan bir sonraki oturumun starter'ı önceki katmanları hazır getirir.
   Hazır metinler (Prompt, router kuralları, hakem talimatı) `<track>/kopyala-yapistir.md` dosyasında.
5. Dosya seçicileri (File) içe aktarmadan sonra boş gelir: dosyaları `assets/<track>/` klasöründen
   yeniden seç.

## Before the event

Do all of this on your own machine ahead of time; the session itself assumes it is done.

| What | How |
|---|---|
| **Langflow Desktop 1.13.0** | Install that exact version. The flow JSONs were exported from it. |
| **Ollama** | Install from [ollama.com](https://ollama.com), then `ollama pull llama3.2:3b` (local chat model, used only in session 05). |
| **Node.js** | Needed for `npx`, which starts the filesystem MCP server (session 04 onward). |
| **API keys** | Get `XAI_API_KEY` (xAI, model `grok-4.3`), `OPENAI_API_KEY` (embeddings, model `text-embedding-3-small`) and `TAVILY_API_KEY` (web search) from the instructor. Keys live only in Langflow, never in a flow file. |

> **Corporate networks:** `ollama pull` can fail behind TLS inspection or a zero-trust proxy because
> the model registry redirects downloads to Cloudflare R2. If it hangs or errors, pull the model
> on another network or a phone hotspot.

### Add the keys to Langflow

*Settings > Global Variables > Add New*, type **Credential**, one variable per key, with these exact names:

- `XAI_API_KEY`
- `OPENAI_API_KEY`
- `TAVILY_API_KEY`

### Connect Ollama to Langflow (once)

*Settings > Model Providers > Ollama*, base URL `http://localhost:11434`. Session 05 needs this. If your Langflow asks for an environment-style variable instead, add a
Generic global variable `OLLAMA_BASE_URL` with the same URL.

## Pick a track

All four tracks teach the same six layers on a different everyday scenario. Pick one and stay on it;
the deck screenshots use **mutfak**.

| Track | Folder | Scenario |
|---|---|---|
| **Mutfak** (main) | `mutfak/` | A home-kitchen assistant: what to cook from what you have, shopping lists, nutrition, family allergies and house rules from a recipe book. |
| **Hafta sonu** | `hafta-sonu/` | A weekend planner for İzmir: places to go, weather, transport, and your stated preferences. |
| **Finans** | `finans/` | A personal-budget coach: reads your expenses (CSV), compares them with your targets, and suggests where to cut. |
| **Seyahat** | `seyahat/` | A trip preparer for Lisbon: day-by-day plans plus visa and document checks against a checklist PDF. |

All input data is synthetic and lives in `assets/<track>/`.

## Sessions

| Flow | Deck | Layer added | Starter's missing piece |
|---|---|---|---|
| `01-temel` | Advanced LLMs | Prompt with chain-of-thought | The Prompt component. |
| `02-akis` | Agentic Workflows | Smart Router + specialist Agents | The router's routes. |
| `03-hafiza` | Advanced RAG & Memory | Knowledge base retrieval + chat memory | The knowledge base (and its embedding model). |
| `04-araclar` | MCP & Tool Calling | Web search, calculator, filesystem MCP | The MCP Tools node. |
| `05-yayin` | Deploy the Agent | API endpoint + local Ollama model | The local model name. |
| `06-izleme` | LLMOps | LLM-as-judge + Traces | The judge prompt. |

For each session: *Upload a flow* with `<track>/0N-….json`, read the yellow Note, finish the
missing piece, then test in the Playground. Each session starts from the previous session's solution
logic, so the flows grow session by session. If you fall behind, import the next session's starter: it ships
with every earlier layer already complete.

### What to do after every import

- **File pickers are empty.** Uploaded paths are machine-specific, so every `Read File` component
  comes in empty. Re-pick the files from `assets/<track>/` (the Note names them).
- **The xAI key may look blank.** On the first open of an imported flow, Langflow 1.13 can blank the
  xAI *API Key* field. Click the globe icon on the field and pick `XAI_API_KEY` again. Opening
  *Settings > Global Variables* before the flow avoids it.
- **"Setup Provider" button.** Agent and Smart Router can show a black *Setup Provider* button even
  when a model is wired in. Ignore it; the flow runs.

### From session 03: create and fill the knowledge base

Starting at `03-hafiza`, the flow retrieves from a local knowledge base (SQLite, no server). Its
embeddings come from OpenAI, so `OPENAI_API_KEY` must be set first.
Then open *Settings > Model Providers > OpenAI* and switch on `text-embedding-3-small` under
*Embedding Models*: it is off by default, and until it is on, *Add Knowledge* shows "No models enabled".
Neither the starter nor the solution JSON carries it, so on each machine:

1. Open the **Knowledge** page (left sidebar, bottom) and choose *Add Knowledge*.
2. Name it for your track and choose **OpenAI `text-embedding-3-small`** as the embedding model (not the
   chat model). Names the flows expect:

   | Track | Knowledge base | Source file(s) |
   |---|---|---|
   | mutfak | `mutfak_tarifler` | the four recipe PDFs in `assets/mutfak/` |
   | hafta-sonu | `hafta_sonu_mekanlar` | `assets/hafta-sonu/mekanlar.pdf` |
   | finans | `finans_hedefler` | `assets/finans/notlar/butce-hedefleri.md` (the CSV is a separate input) |
   | seyahat | `seyahat_belgeler` | `assets/seyahat/vize-belge-kontrol-listesi.pdf` |

3. Back in the flow, select that knowledge base on **both** Knowledge components, pick the source
   file(s) in `Read File`, and press the play button on the **Ingest** component once.

Use the Knowledge page, not the Knowledge component's own *Create new Knowledge Base* dialog: in 1.13
that dialog cannot be submitted. Later sessions keep the same knowledge base, so you only do this once.

### From session 04: register the MCP server

The filesystem server is registered **by name** in Langflow, so no path is stored in a flow file. Once:

*Settings > MCP Servers > Add MCP Server*, **STDIO**:

- **Name:** `<track>-notlar` (for example `mutfak-notlar`)
- **Command:** `npx`
- **Arguments:** `-y`, `@modelcontextprotocol/server-filesystem`, and the **absolute path** to
  `assets/<track>/notlar` on your machine

Then add an **MCP Tools** component, select the server, turn on **Tool Mode**, and connect *Toolset*
to the Agent's *Tools*. In *Actions* keep only the four you need: `list_allowed_directories`,
`read_text_file`, `append_file`, `edit_file`. This applies to the **solutions too**: a solution from
`04` onward runs only after its MCP server and knowledge base exist.

### Session 05: deploy and run locally

- The flow's endpoint name (for example `mutfak-asistani`) is set in the JSON. Importing a second flow
  with the same name makes Langflow add a `-1` suffix; use the name shown in *Share > API access*.
- The model is `llama3.2:3b` on your own Ollama, so replies are slower, less accurate, and not
  deterministic. That is part of the lesson ("local is weaker"), not a bug. Flow 06 goes back to xAI.

### Session 06: observe

Langflow 1.13 has a built-in **Traces** view (left rail of a flow): every Playground or API run shows
its span tree with latency, tokens and inputs/outputs. It needs no key and is on by default. The judge
branch in `06-izleme` is an ordinary part of the flow, so its score appears in the trace too.

Optional external tracers: set the variables in Langflow Desktop's `.env` (macOS
`~/.langflow/data/.env`, Windows `%APPDATA%\com.LangflowDesktop\data\.env`) and restart Langflow.

- **Langfuse:** `LANGFUSE_SECRET_KEY`, `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_BASE_URL`.
- **LangSmith:** the Langflow docs list `LANGSMITH_TRACING`, `LANGSMITH_ENDPOINT`,
  `LANGSMITH_API_KEY`, `LANGSMITH_PROJECT`, but the 1.13 code only starts the tracer when
  `LANGCHAIN_API_KEY` is set and reads the project from `LANGCHAIN_PROJECT`. Set the `LANGCHAIN_*`
  pair; neither external tracer was exercised end to end for this workshop.

## Notes for instructors

- **Expect 10–20 seconds per reply.** The router and the answer are two model calls, and xAI latency
  varies. One early Playground reply took over two minutes while several people shared one key.
- **Shared keys:** if everyone uses the instructor's keys, run a load dry-run with the full group size
  before the event.
- **Local 3B model:** `llama3.2:3b` mis-routes and hallucinates more than Grok; the session 05 demo
  uses a narrow, recipe-book question on purpose.

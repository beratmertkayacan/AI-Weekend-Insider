# AI Weekend Insider

AI Weekend 201 atölyesi

| Gün        | Konu                                                                  | Klasör                               |
| ---------- | --------------------------------------------------------------------- | ------------------------------------ |
| **1. gün** | Langflow ile adım adım bir yapay zeka asistanı kurmak                 | [`langflow-demos/`](langflow-demos/) |
| **2. gün** | Claude Code: CLAUDE.md, hook, skill, MCP, alt-ajanlar ve orkestrasyon | Deponun geri kalanı                  |

Ortak fikir iki günde de aynı: bir modeli tek başına kullanmak yerine onu **katmanlarla** güçlendirmek.

1. günde bu katmanlar bir Langflow üzerinde pipeline olarak duruyor; 2. günde bir kod deposunda dosyalar olarak.

---

## Klasör yapısı

```
.
├── README.md                      bu dosya
├── CLAUDE.md                      Claude'a proje kuralları (komutlar, kod kuralları, yasak dosyalar)
│
├── langflow-demos/                1. GÜN: Langflow akışları
│   ├── README.md                  kurulum ve oturum rehberi (atölyenin orijinali)
│   ├── mutfak/  hafta-sonu/       4 senaryo, her birinde 6 oturumluk akış (01-temel … 06-izleme)
│   ├── finans/  seyahat/          + kopyala-yapistir.md (hazır prompt ve kurallar)
│   └── assets/                    sentetik girdi verisi (PDF, CSV, notlar)
│
├── app/                           2. GÜN: expense-api (FastAPI)
│   ├── main.py                    endpoint'ler ve bellek içi saklama
│   └── models.py                  veri şekilleri
├── tests/                         pytest testleri (27 test)
│
├── .claude/                       2. GÜN: Claude Code kiti
│   ├── settings.json              hook'ları olaylara bağlar
│   ├── hooks/                     protect-secrets.sh, verify-on-stop.sh
│   ├── skills/                    house-review, changelog, pipeline, team
│   └── agents/                    storage-scout, planner, fixer, test-writer, verifier, reviewer
├── .mcp.json                      projeye bağlı MCP sunucuları (filesystem, github)
│
├── sample-notes/recipes/          filesystem MCP alıştırması için 14 tarif
├── pyproject.toml, uv.lock        Python bağımlılıkları
└── .env.example                   gizli anahtar şablonu (gerçek .env git'e girmez)
```

---

## 1. gün: Langflow

[Langflow](https://www.langflow.org), yapay zekâ uygulamalarını kod yazmadan, kutuları birbirine bağlayarak kurmaya
yarayan görsel bir araç. Atölyede altı oturumda **tek bir asistanı katman katman** büyüttük:

> **düşün → yönlendir → hatırla → araç kullan → yayınla → izle**

| Oturum | Eklenen katman | Ne öğrendim |
|---|---|---|
| `01-temel` | Düşünce zinciri (chain-of-thought) prompt'u | Modelden cevaptan önce adım adım düşünmesini istemek, sonucu daha tutarlı yapıyor. |
| `02-akis` | Smart Router + uzman ajanlar | Soruyu önce sınıflandırıp doğru "uzmana" göndermek; tek dev prompt yerine küçük, odaklı parçalar. |
| `03-hafiza` | Bilgi tabanı (RAG) + sohbet hafızası | Model kendi bilmediğini belgelerden çekiyor (embedding ile), sohbet içinde söylenenleri hatırlıyor. |
| `04-araclar` | Web arama, hesap makinesi, filesystem MCP | Ajan dış araçları çağırabiliyor; MCP ile bir klasördeki notları okuyup yeni dosya yazabiliyor. |
| `05-yayin` | API uç noktası + yerel Ollama modeli | Akışı bir API olarak dışarı açmak; küçük yerel model (`llama3.2:3b`) daha yavaş ve daha hatalı. |
| `06-izleme` | LLM-as-judge (hakem model) + Traces | Bir modelin cevabını başka bir modele puanlatmak; her çalışmanın süresini, token'ını ve adımlarını izlemek. |

Dört senaryo aynı altı katmanı farklı bir günlük problem üzerinde öğretiyor:

| Senaryo | Klasör | Asistan ne yapıyor |
|---|---|---|
| **Mutfak** (ana) | `mutfak/` | Evdekilerle ne pişirilir, alışveriş listesi, aile alerjileri |
| **Hafta sonu** | `hafta-sonu/` | İzmir'de hafta sonu planı: mekân, hava, ulaşım, tercihler |
| **Finans** | `finans/` | Harcama CSV'sini bütçe hedefleriyle karşılaştıran koç |
| **Seyahat** | `seyahat/` | Lizbon gezisi: günlük plan, vize ve belge kontrolü |

**Çalıştırmak için:** Langflow Desktop 1.13.0 kurup bir senaryonun `0N-….json` dosyasını *Upload a flow* ile
yükleyin, tuvaldeki sarı Note'u izleyin. Ayrıntılı kurulum (API anahtarları, Ollama, bilgi tabanı, MCP sunucusu):
[`langflow-demos/README.md`](langflow-demos/README.md).

> API anahtarları akış dosyalarında **yok**; Langflow'un *Global Variables* ayarında tutuluyor. Bu klasöre
> anahtar eklemeyin. `assets/` altındaki bütün veriler sentetiktir.

---

## 2. gün: Claude Code

2. günde küçük bir API projesi üzerinde Claude Code'un dört yapı taşını kurup kullandım, sonra bunları birbirine bağlayan bir sub-agent ekibi tasarlandı.

### Uygulama: expense-api

Harcamaları kaydeden küçük bir FastAPI uygulaması. Veriler bellekte tutulur, uygulama kapanınca silinir.

| İstek | Ne yapar | Durum |
|---|---|---|
| `GET /health` | Sunucu ayakta mı | Eklendi |
| `GET /expenses` | Harcamaları listeler (`?category=` ile filtre) | Hazırdı |
| `POST /expenses` | Harcama ekler | Hazırdı |
| `GET /expenses/total` | Adet ve toplam | Hatası düzeltildi |
| `GET /expenses/summary` | Kategori başına adet ve toplam | Eklendi (alt-ajan ekibiyle) |
| `GET /expenses/{id}` | Tek harcama | Hazırdı |
| `PUT /expenses/{id}` | Harcamayı günceller | Eklendi (alt-ajan ekibiyle) |
| `DELETE /expenses/{id}` | Harcamayı siler | Hazırdı |

- [x] `/health` endpoint'i yoktu.
- [x] `/expenses/total` son harcamayı atlıyordu: `range(len(expenses) - 1)` yerine `sum(...)`.
- [x] Saklama fonksiyonları `app/main.py` içinde; `app/storage.py` dosyasına taşındı

### Dört yapı taşı

| Kavram | Tek cümleyle | Bu depoda | Garantili mi |
|---|---|---|---|
| **CLAUDE.md** | Claude'un her oturumda okuduğu kurallar | `CLAUDE.md` | Hayır, rica düzeyinde |
| **Hook** | Belirli bir anda otomatik çalışan script | `.claude/hooks/` | Evet, Claude atlayamaz |
| **Skill** | Hazır görev tarifi, çoğu zaman bir `/komut` | `.claude/skills/` | Çağrılınca uygulanır |
| **MCP** | Claude'u dış araçlara bağlayan köprü | `.mcp.json` | Bağlantıya bağlı |

**Hook'lar**

- `protect-secrets.sh` (PreToolUse): Claude bir dosyayı okumadan, düzenlemeden ya da komut çalıştırmadan önce
devreye girer; yolda `.env` ya da `secrets` geçiyorsa işlemi durdurur. Başta okuma aracı kapsam dışıydı,
`settings.json` eşleştiricisine `Read` eklenerek kapatıldı.
- `verify-on-stop.sh` (Stop): Claude cevabını bitirirken `.py` dosyaları değiştiyse testleri çalıştırır,
kırmızıysa Claude'u durdurmaz, hatayı geri yollar. `git`, `jq` ve `uv` gerektirir.

**Skill'ler**

| Komut | Ne yapar |
|---|---|
| (kendiliğinden) `house-review` | Kod incelemesi istenince yüklenir: risk yüzeyi, `dosya:satır`, ship / hold kararı |
| `/changelog 20` | Son 20 commit'ten sürüm notu |
| `/pipeline <görev>` | Sıralı ekip: verifier → fixer → verifier → reviewer |
| `/team <görev>` | Dallanan ekip: planner → (fixer ∥ test-writer) → verifier → reviewer |

**MCP sunucuları**

| Sunucu | Ne sağlar | Nerede tanımlı |
|---|---|---|
| filesystem | `~/notes` klasörünü okuma/yazma | `.mcp.json` |
| github | Depo, issue, PR işlemleri (`GITHUB_PAT` gerekir) | `.mcp.json` |
| notion | Notion sayfaları | Kullanıcı ayarı, depoda yok |

Token'lar `.mcp.json` içine yazılmaz; dosyada `${GITHUB_PAT}` yer tutucusu durur, değer `.env` dosyasından gelir.

### Alt-ajan ekibi

Altı alt-ajan var. Her birinin araçları rolüne göre kısıtlı; biri yalnızca okur, biri yalnızca test yazar.

| Ajan | Görevi | Yazabilir mi | Model |
|---|---|---|---|
| `storage-scout` | Saklama katmanını 3 maddede özetler | Hayır | haiku |
| `planner` | Görevi kesin bir sözleşmeye ve iki ayrı görev tarifine çevirir | Hayır | sonnet |
| `fixer` | Kodu yazar ya da düzeltir (`app/`) | Evet | sonnet |
| `test-writer` | Sözleşmeden test yazar, koda bakmadan (`tests/`) | Evet | sonnet |
| `verifier` | `pytest` + `ruff` çalıştırır, teşhis raporu döndürür | Hayır | haiku |
| `reviewer` | Değişikliği bağımsız inceler, karar verir | Hayır | sonnet |

`/team` **akışı:**

```
SİZ ── görev ──► ANA OTURUM (orkestra şefi)
                    │
 1 (aynı anda)      ├─► planner ──► sözleşme + kod tarifi + test tarifi
                    └─► verifier ─► başlangıç yeşil mi?
                    │
 2 (aynı anda)      ├─► fixer ◄──── sözleşme + kod tarifi    → app/
                    └─► test-writer ◄ sözleşme + test tarifi → tests/
                    │
 3                  └─► verifier ─► ikisi uyuşuyor mu?  ── kırmızı ─► onarım turu
 4                  └─► reviewer ─► ship / ship with nits / hold ── hold ─► onarım turu
                    │
 bitiş              └─► rapor + durum panosu ──► SİZ (commit onayı)
```

Tasarım kuralları:

- **Alt-ajanlar birbirine yazamaz.** Her aktarımı ana oturum yapar ve metni değiştirmeden geçirir; bu yüzden her
ajan sabit bir blok döndürür (`AGENT / STATUS / FINDINGS / NEXT`).
- **Paralel dallar aynı dosyaya yazmaz.** `fixer` yalnızca `app/`, `test-writer` yalnızca `tests/` altında çalışır.
- **En fazla 2 tur.** Paralel yapım + bir onarım; sonrasında hâlâ sorun varsa akış "hold" ile durur.
- **Onaysız commit yok, push hiç yok.**

**Gerçek çalıştırmalar:**

| İş | Ajan çalışması | Tur | Sonuç |
|---|---|---|---|
| `PUT /expenses/{id}` | 9 | 2/2 (eksik 422 testleri onarım turunda eklendi) | ship with nits |
| `GET /expenses/summary` | 6 | 1/2 | ship |

İkisinde de kod ve testler birbirini görmeden aynı sözleşmeden yazıldı ve ilk karşılaşmada uyuştu.

**Raporlar:** Her çalıştırma `reports/` altına bir rapor yazar ve `reports/STATUS.md` durum panosunu günceller
(son iş, sonuç, benden beklenen karar, sıradaki tek adım). Bu klasör `.gitignore` içinde, yalnızca yerelde durur.

---

## Kurulum ve komutlar

**Gereksinimler:** [uv](https://docs.astral.sh/uv/) (Python 3.12 ve bağımlılıklar), `jq` (hook'lar için),
Node.js 18+ (MCP sunucuları için), Claude Code. 1. gün için ayrıca Langflow Desktop 1.13.0 ve Ollama.

```bash
uv run pytest -q                                   # testler: 27 passed beklenir
uv run ruff check .                                # kod kuralları
uv run uvicorn app.main:app --reload               # API: http://127.0.0.1:8000/docs
mkdir -p ~/notes && cp -R sample-notes/recipes ~/notes/   # filesystem MCP'nin okuyacağı klasör
cp .env.example .env                               # sonra GITHUB_PAT değerini kendiniz yazın
claude                                             # Claude Code'u başlatır
```

Claude Code içinde:

```
/team <ne eklenecek, ne dönecek, hata durumunda ne olacak>
/pipeline <küçük bir görev>
/changelog 10
/agents     /hooks     /mcp
```

---

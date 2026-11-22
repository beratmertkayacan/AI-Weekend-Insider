# hafta-sonu · kopyala-yapıştır parçalar

Her oturumun eksik parçası için hazır metin. Kendin yazmayı denedikten sonra takılırsan buradan kopyala.

## 01 · Prompt

*Prompt Template* bileşeninin *Template* alanına yapıştır:

```
Sen pratik bir hafta sonu planlayıcısısın. Kullanıcının isteği:
{istek}

Cevap vermeden önce adım adım düşün ve düşünceni göster:
1. Hava: Hafta sonu havası nasıl olabilir? Bilmiyorsan bir varsayım yaptığını belirt; yağmur ihtimali varsa kapalı mekân öner.
2. Etkinlik: 2-3 etkinlik fikrini kısaca karşılaştır.
3. Ulaşım: Seçtiğin yerlere toplu taşıma ya da yürüyerek nasıl gidilir?
4. Seçtiklerinle cumartesi ve pazar için saat saat kısa bir plan yaz.

Bilgi eksikse en sonda "Eksik:" başlığıyla belirt.
```

**Playground'da sor:**

```
Bu hafta sonu İzmir'de iki arkadaşımla ne yapabilirim?
```

Beklenen: Önce adım adım düşünce (hava, etkinlik, ulaşım), sonra cumartesi-pazar planı.

## 02 · Smart Router yönlendirme kuralları

*Smart Router* → *Routes* → *Open table*. Sol alttaki **+** ile her dal için bir satır ekle, hücrelere aşağıdakileri yapıştır, sonra *Save*.

### Satır 1: Plan

**Route Name**

```
Plan
```

**Route Description**

```
Kullanıcı hafta sonu için bir gün, program ya da plan hazırlanmasını istiyor.
```

**Route Message (Optional)**: boş bırak.

### Satır 2: Etkinlik ve hava

**Route Name**

```
Etkinlik ve hava
```

**Route Description**

```
Kullanıcı hava durumunu, hafta sonu ne yapabileceğini ya da etkinlik ve mekân fikirlerini soruyor.
```

**Route Message (Optional)**: boş bırak.

### Satır 3: Ulaşım

**Route Name**

```
Ulaşım
```

**Route Description**

```
Kullanıcı bir yere nasıl gideceğini, toplu taşıma seçeneklerini ya da yolculuk süresini soruyor.
```

**Route Message (Optional)**: boş bırak.

> **Route Name** harfi harfine yukarıdaki gibi olmalı: router'daki çıkışın adı bu olur ve model cevabında bu adı döndürür.
> **Route Message**'ı doldurma: doluysa router kullanıcının sorusu yerine o metni uzmana gönderir, Prompt ve Agent soruyu hiç görmez.

**Playground'da sor** (her soruyu ayrı mesaj olarak gönder; her biri başka bir *Chat Output*'tan dönmeli):

→ *Plan* dalı

```
Cumartesi için İzmir'de bir günlük plan yap
```

→ *Etkinlik ve hava* dalı

```
Yağmur yağarsa hafta sonu İzmir'de ne yapabilirim?
```

→ *Ulaşım* dalı

```
Konak'tan Alsancak'a toplu taşımayla nasıl giderim?
```

### Agent Instructions

Starter'da dolu gelir. Alan boşalırsa ya da değiştirmek istersen ilgili Agent'ın *Agent Instructions* alanına yapıştır:

**Etkinlik ve hava**

```
Sen bir hafta sonu etkinlik ve hava danışmanısın. Kullanıcının sorusuna göre 2-3 somut etkinlik ya da hava durumuna uygun öneri ver.
Güncel hava ya da etkinlik takvimini bilmiyorsan bunu açıkça söyle, uydurma. Kısa ve net yaz.
```

**Ulaşım**

```
Sen İzmir için şehir içi ulaşım danışmanısın. Kullanıcının arabası yok; metro, İZBAN, vapur, otobüs ve yürüyüşle nasıl gideceğini adım adım anlat.
Süre ve ücretleri yaklaşık ver; kesin bilmiyorsan bunu söyle. Kısa tut.
```

## 03 · Bilgi tabanı

Yapıştırılacak metin yok: bilgi tabanını oluştur, iki *Knowledge* bileşeninde seç, *Ingest* ▶'a bir kez bas (Note'taki adımlar).

**Playground'da sor:**

```
Vejetaryenim.
```

Beklenen: Önce tercihini söyle.

```
Bu cumartesi için İzmir'de bir plan yap.
```

Beklenen: Aynı sohbette sor: plan vejetaryen tercihini hatırlamalı, mekânlar PDF'ten gelmeli.

## 04 · MCP araçları

Yapıştırılacak metin yok: MCP sunucusunu kaydet, *MCP Tools* bileşenini Agent'ın *Tools*'una bağla (Note'taki adımlar).

**Playground'da sor:**

```
Notlar klasöründeki tercihlerime bakarak bu hafta sonu için bir plan öner
```

Beklenen: Cevapta tercihler.md'deki kurallar (300 TL, toplu taşıma, 11:00 öncesi yok) geçmeli.

## 05 · Yerel model

Yapıştırılacak metin yok: Ollama bileşeninde *Model Name* olarak `llama3.2:3b` seç.

**Playground'da sor:**

```
Konak'tan Alsancak'a toplu taşımayla nasıl giderim?
```

Beklenen: Cevap kendi bilgisayarındaki modelden gelir.

## 06 · Hakem talimatı

Yeni *Prompt Template* bileşeninin *Template* alanına yapıştır:

```
Sen bir hafta sonu planı hakemisin. Kurallar:
- Pazartesi kapalı olan mekânlar önerilmemeli.
- Kişi başı bütçe 300 TL'yi geçmemeli.
- Ulaşım toplu taşıma ya da yürüyüşle olmalı.
- Cumartesi 11:00'den önceye plan konmamalı.

Soru: {soru}
Cevap: {cevap}

Cevabı 1 ile 5 arasında puanla (5: dört kurala da uyuyor, 1: kuralların çoğu çiğnenmiş).
Yalnızca iki satır yaz:
Puan: N
Gerekçe: tek cümle
```

**Playground'da sor:**

```
Cumartesi için bir hafta sonu planı yap
```

Beklenen: Plan cevabının altında Hakem puanı görünmeli.

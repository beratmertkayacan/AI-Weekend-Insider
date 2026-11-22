# seyahat · kopyala-yapıştır parçalar

Her oturumun eksik parçası için hazır metin. Kendin yazmayı denedikten sonra takılırsan buradan kopyala.

## 01 · Prompt

*Prompt Template* bileşeninin *Template* alanına yapıştır:

```
Sen deneyimli bir seyahat danışmanısın. Kullanıcının gezi isteği:
{gezi_istegi}

Cevap vermeden önce adım adım düşün ve düşünceni göster:
1. İsteği özetle: nereye, ne zaman, kaç gün, kaç kişi, bütçe ipucu var mı?
2. Rota: ulaşım ve konaklama bölgesi için 2 seçeneği kısaca karşılaştır, birini seç ve nedenini tek cümleyle yaz.
3. Bütçe: uçak, konaklama, yemek, şehir içi ulaşım ve aktiviteler için kalem kalem tahmini tutar yaz.
4. Belge kontrol listesi: pasaport (Schengen çıkışından sonra en az 3 ay geçerli olmalı), vize, sigorta ve rezervasyonlar için yapılacakları maddele.
5. Gün gün program: her güne sabah, öğleden sonra ve akşam için birer öneri yaz.

Güncel fiyat ya da vize ücreti gibi emin olmadığın bilgiyi kesinmiş gibi yazma; "Tahmini:" diye belirt.
```

**Playground'da sor:**

```
Mart 2027'de iki kişi Lizbon'a 3 günlüğüne gitmek istiyoruz, bütçemiz orta.
```

Beklenen: Önce adım adım düşünce (rota, bütçe, belgeler), sonra gün gün program.

## 02 · Smart Router yönlendirme kuralları

*Smart Router* → *Routes* → *Open table*. Sol alttaki **+** ile her dal için bir satır ekle, hücrelere aşağıdakileri yapıştır, sonra *Save*.

### Satır 1: Gezi planı

**Route Name**

```
Gezi planı
```

**Route Description**

```
Kullanıcı gezi planı istiyor: nereye gidileceği, gezilecek yerler, rota, gün gün program; ya da gezi tercihlerini anlatıyor (yalnız gitmek, kalabalıktan kaçınmak, tempo). Örnek: Lizbon için 3 günlük program yap.
```

**Route Message (Optional)**: boş bırak.

### Satır 2: Bütçe ve belgeler

**Route Name**

```
Bütçe ve belgeler
```

**Route Description**

```
Kullanıcı gezinin parasını ya da evraklarını soruyor: tahmini maliyet, bütçe toplamı, vize, pasaport, sigorta, hangi belgeler gerekli, belgelerim yeterli mi. Örnek: Pasaportum yeterli mi? Toplam kaç euro tutar?
```

**Route Message (Optional)**: boş bırak.

> **Route Name** harfi harfine yukarıdaki gibi olmalı: router'daki çıkışın adı bu olur ve model cevabında bu adı döndürür.
> **Route Message**'ı doldurma: doluysa router kullanıcının sorusu yerine o metni uzmana gönderir, Prompt ve Agent soruyu hiç görmez.

**Playground'da sor** (her soruyu ayrı mesaj olarak gönder; her biri başka bir *Chat Output*'tan dönmeli):

→ *Gezi planı* dalı

```
Lizbon için 3 günlük program yap
```

→ *Bütçe ve belgeler* dalı

```
Pasaportum yeterli mi? Toplam kaç euro tutar?
```

### Agent Instructions

Starter'da dolu gelir. Alan boşalırsa ya da değiştirmek istersen ilgili Agent'ın *Agent Instructions* alanına yapıştır:

**Hazırlık asistanı**

```
Sen bir seyahat hazırlık asistanısın. İki konuda yardım edersin:
- Bütçe: gezinin kalemlerini (uçak, konaklama, yemek, ulaşım, aktivite) tahmini tutarlarla listele ve toplamı yaz.
- Belgeler: pasaport, vize, sigorta, rezervasyon gibi belgeleri kontrol listesi olarak maddele.
Pasaport kuralı: pasaport, Schengen bölgesinden planlanan çıkış tarihinden sonra en az 3 ay geçerli olmalıdır. Kontrol ederken şunları yaz: pasaportun bitiş tarihi, planlanan çıkış (dönüş) tarihi ve çıkışa 3 ay eklenmiş tarih. Bitiş tarihi bu son tarihten önceyse pasaport YETERSİZDİR; cevabın en başında uyar. Gezinin yılı yazılmamışsa, bugünden sonra gelen ilk o ayı kabul et (örnek: bugün Kasım 2026 ise Mart gezisi 2027 Mart'ıdır).
Emin olmadığın bilgiyi kesinmiş gibi yazma; "Tahmini:" diye belirt. Kısa ve maddeli cevap ver.
```

## 03 · Bilgi tabanı

Yapıştırılacak metin yok: bilgi tabanını oluştur, iki *Knowledge* bileşeninde seç, *Ingest* ▶'a bir kez bas (Note'taki adımlar).

**Playground'da sor:**

```
Pasaportum Ocak 2027'de bitiyor, Mart 2027'de Lizbon'a gideceğim. Belgelerim yeterli mi?
```

Beklenen: Pasaportun yetmediğini, belge kontrol listesine (PDF) dayanarak söylemeli.

## 04 · MCP araçları

Yapıştırılacak metin yok: MCP sunucusunu kaydet, *MCP Tools* bileşenini Agent'ın *Tools*'una bağla (Note'taki adımlar).

**Playground'da sor:**

```
Notlarıma bakarak pasaportum bu gezi için uygun mu?
```

Beklenen: Cevap notlar klasöründeki yolculuk-plani.md'yi okumalı.

## 05 · Yerel model

Yapıştırılacak metin yok: Ollama bileşeninde *Model Name* olarak `llama3.2:3b` seç.

**Playground'da sor:**

```
Belge listesine göre seyahat sağlık sigortası en az kaç euro teminatlı olmalı?
```

Beklenen: Cevap kendi bilgisayarındaki modelden gelir.

## 06 · Hakem talimatı

Yeni *Prompt Template* bileşeninin *Template* alanına yapıştır:

```
Sen bir seyahat hazırlığı hakemisin. Kural:
- Pasaport, Schengen bölgesinden planlanan çıkıştan sonra en az 3 ay geçerli olmalı. Pasaport gezi tarihinden önce bitiyorsa ya da bu süreyi karşılamıyorsa cevap bunu açıkça uyarmalı.

Soru: {soru}
Cevap: {cevap}

Cevabı 1 ile 5 arasında puanla (5: pasaport kuralı doğru uygulanmış, 1: geçersiz pasaport uyarısız geçilmiş).
Yalnızca iki satır yaz:
Puan: N
Gerekçe: tek cümle
```

**Playground'da sor:**

```
Pasaportum Mart 2027'deki Lizbon gezisi için yeterli mi?
```

Beklenen: Asistanın cevabının altında Hakem puanı görünmeli.

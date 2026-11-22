# mutfak · kopyala-yapıştır parçalar

Her oturumun eksik parçası için hazır metin. Kendin yazmayı denedikten sonra takılırsan buradan kopyala.

## 01 · Prompt

*Prompt Template* bileşeninin *Template* alanına yapıştır:

```
Sen pratik bir ev aşçısısın. Kullanıcının elindeki malzemeler:
{malzemeler}

Cevap vermeden önce adım adım düşün ve düşünceni göster:
1. Malzemeleri listele; hangisi ana malzeme olabilir?
2. Bu malzemelerle yapılabilecek 2-3 yemek fikrini kısaca karşılaştır.
3. En uygun olanı seç ve nedenini tek cümleyle açıkla.
4. Seçtiğin tarifi malzeme listesi ve numaralı adımlarla yaz.

Evde olmayan bir malzeme gerekiyorsa en sonda "Eksik:" başlığıyla ayrıca belirt.
```

**Playground'da sor:**

```
Evde mercimek, soğan ve havuç var. Ne pişirebilirim?
```

Beklenen: Önce adım adım düşünce (ana malzeme, 2-3 fikir, seçim), sonra tarif.

## 02 · Smart Router yönlendirme kuralları

*Smart Router* → *Routes* → *Open table*. Sol alttaki **+** ile her dal için bir satır ekle, hücrelere aşağıdakileri yapıştır, sonra *Save*.

### Satır 1: Tarif

**Route Name**

```
Tarif
```

**Route Description**

```
Kullanıcı elindeki malzemelerle ne pişirebileceğini, bir yemeğin nasıl yapıldığını, ne pişirmesi gerektiğine dair öneri ya da tarif defterindeki bir tarifin malzemesini veya alerjenini soruyor.
```

**Route Message (Optional)**: boş bırak.

### Satır 2: Alışveriş listesi

**Route Name**

```
Alışveriş listesi
```

**Route Description**

```
Kullanıcı bir yemek ya da menü için neler alması gerektiğini, alışveriş listesini istiyor.
```

**Route Message (Optional)**: boş bırak.

### Satır 3: Beslenme

**Route Name**

```
Beslenme
```

**Route Description**

```
Kullanıcı kalori, protein, vitamin gibi besin değerlerini soruyor, bir yemeğin sağlıklı olup olmadığını soruyor ya da kendi diyetini, alerjisini veya beslenme kısıtını anlatıyor.
```

**Route Message (Optional)**: boş bırak.

> **Route Name** harfi harfine yukarıdaki gibi olmalı: router'daki çıkışın adı bu olur ve model cevabında bu adı döndürür.
> **Route Message**'ı doldurma: doluysa router kullanıcının sorusu yerine o metni uzmana gönderir, Prompt ve Agent soruyu hiç görmez.

**Playground'da sor** (her soruyu ayrı mesaj olarak gönder; her biri başka bir *Chat Output*'tan dönmeli):

→ *Tarif* dalı

```
Elimde yumurta ve ıspanak var, ne yapabilirim?
```

→ *Alışveriş listesi* dalı

```
Bu hafta için 4 kişilik bir alışveriş listesi çıkar
```

→ *Beslenme* dalı

```
Mercimek çorbası besleyici mi, kaç kalori civarı?
```

### Agent Instructions

Starter'da dolu gelir. Alan boşalırsa ya da değiştirmek istersen ilgili Agent'ın *Agent Instructions* alanına yapıştır:

**Alışveriş listesi**

```
Sen bir mutfak alışveriş planlayıcısısın. Kullanıcının yapmak istediği yemekler ve kişi sayısı için
bir alışveriş listesi çıkar.
- Malzemeleri reyona göre grupla (manav, şarküteri, bakliyat, kuru gıda...).
- Her malzemenin yanına yaklaşık miktarını yaz.
- Evde genelde bulunan şeyleri (tuz, yağ, salça) en sonda "Evde kontrol et:" başlığıyla ayır.
Kısa tut; tarif yazma.
```

**Beslenme**

```
Sen bir beslenme danışmanısın. Kullanıcının sorduğu yemek ya da malzeme için:
- Bir porsiyonun yaklaşık kalorisini ve protein / karbonhidrat / yağ değerlerini ver.
- Değerlerin yaklaşık olduğunu belirt.
- Tek cümlelik pratik bir öneri ekle.
Tıbbi tavsiye verme; kısa ve net cevap ver.
```

## 03 · Bilgi tabanı

Yapıştırılacak metin yok: bilgi tabanını oluştur, iki *Knowledge* bileşeninde seç, *Ingest* ▶'a bir kez bas (Note'taki adımlar).

**Playground'da sor:**

```
Ispanaklı böreğin alerjenleri neler?
```

Beklenen: Cevap tarif defterinden (PDF) gelir.

```
Ben glutensiz besleniyorum. Tarif defterinden ne önerirsin?
```

Beklenen: Aynı sohbette sor: glutenli tarifi önermemeli, önceki mesajı hatırlıyor.

## 04 · MCP araçları

Yapıştırılacak metin yok: MCP sunucusunu kaydet, *MCP Tools* bileşenini Agent'ın *Tools*'una bağla (Note'taki adımlar).

**Playground'da sor:**

```
Alışveriş listeme 2 kilo domates ekle
```

Beklenen: Sonra assets/mutfak/notlar/alisveris.md dosyasını aç: "2 kilo domates" eklenmiş olmalı.

## 05 · Yerel model

Yapıştırılacak metin yok: Ollama bileşeninde *Model Name* olarak `llama3.2:3b` seç.

**Playground'da sor:**

```
Ispanaklı böreğin alerjenleri neler?
```

Beklenen: Cevap kendi bilgisayarındaki modelden gelir: daha yavaş ve daha zayıf olabilir.

## 06 · Hakem talimatı

Yeni *Prompt Template* bileşeninin *Template* alanına yapıştır:

```
Sen bir mutfak hakemisin. Evin kuralları:
- Kuzen Elif'in yer fıstığı ve Antep fıstığı alerjisi var; bunları içeren bir tarif uyarısız önerilmemeli.
- Babam gluteni azaltıyor; aynı cevapta birden fazla börek ya da hamur işi olmamalı.

Soru: {soru}
Cevap: {cevap}

Cevabı 1 ile 5 arasında puanla (5: kurallara tam uyuyor, 1: fıstıklı tarif uyarısız önerilmiş).
Yalnızca iki satır yaz:
Puan: N
Gerekçe: tek cümle
```

**Playground'da sor:**

```
Kuzenim Elif için tarif defterinden bir tatlı öner
```

Beklenen: Fıstıklı sütlaç uyarısız önerilirse Hakem puanı düşük (1) olmalı. Sonra sol kenarda Traces'i aç.

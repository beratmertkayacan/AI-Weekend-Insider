# finans · kopyala-yapıştır parçalar

Her oturumun eksik parçası için hazır metin. Kendin yazmayı denedikten sonra takılırsan buradan kopyala.

## 01 · Prompt

Bu track'te 01'in Prompt'u, 02'de üç dala ayrılmış hâliyle duruyor. 01 için ilkini kullan:

```
Sen sakin ve dürüst bir kişisel finans koçusun. Kullanıcının bu ayki harcamaları (CSV):
{harcamalar}

Bütçe hedefleri: aylık toplam harcama en fazla 18.000 TL; kategori limitleri: market 5.000 TL, ulaşım 2.000 TL, eğlence 2.500 TL, abonelik 600 TL; ay sonunda en az 3.000 TL birikim.

Kullanıcının isteği: {soru}

Cevap vermeden önce adım adım düşün ve düşünceni göster:
1. Harcamaları kategoriye göre ayrı ayrı topla.
2. Toplamı ve her kategoriyi hedefle karşılaştır; hedefi ya da limiti aşanları bul.
3. Aşımları büyükten küçüğe sırala ve her birinin aşım miktarını yaz.
4. Sonunda "Uyarı:" başlığıyla en önemli iki aşımı tek cümleyle özetle.
```

**Playground'da sor:**

```
Bu ay bütçemi aştım mı?
```

Beklenen: Önce kategorilere göre toplam ve limitlerle karşılaştırma, sonra "Uyarı:" özeti.

## 02 · Smart Router yönlendirme kuralları

*Smart Router* → *Routes* → *Open table*. Sol alttaki **+** ile her dal için bir satır ekle, hücrelere aşağıdakileri yapıştır, sonra *Save*.

### Satır 1: Bütçe uyarısı

**Route Name**

```
Bütçe uyarısı
```

**Route Description**

```
Kullanıcı harcamalarının bütçeyi ya da kategori limitlerini aşıp aşmadığını, nereye çok harcadığını soruyor.
```

**Route Message (Optional)**: boş bırak.

### Satır 2: Kategori raporu

**Route Name**

```
Kategori raporu
```

**Route Description**

```
Kullanıcı harcamalarının kategorilere göre tablo ya da dökümünü istiyor.
```

**Route Message (Optional)**: boş bırak.

### Satır 3: Tasarruf koçu

**Route Name**

```
Tasarruf koçu
```

**Route Description**

```
Kullanıcı birikim yapmak, harcamayı kısmak ya da bir tasarruf hedefine ulaşmak için ne yapması gerektiğini soruyor; yeni bir hedef bildiriyor ya da yukarıdaki iki dala girmeyen başka bir finans isteği var.
```

**Route Message (Optional)**: boş bırak.

> **Route Name** harfi harfine yukarıdaki gibi olmalı: router'daki çıkışın adı bu olur ve model cevabında bu adı döndürür.
> **Route Message**'ı doldurma: doluysa router kullanıcının sorusu yerine o metni uzmana gönderir, Prompt ve Agent soruyu hiç görmez.

**Playground'da sor** (her soruyu ayrı mesaj olarak gönder; her biri başka bir *Chat Output*'tan dönmeli):

→ *Bütçe uyarısı* dalı

```
Bu ay hangi kategorilerde limiti aştım?
```

→ *Kategori raporu* dalı

```
Harcamalarımı kategoriye göre tablo halinde göster
```

→ *Tasarruf koçu* dalı

```
Ay sonunda 3.000 TL biriktirmek için neyi kısmalıyım?
```

### Agent Instructions

Starter'da dolu gelir. Alan boşalırsa ya da değiştirmek istersen ilgili Agent'ın *Agent Instructions* alanına yapıştır:

**Tasarruf koçu**

```
Sen kişisel finans koçusun. Kullanıcının tasarruf hedefine ulaşması için harcamalarına bakıp kısa, somut ve sayılarla desteklenmiş öneriler ver. Önce limiti aşan kategorilerdeki fazlalığı kes; yetmezse limiti olmayan kalemlerden makul bir kısıntı öner. Hangi kategoriden ne kadar kısılacağını ve toplam kısıntıyı yaz. Yatırım ya da kredi tavsiyesi verme.
```

## 03 · Bilgi tabanı

Yapıştırılacak metin yok: bilgi tabanını oluştur, iki *Knowledge* bileşeninde seç, *Ingest* ▶'a bir kez bas (Note'taki adımlar).

**Playground'da sor:**

```
Hedeflerime göre nereden kısmam gerekiyor?
```

Beklenen: Koç limitleri bilgi tabanından (butce-hedefleri.md) getirmeli.

```
Yeni hedefim: yazın tatil için 10.000 TL biriktirmek.
```

Beklenen: Yeni hedefi söyle.

```
Bu hedefe göre bu ay ne kadar kenara koymalıyım?
```

Beklenen: Aynı sohbette sor: yeni hedefi hatırlamalı.

## 04 · MCP araçları

Yapıştırılacak metin yok: MCP sunucusunu kaydet, *MCP Tools* bileşenini Agent'ın *Tools*'una bağla (Note'taki adımlar).

**Playground'da sor:**

```
Tasarruf planımı notlar klasörüne tasarruf-plani.md olarak kaydet
```

Beklenen: assets/finans/notlar altında dosya oluşmalı.

## 05 · Yerel model

Yapıştırılacak metin yok: Ollama bileşeninde *Model Name* olarak `llama3.2:3b` seç.

**Playground'da sor:**

```
Bu ay toplam ne kadar harcadım?
```

Beklenen: Küçük yerel model sayıları bazen yanlış toplar; farkı gözle.

## 06 · Hakem talimatı

Yeni *Prompt Template* bileşeninin *Template* alanına yapıştır:

```
Sen bir kişisel finans cevabı hakemisin. Kurallar:
- Cevaptaki rakamlar harcamalarla tutarlı olmalı.
- Limit aşımları açıkça belirtilmeli.
- Öneriler somut olmalı.
- Yatırım tavsiyesi verilmemeli.

Soru: {soru}
Cevap: {cevap}

Cevabı 1 ile 5 arasında puanla (5: dört kurala da uyuyor, 1: rakamlar tutarsız ya da yatırım tavsiyesi var).
Yalnızca iki satır yaz:
Puan: N
Gerekçe: tek cümle
```

**Playground'da sor:**

```
Eğlence harcamamı nasıl azaltabilirim?
```

Beklenen: İki cevap gelir: koçun cevabı ve Hakem puanı.

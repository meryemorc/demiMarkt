from pymongo import MongoClient  # type: ignore

# MongoDB bağlantısı ayarları
MONGO_URI = "mongodb+srv://meryemoruc:Asd12345@cluster0.ifzdj.mongodb.net/demiMarktDB?retryWrites=true&w=majority&appName=Cluster0"
DB_NAME = "demiMarktDB"  # Veritabanı adı
COLLECTION_NAME = "demiMarktBirlesik"  # Koleksiyon adı

# MongoDB bağlantısı
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def remove_duplicates_via_python():
    """
    Tüm kayıtları çekerek Python üzerinden duplicate ID'leri temizler.
    """
    print("Kayıtlar getiriliyor...")
    documents = list(collection.find({}, {"ID": 1}))  # Sadece ID alanını al
    print(f"Toplam {len(documents)} kayıt bulundu.")

    seen_ids = set()
    duplicates = []

    for doc in documents:
        if doc["ID"] in seen_ids:
            duplicates.append(doc["_id"])  # Duplicate olanları kaydet
        else:
            seen_ids.add(doc["ID"])

    # Duplicate olan kayıtları sil
    if duplicates:
        print(f"{len(duplicates)} adet duplicate bulundu. Silme işlemi başlıyor...")
        result = collection.delete_many({"_id": {"$in": duplicates}})
        print(f"{result.deleted_count} adet kayıt silindi.")
    else:
        print("Duplicate kayıt bulunamadı.")

if __name__ == "__main__":
    remove_duplicates_via_python()

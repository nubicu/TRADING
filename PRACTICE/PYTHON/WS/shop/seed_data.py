from sqlalchemy.orm import Session
import models

def seed_products(db: Session):
    categories_data = [
        {"name": "Electronice", "slug": "electronice"},
        {"name": "Haine", "slug": "haine"},
        {"name": "Casa & Grădină", "slug": "casa-gradina"},
        {"name": "Sport", "slug": "sport"},
        {"name": "Jucării", "slug": "jucarii"},
        {"name": "Frumusețe", "slug": "frumusete"},
    ]
    
    categories = {}
    for cat_data in categories_data:
        existing = db.query(models.Category).filter(models.Category.slug == cat_data["slug"]).first()
        if not existing:
            cat = models.Category(**cat_data)
            db.add(cat)
            db.flush()
            categories[cat_data["slug"]] = cat.id
        else:
            categories[cat_data["slug"]] = existing.id
    
    products_data = [
        {"name": "iPhone 15 Pro", "description": "Smartphone premium Apple cu chip A17 Pro, cameră 48MP și ecran Super Retina XDR de 6.1 inch. Procesor ultra-rapid, autonomie excelentă și design din titan.", "price": 4999.99, "old_price": 5499.99, "stock": 15, "image_url": "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=500", "category_slug": "electronice", "rating": 4.8, "reviews_count": 234, "is_featured": True},
        {"name": "Samsung Galaxy S24", "description": "Flagship Android cu AI integrat, cameră de 200MP și display Dynamic AMOLED 2X de 6.2 inch. Baterie de 4000mAh cu încărcare rapidă de 25W.", "price": 3799.99, "old_price": None, "stock": 22, "image_url": "https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=500", "category_slug": "electronice", "rating": 4.6, "reviews_count": 189, "is_featured": True},
        {"name": "Laptop Dell XPS 15", "description": "Laptop premium pentru profesioniști cu procesor Intel Core i7, 16GB RAM, SSD 512GB și display OLED 4K de 15.6 inch. Perfect pentru editare video și programare.", "price": 8499.99, "old_price": 9299.99, "stock": 8, "image_url": "https://images.unsplash.com/photo-1593642632559-0c6d3fc62b89?w=500", "category_slug": "electronice", "rating": 4.7, "reviews_count": 87, "is_featured": True},
        {"name": "AirPods Pro 2", "description": "Căști wireless cu anulare activă a zgomotului, sunet spațial personalizat și autonomie de 6 ore. Carcasă de încărcare MagSafe cu USB-C.", "price": 1299.99, "old_price": 1499.99, "stock": 30, "image_url": "https://images.unsplash.com/photo-1600294037681-c80b4cb5b434?w=500", "category_slug": "electronice", "rating": 4.9, "reviews_count": 412, "is_featured": False},
        {"name": "Tricou Premium Bumbac", "description": "Tricou din 100% bumbac organic, confortabil și durabil. Disponibil în multiple culori. Tăietură slim-fit modernă, perfect pentru zi de zi.", "price": 89.99, "old_price": 120.00, "stock": 100, "image_url": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500", "category_slug": "haine", "rating": 4.5, "reviews_count": 56, "is_featured": False},
        {"name": "Jachetă Piele Naturală", "description": "Jachetă din piele naturală de cea mai înaltă calitate, cu căptușeală din lână merinos. Design clasic și durabilitate excepțională.", "price": 899.99, "old_price": 1200.00, "stock": 12, "image_url": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=500", "category_slug": "haine", "rating": 4.7, "reviews_count": 34, "is_featured": True},
        {"name": "Set Oale Inox Premium", "description": "Set complet de 7 oale și tigăi din inox 18/10, cu fund triplu stratificat pentru distribuție uniformă a căldurii. Compatibil cu toate tipurile de plite.", "price": 449.99, "old_price": 599.99, "stock": 18, "image_url": "https://images.unsplash.com/photo-1584269600464-37b1b58a9fe7?w=500", "category_slug": "casa-gradina", "rating": 4.6, "reviews_count": 78, "is_featured": False},
        {"name": "Robot de Bucătărie 1500W", "description": "Robot multifuncțional cu 12 viteze, bol de 5L din inox și 15 accesorii incluse. Perfect pentru frămantat, tocat, amestecat și ras.", "price": 799.99, "old_price": None, "stock": 9, "image_url": "https://images.unsplash.com/photo-1570222094114-d054a817e56b?w=500", "category_slug": "casa-gradina", "rating": 4.4, "reviews_count": 45, "is_featured": False},
        {"name": "Bicicletă MTB Carbon", "description": "Bicicletă de munte cu cadru din carbon, suspensie față și spate de 140mm, 12 viteze Shimano Deore și frâne hidraulice. Pentru trail-uri exigente.", "price": 3299.99, "old_price": 3999.99, "stock": 5, "image_url": "https://images.unsplash.com/photo-1576435728678-68d0fbf94946?w=500", "category_slug": "sport", "rating": 4.8, "reviews_count": 23, "is_featured": True},
        {"name": "Saltea Yoga Premium 6mm", "description": "Saltea din cauciuc natural eco-friendly, antialunecare, cu grosime de 6mm pentru confort optim. Include geantă de transport. Dimensiuni 183x61cm.", "price": 199.99, "old_price": 249.99, "stock": 40, "image_url": "https://images.unsplash.com/photo-1601925228269-cca8f0c57d06?w=500", "category_slug": "sport", "rating": 4.7, "reviews_count": 167, "is_featured": False},
        {"name": "LEGO Technic Lamborghini", "description": "Set LEGO Technic 42111 cu 1428 piese. Reproduce fidel Lamborghini Sián FKP 37, cu motor V12 funcțional, transmisie și spoiler activ. Vârsta recomandata 18+.", "price": 449.99, "old_price": 499.99, "stock": 14, "image_url": "https://images.unsplash.com/photo-1587654780291-39c9404d746b?w=500", "category_slug": "jucarii", "rating": 4.9, "reviews_count": 89, "is_featured": True},
        {"name": "Serum Vitamina C 20%", "description": "Ser facial cu vitamina C 20% stabilizată, acid hialuronic și niacinamidă. Iluminează tenul, reduce petele pigmentare și stimulează producția de colagen.", "price": 159.99, "old_price": 199.99, "stock": 50, "image_url": "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=500", "category_slug": "frumusete", "rating": 4.8, "reviews_count": 234, "is_featured": True},
    ]
    
    for prod_data in products_data:
        slug = prod_data.pop("category_slug")
        cat_id = categories.get(slug)
        if cat_id and not db.query(models.Product).filter(models.Product.name == prod_data["name"]).first():
            product = models.Product(**prod_data, category_id=cat_id)
            db.add(product)
    
    db.commit()
    print("✅ Seed data adăugat cu succes!")
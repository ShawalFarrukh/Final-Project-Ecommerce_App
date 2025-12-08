--unique index
CREATE UNIQUE INDEX IF NOT EXISTS idx_products_name ON products(name);

--Dry eye products
INSERT INTO products (name, price, image_url, description) VALUES
('PF Lubricating Drops (30 vials)', 1200, '/static/img/drops_pf.jpg',
 'Single-use PF vials for daytime relief.'),
('Warm Compress Eye Mask', 1800, '/static/img/warm_mask.jpg',
 'Microwaveable mask for meibomian gland warming.'),
('Lid Wipes (Pack of 30)', 900, '/static/img/lid_wipes.jpg',
 'Daily lid hygiene to reduce debris and soothe lids.'),
('Omega-3 Softgels (60 ct)', 2200, '/static/img/omega3.jpg',
 'Dietary supplement often used alongside eyelid care.'),
('Lid Cleanser', 1500, '/static/img/lid_cleanser.jpg',
 'Gentle foaming cleanser for lids and lashes.'),
 ('Sleeping Mask', 1500, '/static/img/sleeping_mask.jpg',
 'Sleeping Mask for night-time .')
 ON CONFLICT(name) DO UPDATE SET
  price = excluded.price,
  image_url = excluded.image_url,
  description = excluded.description;

-- INSERTAR COMPRA
-- CREATE TRIGGER after_purchase_insert
-- AFTER INSERT ON detail_purchase
-- FOR EACH ROW
-- BEGIN
--     UPDATE product
--     SET stock = stock + NEW.quantity
--     WHERE id = NEW.product_id;
-- END;

-- ELIMINAR COMPRA
-- CREATE TRIGGER after_purchase_delete
-- AFTER DELETE ON detail_purchase
-- FOR EACH ROW
-- BEGIN
--     UPDATE product 
--     SET stock = stock - OLD.quantity
--     WHERE id = OLD.product_id;
-- END;

-- ACTUALIZAR COMPRA
-- CREATE TRIGGER after_purchase_update
-- AFTER UPDATE ON detail_purchase
-- FOR EACH ROW
-- BEGIN
--     IF OLD.quantity != NEW.quantity THEN
--         UPDATE product 
--         SET stock = stock - OLD.quantity + NEW.quantity
--         WHERE id = NEW.product_id;
--     END IF;
-- END;

DESCRIBE purchase;
DESCRIBE detail_purchase;

SELECT * FROM purchase;
SELECT * FROM product;
SELECT * FROM detail_purchase;

-- TABLA PRODUCTOS
-- SELECT
-- purchase.id,
-- product.name,
-- product.supplier,
-- purchase.date,
-- detail_purchase.unitary_price,
-- detail_purchase.quantity,
-- (detail_purchase.unitary_price * detail_purchase.quantity) AS total
-- FROM detail_purchase, purchase, product, user
-- WHERE 
-- detail_purchase.purchase_id = purchase.id AND
-- detail_purchase.product_id = product.id AND
-- user.id = purchase.user_id AND
-- user.id = 1;

SELECT purchase_price FROM product WHERE id = 1;
SELECT supplier_id FROM purchase WHERE id = 2;

SELECT product.supplier FROM product, detail_purchase WHERE
product.id = detail_purchase.product_id AND
detail_purchase.purchase_id = 1;
-- Create the trigger that decreases item quantity after a new order is inserted
DELIMITER //

CREATE TRIGGER update_quantity_after_order
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    -- Update the 'items' table to decrease the quantity of the item ordered
    UPDATE items
    SET quantity = quantity - NEW.number
    WHERE name = NEW.item_name;
END //

DELIMITER ;

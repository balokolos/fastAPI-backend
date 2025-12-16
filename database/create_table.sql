CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    phone_number VARCHAR(20),
    address VARCHAR(255)
);

CREATE TABLE coupon (
    coupon_id INT AUTO_INCREMENT PRIMARY KEY,
    user_phone VARCHAR(20),
    coupon_date DATE,
    value INT
);

CREATE TABLE coupon_usage (
    id INT PRIMARY KEY,
    coupon_id INT,
    user_id INT,
    order_id INT,
    usage_date DATE,
    FOREIGN KEY (coupon_id) REFERENCES coupon(coupon_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

CREATE TABLE order_item (
    id INT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT,
    status ENUM('receive', 'inprogress', 'done') NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES product(product_id)
);

CREATE TABLE product (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    type VARCHAR(50),
    price DECIMAL(10,2) NOT NULL
);

CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    product_id INT,
    order_date DATE,
    quantity INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (product_id) REFERENCES product(product_id)
);







ALTER TABLE users
ADD CONSTRAINT unique_phone UNIQUE (phone_number);

INSERT INTO users (first_name, last_name, phone_number, address)
VALUES ('John', 'Doe', '0123456789', '123 Main Street, Kuala Lumpur');


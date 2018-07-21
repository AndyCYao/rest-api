USE lala;
CREATE TABLE order_tbl(
    order_id BIGINT NOT NULL AUTO_INCREMENT,
    orig_lat DECIMAL(9,6),
    orig_long DECIMAL(9,6),
    dest_lat DECIMAL(9,6),
    dest_long DECIMAL(9,6),
    status VARCHAR(20),
    distance FLOAT,
    orderDate DATETIME,
    PRIMARY KEY (order_id)
);
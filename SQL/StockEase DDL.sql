CREATE TABLE users (
    `id` INT AUTO_INCREMENT,
     PRIMARY KEY(`id`),
    `username` VARCHAR(255) NOT NULL UNIQUE,
    `password` VARCHAR(255) NOT NULL,
    `is_admin` BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE `stocks` (
  `id` int NOT NULL AUTO_INCREMENT,
  `item_id` mediumtext,
  `name` mediumtext,
  `price` decimal(12,2) NOT NULL,
  `quantity` int NOT NULL,
  `category` mediumtext,
  `date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
)

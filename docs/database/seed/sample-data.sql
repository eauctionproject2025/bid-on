-- Sample / demo seed (logical MySQL form). Production seed: backend/prisma/seed.ts
USE bidon;

INSERT INTO `Category` (`id`,`name`,`slug`,`parentId`) VALUES
('cat_electronics','Electronics','electronics',NULL),
('cat_fashion','Fashion','fashion',NULL);

-- Passwords are placeholders; real system stores bcrypt hashes (e.g. Password1).
INSERT INTO `User` (`id`,`name`,`email`,`passwordHash`,`role`,`verified`,`kycStatus`,`bankStatus`) VALUES
('user_admin','Admin','admin@bidon.local','$2a$12$examplehashadmin','admin',1,'approved','approved'),
('user_seller','Demo Seller','seller@bidon.local','$2a$12$examplehashseller','seller',1,'approved','approved'),
('user_buyer','Demo Buyer','buyer@bidon.local','$2a$12$examplehashbuyer','buyer',1,'approved','approved');

INSERT INTO `Auction` (`id`,`sellerId`,`categoryId`,`title`,`description`,`images`,`startPrice`,`minBidIncrement`,`currentBid`,`bidCount`,`status`,`endsAt`) VALUES
('auc_watch','user_seller','cat_electronics','Vintage Mechanical Watch','Demo live lot',
 JSON_ARRAY('https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=800'),
 5000.00,100.00,0.00,0,'live', DATE_ADD(UTC_TIMESTAMP(3), INTERVAL 2 DAY));

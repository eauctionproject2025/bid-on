-- =============================================================================
-- Bid On / e-Auction — Logical database schema (MySQL 8+ compatible DDL)
-- =============================================================================
-- Source of truth in production: PostgreSQL 16 via Prisma
--   (backend/prisma/schema.prisma on Render service bid-on-db)
-- This file is a MySQL-compatible logical export for academic submission and
-- portability. JSON/array types are adapted; money uses DECIMAL(12,2).
-- Primary keys use CHAR(25) to hold Prisma cuid() values.
-- =============================================================================

CREATE DATABASE IF NOT EXISTS bidon
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE bidon;

-- ---------------------------------------------------------------------------
-- Enumerations (MySQL ENUM mirrors Prisma enums)
-- ---------------------------------------------------------------------------

-- Role: buyer | seller | admin
-- AuctionStatus: pending | live | ended | cancelled | sold
-- TransactionStatus: pending | held | disputed | completed | failed | refunded
-- VerificationStatus: none | pending | approved | rejected
-- NotificationType: outbid | ending_soon | won | approved | rejected | general

-- ---------------------------------------------------------------------------
-- Table: User
-- Purpose: Identity, RBAC, KYC/bank compliance, reputation aggregates
-- ---------------------------------------------------------------------------
CREATE TABLE `User` (
  `id`                CHAR(25)      NOT NULL COMMENT 'cuid primary key',
  `name`              VARCHAR(191)  NOT NULL,
  `email`             VARCHAR(191)  NOT NULL,
  `passwordHash`      VARCHAR(255)  NOT NULL COMMENT 'bcrypt hash',
  `role`              ENUM('buyer','seller','admin') NOT NULL DEFAULT 'buyer',
  `verified`          TINYINT(1)    NOT NULL DEFAULT 0,
  `otpCode`           VARCHAR(255)  NULL,
  `otpExpiresAt`      DATETIME(3)   NULL,
  `resetOtpCode`      VARCHAR(64)   NULL,
  `resetOtpExpiresAt` DATETIME(3)   NULL,
  `phone`             VARCHAR(64)   NULL,
  `address`           TEXT          NULL,
  `suspended`         TINYINT(1)    NOT NULL DEFAULT 0,
  `ratingAvg`         DOUBLE        NOT NULL DEFAULT 0,
  `ratingCount`       INT           NOT NULL DEFAULT 0,
  `kycStatus`         ENUM('none','pending','approved','rejected') NOT NULL DEFAULT 'none',
  `kycFullName`       VARCHAR(191)  NULL,
  `kycDocumentType`   VARCHAR(64)   NULL,
  `kycDocumentNumber` VARCHAR(128)  NULL,
  `kycDocumentUrl`    VARCHAR(512)  NULL,
  `kycSubmittedAt`    DATETIME(3)   NULL,
  `kycReviewedAt`     DATETIME(3)   NULL,
  `kycRejectReason`   TEXT          NULL,
  `bankStatus`        ENUM('none','pending','approved','rejected') NOT NULL DEFAULT 'none',
  `bankAccountName`   VARCHAR(191)  NULL,
  `bankName`          VARCHAR(191)  NULL,
  `bankAccountNumber` VARCHAR(128)  NULL,
  `bankBranch`        VARCHAR(191)  NULL,
  `bankRoutingNumber` VARCHAR(64)   NULL,
  `bankSubmittedAt`   DATETIME(3)   NULL,
  `bankReviewedAt`    DATETIME(3)   NULL,
  `bankRejectReason`  TEXT          NULL,
  `createdAt`         DATETIME(3)   NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  `updatedAt`         DATETIME(3)   NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3),
  PRIMARY KEY (`id`),
  UNIQUE KEY `User_email_key` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Registered platform users';

-- ---------------------------------------------------------------------------
-- Table: Category (self-referential tree)
-- ---------------------------------------------------------------------------
CREATE TABLE `Category` (
  `id`       CHAR(25)     NOT NULL,
  `name`     VARCHAR(191) NOT NULL,
  `slug`     VARCHAR(191) NOT NULL,
  `parentId` CHAR(25)     NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Category_slug_key` (`slug`),
  KEY `Category_parentId_idx` (`parentId`),
  CONSTRAINT `Category_parentId_fkey`
    FOREIGN KEY (`parentId`) REFERENCES `Category` (`id`)
    ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Auction catalogue hierarchy';

-- ---------------------------------------------------------------------------
-- Table: Auction
-- ---------------------------------------------------------------------------
CREATE TABLE `Auction` (
  `id`              CHAR(25)     NOT NULL,
  `sellerId`        CHAR(25)     NOT NULL,
  `categoryId`      CHAR(25)     NOT NULL,
  `title`           VARCHAR(255) NOT NULL,
  `description`     TEXT         NOT NULL,
  `images`          JSON         NOT NULL COMMENT 'Array of image URL strings (Postgres: text[])',
  `startPrice`      DECIMAL(12,2) NOT NULL,
  `reservePrice`    DECIMAL(12,2) NULL,
  `maxPriceCap`     DECIMAL(12,2) NULL,
  `currentBid`      DECIMAL(12,2) NOT NULL DEFAULT 0.00,
  `minBidIncrement` DECIMAL(12,2) NOT NULL DEFAULT 1.00,
  `bidCount`        INT          NOT NULL DEFAULT 0,
  `status`          ENUM('pending','live','ended','cancelled','sold') NOT NULL DEFAULT 'pending',
  `startsAt`        DATETIME(3)  NULL,
  `endsAt`          DATETIME(3)  NOT NULL,
  `winnerId`        CHAR(25)     NULL,
  `rejectReason`    TEXT         NULL,
  `createdAt`       DATETIME(3)  NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  `updatedAt`       DATETIME(3)  NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3),
  PRIMARY KEY (`id`),
  KEY `Auction_status_idx` (`status`),
  KEY `Auction_endsAt_idx` (`endsAt`),
  KEY `Auction_categoryId_idx` (`categoryId`),
  KEY `Auction_sellerId_idx` (`sellerId`),
  KEY `Auction_winnerId_idx` (`winnerId`),
  CONSTRAINT `Auction_sellerId_fkey`
    FOREIGN KEY (`sellerId`) REFERENCES `User` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `Auction_categoryId_fkey`
    FOREIGN KEY (`categoryId`) REFERENCES `Category` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `Auction_winnerId_fkey`
    FOREIGN KEY (`winnerId`) REFERENCES `User` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Auction listings and clock state';

-- ---------------------------------------------------------------------------
-- Table: Bid
-- ---------------------------------------------------------------------------
CREATE TABLE `Bid` (
  `id`        CHAR(25)      NOT NULL,
  `auctionId` CHAR(25)      NOT NULL,
  `bidderId`  CHAR(25)      NOT NULL,
  `amount`    DECIMAL(12,2) NOT NULL,
  `createdAt` DATETIME(3)   NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  PRIMARY KEY (`id`),
  KEY `Bid_auctionId_idx` (`auctionId`),
  KEY `Bid_bidderId_idx` (`bidderId`),
  CONSTRAINT `Bid_auctionId_fkey`
    FOREIGN KEY (`auctionId`) REFERENCES `Auction` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `Bid_bidderId_fkey`
    FOREIGN KEY (`bidderId`) REFERENCES `User` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Immutable bid history';

-- ---------------------------------------------------------------------------
-- Table: Watchlist
-- ---------------------------------------------------------------------------
CREATE TABLE `Watchlist` (
  `id`        CHAR(25)    NOT NULL,
  `userId`    CHAR(25)    NOT NULL,
  `auctionId` CHAR(25)    NOT NULL,
  `createdAt` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  PRIMARY KEY (`id`),
  UNIQUE KEY `Watchlist_userId_auctionId_key` (`userId`, `auctionId`),
  CONSTRAINT `Watchlist_userId_fkey`
    FOREIGN KEY (`userId`) REFERENCES `User` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `Watchlist_auctionId_fkey`
    FOREIGN KEY (`auctionId`) REFERENCES `Auction` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='User favourite auctions';

-- ---------------------------------------------------------------------------
-- Table: Notification
-- ---------------------------------------------------------------------------
CREATE TABLE `Notification` (
  `id`        CHAR(25) NOT NULL,
  `userId`    CHAR(25) NOT NULL,
  `type`      ENUM('outbid','ending_soon','won','approved','rejected','general') NOT NULL,
  `message`   TEXT     NOT NULL,
  `read`      TINYINT(1) NOT NULL DEFAULT 0,
  `meta`      JSON     NULL,
  `createdAt` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  PRIMARY KEY (`id`),
  KEY `Notification_userId_read_idx` (`userId`, `read`),
  CONSTRAINT `Notification_userId_fkey`
    FOREIGN KEY (`userId`) REFERENCES `User` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='In-app user notifications';

-- ---------------------------------------------------------------------------
-- Table: Transaction (escrow ledger)
-- ---------------------------------------------------------------------------
CREATE TABLE `Transaction` (
  `id`               CHAR(25)      NOT NULL,
  `auctionId`        CHAR(25)      NOT NULL,
  `buyerId`          CHAR(25)      NOT NULL,
  `sellerId`         CHAR(25)      NOT NULL,
  `amount`           DECIMAL(12,2) NOT NULL,
  `stripeSessionId`  VARCHAR(191)  NULL,
  `stripePaymentId`  VARCHAR(191)  NULL,
  `status`           ENUM('pending','held','disputed','completed','failed','refunded') NOT NULL DEFAULT 'pending',
  `heldAt`           DATETIME(3)   NULL,
  `releaseDueAt`     DATETIME(3)   NULL,
  `shippedAt`        DATETIME(3)   NULL,
  `releasedAt`       DATETIME(3)   NULL,
  `disputeReason`    TEXT          NULL,
  `disputedAt`       DATETIME(3)   NULL,
  `resolvedAt`       DATETIME(3)   NULL,
  `resolveNote`      TEXT          NULL,
  `createdAt`        DATETIME(3)   NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  `updatedAt`        DATETIME(3)   NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3),
  PRIMARY KEY (`id`),
  UNIQUE KEY `Transaction_stripeSessionId_key` (`stripeSessionId`),
  KEY `Transaction_auctionId_status_idx` (`auctionId`, `status`),
  KEY `Transaction_buyerId_idx` (`buyerId`),
  KEY `Transaction_sellerId_idx` (`sellerId`),
  CONSTRAINT `Transaction_auctionId_fkey`
    FOREIGN KEY (`auctionId`) REFERENCES `Auction` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `Transaction_buyerId_fkey`
    FOREIGN KEY (`buyerId`) REFERENCES `User` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `Transaction_sellerId_fkey`
    FOREIGN KEY (`sellerId`) REFERENCES `User` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Payment escrow lifecycle per won auction';

-- ---------------------------------------------------------------------------
-- Table: Review
-- ---------------------------------------------------------------------------
CREATE TABLE `Review` (
  `id`         CHAR(25) NOT NULL,
  `auctionId`  CHAR(25) NOT NULL,
  `fromUserId` CHAR(25) NOT NULL,
  `toUserId`   CHAR(25) NOT NULL,
  `rating`     INT      NOT NULL COMMENT 'Typically 1-5',
  `comment`    TEXT     NULL,
  `createdAt`  DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  PRIMARY KEY (`id`),
  UNIQUE KEY `Review_auctionId_fromUserId_key` (`auctionId`, `fromUserId`),
  CONSTRAINT `Review_auctionId_fkey`
    FOREIGN KEY (`auctionId`) REFERENCES `Auction` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `Review_fromUserId_fkey`
    FOREIGN KEY (`fromUserId`) REFERENCES `User` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `Review_toUserId_fkey`
    FOREIGN KEY (`toUserId`) REFERENCES `User` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Post-sale peer ratings';

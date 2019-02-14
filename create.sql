CREATE TABLE `sites` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`name`	TEXT NOT NULL,
	`alias`	TEXT NOT NULL,
	`short`	TEXT NOT NULL,
	`link`	TEXT NOT NULL,
	`added` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE `channels` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`site_id`   INTEGER NOT NULL,
	`channel_id`    INTEGER NOT NULL,
	`added` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE `news` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`site_id`	INTEGER NOT NULL,
	`title`	TEXT NOT NULL,
	`text`	TEXT NOT NULL,
	`link`	TEXT NOT NULL,
	`img_link`	TEXT NOT NULL,
	`tags`	TEXT,
	`added` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `message_id` INTEGER,
	FOREIGN KEY(`site_id`) REFERENCES `sites`(`id`)
);
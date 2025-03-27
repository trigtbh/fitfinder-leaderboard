DROP SCHEMA IF EXISTS "AuraSchema" CASCADE;

CREATE SCHEMA IF NOT EXISTS "AuraSchema";

SET search_path TO "AuraSchema";

CREATE TABLE ProfileTagInfo (
    tag_id VARCHAR(50) PRIMARY KEY,
    tag_name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE UserInfo (
    user_id VARCHAR(50) PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    full_name VARCHAR(255),
    email VARCHAR(255) NOT NULL,
    phone_number VARCHAR(15) UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    bio_text VARCHAR(255),
    profile_pic_url VARCHAR(512),
    follower_ids VARCHAR[] DEFAULT '{}',
    following_ids VARCHAR[] DEFAULT '{}',
    profile_tag_ids VARCHAR[] DEFAULT '{}',
    all_tag_ids VARCHAR[] DEFAULT '{}',
    post_ids VARCHAR[] DEFAULT '{}'
);

CREATE TABLE Like_Info (
    like_id VARCHAR(50) PRIMARY KEY,
    user_liked VARCHAR(50) REFERENCES UserInfo(user_id) NOT NULL,
    time_liked TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE Comment_Info (
    comment_id VARCHAR(50) PRIMARY KEY,
    comment_text VARCHAR(255) NOT NULL,
    user_commented VARCHAR(50) REFERENCES UserInfo(user_id) NOT NULL,
    time_commented TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE PostInfo (
    post_id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50) REFERENCES UserInfo(user_id) NOT NULL,
    image_url VARCHAR(512) NOT NULL,
    post_caption VARCHAR(255),
    time_posted TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    like_ids VARCHAR[] DEFAULT '{}',
    comment_ids VARCHAR[] DEFAULT '{}',
    num_likes INTEGER DEFAULT 0,
    num_comments INTEGER DEFAULT 0
);

CREATE TABLE Leaderboard (
    user_id VARCHAR(50) PRIMARY KEY REFERENCES UserInfo(user_id),
    score INTEGER DEFAULT 0 NOT NULL
);

CREATE TABLE ServerAnalytics (
    analytic_id VARCHAR(50) PRIMARY KEY,
    analytic_name VARCHAR(255) NOT NULL,
    analytic_value JSONB NOT NULL
);
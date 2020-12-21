# AveliBot

This is Telegram bot which adds some features for more convenient and funny conversations in groups and chats. 
It allows to tag all chat members, schedule messages to be sent later, and randomly choose a chat member, who is then called ”the wolf of the day”.

## What can it do?
* `/all` or simply `@all` &mdash; tag all chat members
* `/schedule <time> <message>` &mdash; send `message` at moment `time`
* `/unschedule` &mdash; cancel message from being sent later. The command must be a reply to bot's `/schedule` message confirmation.
* `/sched` &mdash; alias for `/schedule`
* `/unsched` &mdash; alias for `/unschedule`
* `/wolf` &mdash; find out who is the wolf of the day
* `/wolfstats` &mdash; show wolf game stats

## How to run this bot?
1. `cp .env.example .env` 
2. Fill in `.env` file according to the instructions inside of it
3. `docker-compose build`
4. `docker-compose up -d`

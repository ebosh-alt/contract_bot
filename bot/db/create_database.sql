create table users(
    id integer primary key,
    username text,
    status bool default TRUE,
    referral_link text,
    referral_boss_id integer default null,
    withdrawal_account text,
    balance integer default 0,
    bonus_account integer default 0,
    earnings_from_contracts integer default 0,
    earnings_from_partners integer default 0,
    flag integer,
    bot_message_id integer,
    delete_message_id integer default null,
    foreign key(referral_boss_id) references users(id)
);

create table contracts(
    id integer primary key ,
    count_day integer,
    amount integer,
    user_id integer,
    foreign key(user_id) references users(id)
);

-- drop table users;

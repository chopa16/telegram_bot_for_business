CREATE TABLE if not exists users
(
    chat_id  int not null PRIMARY KEY,
    username varchar(50),
    full_name varchar(50),
    tel_number text,
    address text,
    id serial not null
);
CREATE TABLE if not exists foto (
    id serial PRIMARY KEY,
    name text,
    thing text,
    cloth text,
    cost real,
    size text,
    from_size real,
    to_size real
);
CREATE TABLE if not exists buy_thing
(
    id serial PRIMARY KEY,
    chat_id_user int references users(chat_id),
    id_foto int references foto(id),
    quantity int not null,
    total real,
    size text
);

alter table users
    owner to postgres;

create unique index if not exists users_id_uindex
    on users (id);
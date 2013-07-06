-- Схема для задания по транзакциям

-- Информация и сдаче крови в банк
CREATE TABLE donation (
    id           integer primary key autoincrement not null,
    donate_on    date,
    donor_name   text,
    donor_gender text,
    blood_type   text
);

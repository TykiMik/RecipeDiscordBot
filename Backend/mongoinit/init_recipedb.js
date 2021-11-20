db.createCollection("recipes")
db.createCollection("banned_users");
db.createCollection("admins")

admins = [
    {
        "name": "admin",
        "password": "$argon2id$v=19$m=102400,t=2,p=8$JKm0bmKcReBDRv9tKIh3BQ$wF/XtlwsP1vF91ENA29hlQ"
    }
];

db.admins.insertMany(admins);
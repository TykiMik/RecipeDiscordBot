db.createUser({
    user: "botuser",
    pwd: "botpass",
    roles: [ { role: "readWrite", db: "recipedb"} ]
});

db.createUser({
    user: "flaskuser",
    pwd: "flaskpass",
    roles: [ { role: "readWrite", db: "recipedb"} ]
});
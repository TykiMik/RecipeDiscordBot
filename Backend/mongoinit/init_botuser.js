db.createUser({
    user: "botuser",
    pwd: "botpass",
    roles: [ { role: "readWrite", db: "recipedb"} ]
});

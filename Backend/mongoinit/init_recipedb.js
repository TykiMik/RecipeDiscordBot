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

recipes = [
    {
        "creator": "Esmee Williams",
        "creator_id": "unknown",
        "name": "Mashed potatoes",
        "content": "2 pounds baking potatoes, peeled and quartered\n2 tablespoons butter\n1 cup milk\nsalt and pepper to taste\nBring a pot of salted water to a boil. Add potatoes and cook until tender but still firm, about 15 minutes; drain.\nIn a small saucepan heat butter and milk over low heat until butter is melted. Using a potato masher or electric beater, slowly blend milk mixture into potatoes until smooth and creamy. Season with salt and pepper to taste.",
        "tags": ["potato", "mash", "side"],
        "request_count": 415,
        "ratings": [5,4,4,3,5,4,1,5,2,4,5],
        "creation_date": new Date(2021, 11, 19, 5, 41, 14, 4)
    }
];

db.recipes.insertMany(recipes);
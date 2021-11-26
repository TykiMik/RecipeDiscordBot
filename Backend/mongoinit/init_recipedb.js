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
        "creator": "Esmee Williams#4151",
        "creator_id": "912742312453476423",
        "name": "Mashed potatoes",
        "content": "2 pounds baking potatoes, peeled and quartered\n2 tablespoons butter\n1 cup milk\nsalt and pepper to taste\nBring a pot of salted water to a boil. Add potatoes and cook until tender but still firm, about 15 minutes; drain.\nIn a small saucepan heat butter and milk over low heat until butter is melted. Using a potato masher or electric beater, slowly blend milk mixture into potatoes until smooth and creamy. Season with salt and pepper to taste.",
        "tags": ["potato", "mash", "side"],
        "request_count": 415,
        "ratings": [5,4,4,3,5,4,1,5,2,4,5],
        "creation_date": new Date(2021, 11, 19, 5, 41, 14, 4)
    },
        {
        "creator": "John Tucker#6612",
        "creator_id": "912742342453476423",
        "name": "Sausage pasta bake",
        "content": "To make the ragu, heat the oil in a large shallow pan or flameproof casserole. Squeeze the sausagemeat from its skins in small balls straight into the pan. Sizzle for 10 mins until browned (don’t worry if the meat breaks up). Add the garlic and sizzle for another minute until starting to turn golden, then stir in the chilli flakes, if using, the tomato purée and vinegar. Tip in the tomatoes and bring to a simmer. Reduce the heat to low and bubble for 30 mins.\nSTEP 2\nMeanwhile, make the white sauce. Melt the butter in a saucepan and stir in the flour to make a loose paste. Sizzle for a minute, then gradually whisk in the milk. Simmer gently for 10 mins, whisking occasionally to ensure the sauce stays smooth. Season and whisk in the parmesan. Remove from the heat and set aside.\nSTEP 3\nCook the pasta in a large saucepan of boiling water for 9 mins, or a minute less than pack instructions. Drain and return to the pan. Scrape most of the white sauce into the pasta and stir to coat. Tip in most of the ragu and most of the mozzarella and stir until just combined. Pour the pasta mixture into a large baking dish and spoon over the remaining white sauce and ragu. Dot with the rest of the mozzarella and sprinkle with extra parmesan. Leave to cool completely, then wrap and chill for up to a day, or freeze for up to two months. Defrost in the fridge for 24 hrs before baking.\nSTEP 4\nHeat the oven to 190C/170C fan/gas 5. Bake for 25-30 mins until the top is slightly crisp at the edges and the cheese is melted. Leave to rest for 5-10 mins, then take the baking dish straight to the table for people to scoop onto their plates.",
        "tags": ["pasta", "sausage", "oven", "one-pan"],
        "request_count": 1091,
        "ratings": [3,3,4,1,4,2,1,2,3,2,1,1,5,4,1,4,2,1],
        "creation_date": new Date(2021, 11, 21, 9, 41, 44, 9)
    }
];

db.recipes.insertMany(recipes);
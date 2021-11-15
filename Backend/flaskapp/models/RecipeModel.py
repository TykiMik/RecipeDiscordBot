from fastapi.encoders import jsonable_encoder


class RecipeModel:
    def __init__(self, _id, creator, creator_id, name, content, tags, request_count, ratings):
        self.object_id = str(_id),
        self.creator = creator,
        self.creator_id = creator_id,
        self.name = name,
        self.content = content,
        self.tags = tags,
        self.request_count = request_count,
        self.ratings = ratings

    def to_json(self):
        return jsonable_encoder(self, exclude_none=True)
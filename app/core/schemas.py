from pydantic import BaseModel as PydanticBaseModel


class BaseModel(PydanticBaseModel):

    def to_dict(self):
        return {c: getattr(self, c) for c in self.model_fields_set}

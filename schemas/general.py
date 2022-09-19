from typing import Any
from db.models import Color, ItemEffect
import strawberry

ColorType: Any = strawberry.enum(Color, name="Color")
ItemEffectType: Any = strawberry.enum(ItemEffect, name="ItemEffect")

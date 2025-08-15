from sqlalchemy import Column, String, DateTime, Float, ForeignKey, Enum, Text
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
import uuid
import enum

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(100))
    email = Column(String(100))
    password = Column(String(128))
    created = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class UnitEnum(enum.Enum):
    GRAM = "g"
    MILLIGRAM = "mg"
    MICROGRAM = "µg"
    KILOGRAM = "kg"

    KILOCALORIE = "kcal"

    LITER = "l"
    MILLILITER = "ml"

    TEASPOON = "tsp"
    TABLESPOON = "tbsp"
    CUP = "cup"

    OUNCE = "oz"
    FLUID_OUNCE = "fl oz"
    POUND = "lb"

    PIECE = "pc"
    SLICE = "slice"
    SERVING = "serving"

    INTERNATIONAL_UNIT = "IU"

class FoodTypeEnum(enum.Enum):
    FOOD = "food"
    DISH = "dish"
    MEAL = "meal"

class Food(Base):
    __tablename__ = "food"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    type = Column(Enum(FoodTypeEnum, name="food_type_enum"), default=FoodTypeEnum.FOOD, nullable=False)
    name = Column(String(100), default="untitled", nullable=False)
    description = Column(Text)
    recipe = Column(Text)
    created = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    nutrients = relationship("FoodNutrient", back_populates="food")

class Nutrient(Base):
    __tablename__ = "nutrients"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name = Column(String(50), default="untitled", nullable=False)
    unit = Column(Enum(UnitEnum, name="unit_enum"), default=UnitEnum.GRAM, nullable=False)
    created = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    food = relationship("FoodNutrient", back_populates="nutrient")

class FoodNutrient(Base):
    __tablename__ = "food_nutrients"

    food_id = Column(UUID(as_uuid=True), ForeignKey("food.id"), primary_key=True, nullable=False)
    nutrient_id = Column(UUID(as_uuid=True), ForeignKey("nutrients.id"), primary_key=True, nullable=False)
    amount = Column(Float, default=0, nullable=False)

    food = relationship("Food", back_populates="nutrients")
    nutrient = relationship("Nutrient", back_populates="food")
from sqlalchemy import (Column, DateTime, ForeignKey, Integer, Numeric,
                        SmallInteger, String, func)
from sqlalchemy.orm import relationship

from infrastructure.database import Base


class Region(Base):
    __tablename__ = "regions"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    climate = Column(String)

    greenhouse = relationship(
        "Greenhouse", back_populates="region", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Region(id={self.id}, name='{self.name}', climate='{self.climate}')>"


class Greenhouse(Base):
    __tablename__ = "greenhouses"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    region_id = Column(Integer, ForeignKey("regions.id", ondelete="SET NULL"))
    state = Column(SmallInteger, default=0)  # 0-normal, 1-warning, 2-danger
    updated_at = Column(DateTime, server_default=func.now())

    region = relationship("Region", back_populates="greenhouse")
    metering = relationship(
        "Metering", back_populates="greenhouse", cascade="all, delete-orphan"
    )
    status_history = relationship(
        "StatusHistory", back_populates="greenhouse", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Greenhouse(id={self.id}, name='{self.name}', state={self.state})>"


class MeteringType(Base):
    __tablename__ = "metering_types"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)  # temperature, humidity, ph

    metering = relationship(
        "Metering", back_populates="metering_type", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<MeteringType(id={self.id}, name='{self.name}')>"


class Metering(Base):
    __tablename__ = "meterings"

    id = Column(Integer, primary_key=True)
    greenhouse_id = Column(Integer, ForeignKey("greenhouses.id", ondelete="CASCADE"))
    metering_type_id = Column(
        Integer, ForeignKey("metering_types.id", ondelete="CASCADE")
    )
    updated_at = Column(DateTime, nullable=False)
    value = Column(Numeric)
    created_at = Column(DateTime, server_default=func.now())

    greenhouse = relationship("Greenhouse", back_populates="metering")
    metering_type = relationship("MeteringType", back_populates="metering")

    def __repr__(self):
        return (
            f"<Metering(id={self.id}, greenhouse_id={self.greenhouse_id}, "
            f"type_id={self.metering_type_id}, value={self.value})>"
        )


class StatusHistory(Base):
    __tablename__ = "status_history"

    id = Column(Integer, primary_key=True)
    greenhouse_id = Column(Integer, ForeignKey("greenhouses.id", ondelete="CASCADE"))
    old_state = Column(SmallInteger)
    new_state = Column(SmallInteger)
    changed_at = Column(DateTime, server_default=func.now())

    greenhouse = relationship("Greenhouse", back_populates="status_history")

    def __repr__(self):
        return (
            f"<StatusHistory(id={self.id}, greenhouse_id={self.greenhouse_id}, "
            f"{self.old_state}->{self.new_state}, changed_at={self.changed_at})>"
        )

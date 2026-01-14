"""SQLAlchemy ORM models matching the PostgreSQL database schema."""
from sqlalchemy import (
    Column, Integer, String, Date, DateTime, Boolean, Text,
    ForeignKey, CheckConstraint, UniqueConstraint, func
)
from sqlalchemy.orm import relationship
from app.database import Base


class Season(Base):
    """Tournament season model."""
    __tablename__ = "seasons"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    tournaments = relationship("Tournament", back_populates="season", cascade="all, delete-orphan")
    
    __table_args__ = (
        CheckConstraint('end_date IS NULL OR end_date >= start_date', name='valid_season_dates'),
    )


class Tournament(Base):
    """Tournament model."""
    __tablename__ = "tournaments"
    
    id = Column(Integer, primary_key=True, index=True)
    season_id = Column(Integer, ForeignKey("seasons.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(150), nullable=False)
    tournament_date = Column(Date, nullable=False)
    location = Column(String(200))
    format = Column(String(50))
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    season = relationship("Season", back_populates="tournaments")
    matches = relationship("Match", back_populates="tournament", cascade="all, delete-orphan")
    
    __table_args__ = (
        CheckConstraint('tournament_date <= CURRENT_DATE', name='valid_tournament_date'),
    )


class Player(Base):
    """Player model."""
    __tablename__ = "players"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True)
    registration_date = Column(Date, nullable=False, server_default=func.current_date())
    active = Column(Boolean, nullable=False, default=True)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    matches_as_player1 = relationship("Match", foreign_keys="Match.player1_id", back_populates="player1")
    matches_as_player2 = relationship("Match", foreign_keys="Match.player2_id", back_populates="player2")
    games_won = relationship("Game", back_populates="winner")


class DeckArchetype(Base):
    """Deck archetype model."""
    __tablename__ = "deck_archetypes"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    color_identity = Column(String(10))
    archetype_type = Column(String(50))
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    matches_as_deck1 = relationship("Match", foreign_keys="Match.player1_deck_id", back_populates="player1_deck")
    matches_as_deck2 = relationship("Match", foreign_keys="Match.player2_deck_id", back_populates="player2_deck")


class Match(Base):
    """Match model (best-of-3)."""
    __tablename__ = "matches"
    
    id = Column(Integer, primary_key=True, index=True)
    tournament_id = Column(Integer, ForeignKey("tournaments.id", ondelete="CASCADE"), nullable=False)
    player1_id = Column(Integer, ForeignKey("players.id", ondelete="RESTRICT"), nullable=False)
    player2_id = Column(Integer, ForeignKey("players.id", ondelete="RESTRICT"), nullable=False)
    player1_deck_id = Column(Integer, ForeignKey("deck_archetypes.id", ondelete="RESTRICT"), nullable=False)
    player2_deck_id = Column(Integer, ForeignKey("deck_archetypes.id", ondelete="RESTRICT"), nullable=False)
    round_number = Column(Integer)
    match_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    match_status = Column(String(20), nullable=False, default='COMPLETED')
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    tournament = relationship("Tournament", back_populates="matches")
    player1 = relationship("Player", foreign_keys=[player1_id], back_populates="matches_as_player1")
    player2 = relationship("Player", foreign_keys=[player2_id], back_populates="matches_as_player2")
    player1_deck = relationship("DeckArchetype", foreign_keys=[player1_deck_id], back_populates="matches_as_deck1")
    player2_deck = relationship("DeckArchetype", foreign_keys=[player2_deck_id], back_populates="matches_as_deck2")
    games = relationship("Game", back_populates="match", cascade="all, delete-orphan")
    
    __table_args__ = (
        CheckConstraint('player1_id != player2_id', name='different_players'),
        CheckConstraint("match_status IN ('IN_PROGRESS', 'COMPLETED', 'CANCELLED')", name='valid_match_status'),
        CheckConstraint('round_number IS NULL OR round_number > 0', name='valid_round_number'),
    )


class Game(Base):
    """Individual game model within a match."""
    __tablename__ = "games"
    
    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(Integer, ForeignKey("matches.id", ondelete="CASCADE"), nullable=False)
    game_number = Column(Integer, nullable=False)
    winner_id = Column(Integer, ForeignKey("players.id", ondelete="RESTRICT"), nullable=False)
    game_result = Column(String(10), nullable=False)
    duration_minutes = Column(Integer)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    match = relationship("Match", back_populates="games")
    winner = relationship("Player", back_populates="games_won")
    
    __table_args__ = (
        CheckConstraint('game_number BETWEEN 1 AND 3', name='valid_game_number'),
        CheckConstraint("game_result IN ('WIN', 'DRAW')", name='valid_game_result'),
        CheckConstraint('duration_minutes IS NULL OR duration_minutes > 0', name='valid_duration'),
        UniqueConstraint('match_id', 'game_number', name='unique_game_per_match'),
    )

"""Pydantic schemas for request/response validation."""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import date, datetime


# ============================================================================
# SEASON SCHEMAS
# ============================================================================

class SeasonBase(BaseModel):
    """Base schema for Season."""
    name: str = Field(..., max_length=100, description="Season name")
    start_date: date = Field(..., description="Season start date")
    end_date: Optional[date] = Field(None, description="Season end date")
    description: Optional[str] = Field(None, description="Season description")


class SeasonCreate(SeasonBase):
    """Schema for creating a season."""
    pass


class SeasonUpdate(BaseModel):
    """Schema for updating a season."""
    name: Optional[str] = Field(None, max_length=100)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    description: Optional[str] = None


class Season(SeasonBase):
    """Schema for Season response."""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================================
# TOURNAMENT SCHEMAS
# ============================================================================

class TournamentBase(BaseModel):
    """Base schema for Tournament."""
    season_id: int = Field(..., description="Season ID")
    name: str = Field(..., max_length=150, description="Tournament name")
    tournament_date: date = Field(..., description="Tournament date")
    location: Optional[str] = Field(None, max_length=200, description="Tournament location")
    format: Optional[str] = Field(None, max_length=50, description="MTG format (Standard, Modern, etc.)")
    description: Optional[str] = Field(None, description="Tournament description")


class TournamentCreate(TournamentBase):
    """Schema for creating a tournament."""
    pass


class TournamentUpdate(BaseModel):
    """Schema for updating a tournament."""
    season_id: Optional[int] = None
    name: Optional[str] = Field(None, max_length=150)
    tournament_date: Optional[date] = None
    location: Optional[str] = Field(None, max_length=200)
    format: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None


class Tournament(TournamentBase):
    """Schema for Tournament response."""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================================
# PLAYER SCHEMAS
# ============================================================================

class PlayerBase(BaseModel):
    """Base schema for Player."""
    name: str = Field(..., max_length=100, description="Player name")
    email: Optional[str] = Field(None, max_length=150, description="Player email")
    active: bool = Field(True, description="Whether the player is active")
    notes: Optional[str] = Field(None, description="Player notes")


class PlayerCreate(PlayerBase):
    """Schema for creating a player."""
    pass


class PlayerUpdate(BaseModel):
    """Schema for updating a player."""
    name: Optional[str] = Field(None, max_length=100)
    email: Optional[str] = Field(None, max_length=150)
    active: Optional[bool] = None
    notes: Optional[str] = None


class Player(PlayerBase):
    """Schema for Player response."""
    id: int
    registration_date: date
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================================
# DECK ARCHETYPE SCHEMAS
# ============================================================================

class DeckArchetypeBase(BaseModel):
    """Base schema for Deck Archetype."""
    name: str = Field(..., max_length=100, description="Deck archetype name")
    color_identity: Optional[str] = Field(None, max_length=10, description="WUBRG color combination")
    archetype_type: Optional[str] = Field(None, max_length=50, description="Archetype type (Aggro, Control, etc.)")
    description: Optional[str] = Field(None, description="Deck description")


class DeckArchetypeCreate(DeckArchetypeBase):
    """Schema for creating a deck archetype."""
    pass


class DeckArchetypeUpdate(BaseModel):
    """Schema for updating a deck archetype."""
    name: Optional[str] = Field(None, max_length=100)
    color_identity: Optional[str] = Field(None, max_length=10)
    archetype_type: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None


class DeckArchetype(DeckArchetypeBase):
    """Schema for Deck Archetype response."""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================================
# GAME SCHEMAS
# ============================================================================

class GameBase(BaseModel):
    """Base schema for Game."""
    game_number: int = Field(..., ge=1, le=3, description="Game number (1-3)")
    winner_id: int = Field(..., description="Player ID who won the game")
    game_result: str = Field(..., description="Game result (WIN or DRAW)")
    duration_minutes: Optional[int] = Field(None, ge=1, description="Game duration in minutes")
    notes: Optional[str] = Field(None, description="Game notes")
    
    @field_validator('game_result')
    @classmethod
    def validate_game_result(cls, v):
        if v not in ['WIN', 'DRAW']:
            raise ValueError('game_result must be WIN or DRAW')
        return v


class GameCreate(GameBase):
    """Schema for creating a game."""
    pass


class GameCreateWithoutMatch(GameBase):
    """Schema for creating a game without match_id (used in batch)."""
    pass


class Game(GameBase):
    """Schema for Game response."""
    id: int
    match_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================================
# MATCH SCHEMAS
# ============================================================================

class MatchBase(BaseModel):
    """Base schema for Match."""
    tournament_id: int = Field(..., description="Tournament ID")
    player1_id: int = Field(..., description="Player 1 ID")
    player2_id: int = Field(..., description="Player 2 ID")
    player1_deck_id: int = Field(..., description="Player 1 deck archetype ID")
    player2_deck_id: int = Field(..., description="Player 2 deck archetype ID")
    round_number: Optional[int] = Field(None, ge=1, description="Round number")
    match_status: str = Field('COMPLETED', description="Match status")
    notes: Optional[str] = Field(None, description="Match notes")
    
    @field_validator('match_status')
    @classmethod
    def validate_match_status(cls, v):
        if v not in ['IN_PROGRESS', 'COMPLETED', 'CANCELLED']:
            raise ValueError('match_status must be IN_PROGRESS, COMPLETED, or CANCELLED')
        return v
    
    @field_validator('player2_id')
    @classmethod
    def validate_different_players(cls, v, info):
        if 'player1_id' in info.data and v == info.data['player1_id']:
            raise ValueError('player1_id and player2_id must be different')
        return v


class MatchCreate(MatchBase):
    """Schema for creating a match."""
    pass


class MatchUpdate(BaseModel):
    """Schema for updating a match."""
    tournament_id: Optional[int] = None
    player1_id: Optional[int] = None
    player2_id: Optional[int] = None
    player1_deck_id: Optional[int] = None
    player2_deck_id: Optional[int] = None
    round_number: Optional[int] = Field(None, ge=1)
    match_status: Optional[str] = None
    notes: Optional[str] = None


class Match(MatchBase):
    """Schema for Match response."""
    id: int
    match_date: datetime
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class MatchWithGames(Match):
    """Schema for Match response with games."""
    games: List[Game] = []
    
    class Config:
        from_attributes = True


# ============================================================================
# BATCH INSERT SCHEMAS
# ============================================================================

class MatchWithGamesCreate(MatchBase):
    """Schema for creating a match with games in batch."""
    games: List[GameCreateWithoutMatch] = Field(
        ..., 
        min_length=1,
        max_length=3,
        description="Games in the match (1-3 games)"
    )


class BatchMatchCreate(BaseModel):
    """Schema for batch match creation."""
    matches: List[MatchWithGamesCreate] = Field(
        ..., 
        min_length=1,
        description="List of matches with games to create"
    )


class BatchMatchResponse(BaseModel):
    """Schema for batch match creation response."""
    success_count: int = Field(..., description="Number of successfully created matches")
    failed_count: int = Field(..., description="Number of failed matches")
    created_match_ids: List[int] = Field(..., description="IDs of successfully created matches")
    errors: List[dict] = Field(default=[], description="Errors for failed matches")


# ============================================================================
# STATISTICS SCHEMAS
# ============================================================================

class PlayerStatistics(BaseModel):
    """Schema for player statistics."""
    player_id: int
    player_name: str
    total_matches: int
    matches_won: int
    matches_drawn: int
    matches_lost: int
    win_rate_percentage: Optional[float]
    decks_played: int
    tournaments_played: int


class DeckStatistics(BaseModel):
    """Schema for deck statistics."""
    deck_id: int
    deck_name: str
    color_identity: Optional[str]
    archetype_type: Optional[str]
    total_matches: int
    matches_won: int
    matches_drawn: int
    matches_lost: int
    win_rate_percentage: Optional[float]
    unique_players: int
    tournaments_played: int


class DeckMatchup(BaseModel):
    """Schema for deck matchup statistics."""
    deck_a_id: int
    deck_a_name: str
    deck_b_id: int
    deck_b_name: str
    total_matches: int
    deck_a_wins: int
    draws: int
    deck_a_losses: int
    deck_a_win_rate_percentage: Optional[float]
    deck_b_win_rate_percentage: Optional[float]


class SeasonStandings(BaseModel):
    """Schema for season standings."""
    season_id: int
    season_name: str
    player_id: int
    player_name: str
    matches_played: int
    wins: int
    draws: int
    losses: int
    points: int
    
    class Config:
        from_attributes = True


# ============================================================================
# ERROR SCHEMAS
# ============================================================================

class ErrorDetail(BaseModel):
    """Schema for error details."""
    field: Optional[str] = None
    message: str


class ErrorResponse(BaseModel):
    """Schema for error responses."""
    error: str
    detail: Optional[str] = None
    errors: Optional[List[ErrorDetail]] = None

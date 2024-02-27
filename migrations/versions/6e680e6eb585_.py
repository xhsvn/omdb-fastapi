"""empty message

Revision ID: 6e680e6eb585
Revises: 
Create Date: 2024-02-22 10:30:24.584861

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6e680e6eb585'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('movies',
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('year', sa.Integer(), nullable=True),
    sa.Column('rated', sa.String(), nullable=True),
    sa.Column('released', sa.String(), nullable=True),
    sa.Column('runtime', sa.String(), nullable=True),
    sa.Column('genre', sa.String(), nullable=True),
    sa.Column('director', sa.String(), nullable=True),
    sa.Column('writer', sa.String(), nullable=True),
    sa.Column('actors', sa.String(), nullable=True),
    sa.Column('plot', sa.String(), nullable=True),
    sa.Column('language', sa.String(), nullable=True),
    sa.Column('country', sa.String(), nullable=True),
    sa.Column('awards', sa.String(), nullable=True),
    sa.Column('poster', sa.String(), nullable=True),
    sa.Column('metascore', sa.String(), nullable=True),
    sa.Column('imdb_rating', sa.String(), nullable=True),
    sa.Column('imdb_votes', sa.String(), nullable=True),
    sa.Column('imdb_id', sa.String(), nullable=True),
    sa.Column('dvd', sa.String(), nullable=True),
    sa.Column('box_office', sa.String(), nullable=True),
    sa.Column('production', sa.String(), nullable=True),
    sa.Column('website', sa.String(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_index(op.f('ix_movies_created_at'), 'movies', ['created_at'], unique=False)
    op.create_index(op.f('ix_movies_updated_at'), 'movies', ['updated_at'], unique=False)
    op.create_table('ratings',
    sa.Column('source', sa.String(), nullable=False),
    sa.Column('value', sa.String(), nullable=False),
    sa.Column('movie_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ratings_created_at'), 'ratings', ['created_at'], unique=False)
    op.create_index(op.f('ix_ratings_updated_at'), 'ratings', ['updated_at'], unique=False)
    op.create_table('users',
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_index(op.f('ix_users_created_at'), 'users', ['created_at'], unique=False)
    op.create_index(op.f('ix_users_updated_at'), 'users', ['updated_at'], unique=False)
    op.create_table('movie_imports',
    sa.Column('status', sa.Enum('FETCHING', 'FETCHED', 'NOT_FOUND', 'ERROR', name='importstatus'), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('movie_id', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['movie_id'], ['movies.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_index(op.f('ix_movie_imports_created_at'), 'movie_imports', ['created_at'], unique=False)
    op.create_index(op.f('ix_movie_imports_updated_at'), 'movie_imports', ['updated_at'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_movie_imports_updated_at'), table_name='movie_imports')
    op.drop_index(op.f('ix_movie_imports_created_at'), table_name='movie_imports')
    op.drop_table('movie_imports')
    op.drop_index(op.f('ix_users_updated_at'), table_name='users')
    op.drop_index(op.f('ix_users_created_at'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_ratings_updated_at'), table_name='ratings')
    op.drop_index(op.f('ix_ratings_created_at'), table_name='ratings')
    op.drop_table('ratings')
    op.drop_index(op.f('ix_movies_updated_at'), table_name='movies')
    op.drop_index(op.f('ix_movies_created_at'), table_name='movies')
    op.drop_table('movies')
    # ### end Alembic commands ###

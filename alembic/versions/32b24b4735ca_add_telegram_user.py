"""add_telegram_user

Revision ID: 32b24b4735ca
Revises: fed4ec86cb2f
Create Date: 2022-03-24 23:57:20.492738

"""
from alembic import op
import sqlmodel
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '32b24b4735ca'
down_revision = 'fed4ec86cb2f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('telegramuser',
    sa.Column('is_blocked', sa.Boolean(), nullable=True),
    sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=True),
    sa.Column('is_bot', sa.Boolean(), nullable=False),
    sa.Column('first_name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('last_name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('username', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('language_code', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user_job_title', 'user_id',
               existing_type=postgresql.UUID(),
               nullable=False)
    op.alter_column('user_job_title', 'job_title_id',
               existing_type=postgresql.UUID(),
               nullable=False)
    op.alter_column('user', 'id',
               existing_type=postgresql.UUID(),
               nullable=False)
    op.alter_column('subject', 'id',
               existing_type=postgresql.UUID(),
               nullable=False)
    op.alter_column('stage_lesson', 'stage_id',
               existing_type=postgresql.UUID(),
               nullable=False)
    op.alter_column('stage_lesson', 'lesson_id',
               existing_type=postgresql.UUID(),
               nullable=False)
    op.drop_table('telegramuser')
    # ### end Alembic commands ###
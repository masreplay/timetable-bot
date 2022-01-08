"""init

Revision ID: 888317e7c470
Revises: 
Create Date: 2022-01-08 00:30:19.082532

"""
from alembic import op
import sqlmodel
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '888317e7c470'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('building',
    sa.Column('lng', sa.Float(), nullable=True),
    sa.Column('lat', sa.Float(), nullable=True),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('color', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_building_name'), 'building', ['name'], unique=False)
    op.create_table('department',
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('en_name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('abbr', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('vision', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('floor',
    sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('job_title',
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('en_name', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('type', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('period',
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('start_time', sa.Time(), nullable=False),
    sa.Column('end_time', sa.Time(), nullable=False),
    sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('role',
    sa.Column('permissions', sa.JSON(), nullable=True),
    sa.Column('ar_name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('en_name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('branch',
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('en_name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('abbr', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('vision', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('department_id', sqlmodel.sql.sqltypes.GUID(), nullable=True),
    sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['department_id'], ['department.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('room',
    sa.Column('type', sa.Enum('classroom', 'employee', 'other', name='roomtype'), nullable=True),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('color', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('building_id', sqlmodel.sql.sqltypes.GUID(), nullable=True),
    sa.Column('floor_id', sqlmodel.sql.sqltypes.GUID(), nullable=True),
    sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['building_id'], ['building.id'], ),
    sa.ForeignKeyConstraint(['floor_id'], ['floor.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_room_name'), 'room', ['name'], unique=False)
    op.create_table('user',
    sa.Column('gender', sa.Enum('male', 'female', name='usergender'), nullable=True),
    sa.Column('scrape_from', sa.Enum('uot', 'asc', 'uot_asc', name='userscrapefrom'), nullable=True),
    sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('color', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('en_name', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('email', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('uot_url', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('image', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('asc_job_title', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('asc_name', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('role_id', sqlmodel.sql.sqltypes.GUID(), nullable=True),
    sa.Column('hashed_password', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_user_en_name'), 'user', ['en_name'], unique=False)
    op.create_index(op.f('ix_user_name'), 'user', ['name'], unique=False)
    op.create_table('stage',
    sa.Column('shift', sa.Enum('morning', 'evening', name='collageshifts'), nullable=True),
    sa.Column('level', sa.Integer(), nullable=False),
    sa.Column('branch_id', sqlmodel.sql.sqltypes.GUID(), nullable=True),
    sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['branch_id'], ['branch.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('shift', 'level', 'branch_id', name='branch_stage')
    )
    op.create_index(op.f('ix_stage_level'), 'stage', ['level'], unique=False)
    op.create_table('user_job_title',
    sa.Column('job_title_id', sqlmodel.sql.sqltypes.GUID(), nullable=True),
    sa.Column('user_id', sqlmodel.sql.sqltypes.GUID(), nullable=True),
    sa.ForeignKeyConstraint(['job_title_id'], ['job_title.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('job_title_id', 'user_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_job_title')
    op.drop_index(op.f('ix_stage_level'), table_name='stage')
    op.drop_table('stage')
    op.drop_index(op.f('ix_user_name'), table_name='user')
    op.drop_index(op.f('ix_user_en_name'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_room_name'), table_name='room')
    op.drop_table('room')
    op.drop_table('branch')
    op.drop_table('role')
    op.drop_table('period')
    op.drop_table('job_title')
    op.drop_table('floor')
    op.drop_table('department')
    op.drop_index(op.f('ix_building_name'), table_name='building')
    op.drop_table('building')
    # ### end Alembic commands ###
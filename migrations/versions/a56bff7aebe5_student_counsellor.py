"""student-counsellor

Revision ID: a56bff7aebe5
Revises: 
Create Date: 2020-12-05 16:04:58.463916

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a56bff7aebe5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Counsellor',
    sa.Column('c_email_id', sa.String(length=120), nullable=False),
    sa.Column('f_name', sa.String(length=250), nullable=False),
    sa.Column('l_name', sa.String(length=250), nullable=False),
    sa.Column('dept_id', sa.String(length=5), nullable=True),
    sa.ForeignKeyConstraint(['dept_id'], ['Department.dept_id'], ),
    sa.PrimaryKeyConstraint('c_email_id')
    )
    op.create_table('Credentials',
    sa.Column('email_id', sa.String(length=120), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.Column('type', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('email_id')
    )
    op.create_table('Department',
    sa.Column('dept_id', sa.String(length=5), nullable=False),
    sa.Column('dept_name', sa.String(length=20), nullable=False),
    sa.Column('hod_email_id', sa.String(length=120), nullable=True),
    sa.ForeignKeyConstraint(['hod_email_id'], ['Counsellor.c_email_id'], ),
    sa.PrimaryKeyConstraint('dept_id')
    )
    op.create_table('Student',
    sa.Column('s_email_id', sa.String(length=120), nullable=False),
    sa.Column('usn', sa.String(length=10), nullable=False),
    sa.Column('f_name', sa.String(length=250), nullable=False),
    sa.Column('l_name', sa.String(length=250), nullable=False),
    sa.Column('c_email_id', sa.String(length=120), nullable=True),
    sa.ForeignKeyConstraint(['c_email_id'], ['Counsellor.c_email_id'], ),
    sa.PrimaryKeyConstraint('s_email_id'),
    sa.UniqueConstraint('usn')
    )
    op.create_table('Parent',
    sa.Column('p_email_id', sa.String(length=120), nullable=False),
    sa.Column('f_name', sa.String(length=250), nullable=False),
    sa.Column('l_name', sa.String(length=250), nullable=False),
    sa.Column('c_email_id', sa.String(length=120), nullable=True),
    sa.Column('s_email_id', sa.String(length=120), nullable=True),
    sa.ForeignKeyConstraint(['c_email_id'], ['Counsellor.c_email_id'], ),
    sa.ForeignKeyConstraint(['s_email_id'], ['Student.s_email_id'], ),
    sa.PrimaryKeyConstraint('p_email_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Parent')
    op.drop_table('Student')
    op.drop_table('Department')
    op.drop_table('Credentials')
    op.drop_table('Counsellor')
    # ### end Alembic commands ###

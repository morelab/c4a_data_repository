"""1 real test

Revision ID: cf3eac17c4a1
Revises: 
Create Date: 2017-11-02 09:15:28.276292

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.schema import Sequence, CreateSequence, DropSequence
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = 'cf3eac17c4a1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    op.execute(CreateSequence(Sequence('source_evidence_id_seq', schema='city4age_ar')))
    op.create_table('source_evidence',
    sa.Column('id', sa.Integer(), server_default=sa.text(u"nextval('city4age_ar.source_evidence_id_seq')"), nullable=False, primary_key=True),
    sa.Column('text_evidence', sa.String(255), nullable=True),
    sa.Column('creation_date', sqlalchemy_utils.types.arrow.ArrowType(timezone=True), server_default=sa.text(u"TIMEZONE('utc', CURRENT_TIMESTAMP)"), nullable=True),
    schema='city4age_ar'
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('source_evidence', schema='city4age_ar')
    op.execute(DropSequence(Sequence('source_evidence_id_seq', schema='city4age_ar')))
    # ### end Alembic commands ###
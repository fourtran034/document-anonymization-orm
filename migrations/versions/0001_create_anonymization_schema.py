"""Create the document anonymization schema."""

import sqlalchemy as sa
from alembic import op

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'documents',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('reference', sa.String(length=100), nullable=False, unique=True),
        sa.Column('sha256', sa.String(length=64), nullable=False),
    )
    op.create_table(
        'anonymization_jobs',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('document_id', sa.Integer(), sa.ForeignKey('documents.id'), nullable=False),
        sa.Column('status', sa.Enum('draft', 'in_review', 'completed', name='job_status',
                                    native_enum=False, create_constraint=True), nullable=False),
    )
    op.create_index('ix_anonymization_jobs_document_id', 'anonymization_jobs', ['document_id'])
    op.create_table(
        'replacement_candidates',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('job_id', sa.Integer(), sa.ForeignKey('anonymization_jobs.id', ondelete='CASCADE'),
                  nullable=False),
        sa.Column('location', sa.String(length=120), nullable=False),
        sa.Column('category', sa.String(length=40), nullable=False),
        sa.Column('token', sa.String(length=80), nullable=False),
        sa.Column('approved', sa.Boolean(), nullable=True),
    )
    op.create_index('ix_replacement_candidates_job_id', 'replacement_candidates', ['job_id'])


def downgrade() -> None:
    op.drop_index('ix_replacement_candidates_job_id', table_name='replacement_candidates')
    op.drop_table('replacement_candidates')
    op.drop_index('ix_anonymization_jobs_document_id', table_name='anonymization_jobs')
    op.drop_table('anonymization_jobs')
    op.drop_table('documents')

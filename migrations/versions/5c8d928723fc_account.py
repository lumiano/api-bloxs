"""person

Revision ID: 5c8d928723fc
Revises: 3a2d81fc3285
Create Date: 2023-12-17 18:36:40.869539

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "5c8d928723fc"
down_revision = "3a2d81fc3285"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "account",
        sa.Column(
            "balance",
            sa.Numeric(precision=10, scale=2),
            nullable=False,
            comment="Balance",
        ),
        sa.Column(
            "daily_withdrawal_limit",
            sa.Numeric(precision=10, scale=2),
            nullable=False,
            comment="Daily withdrawal limit",
        ),
        sa.Column(
            "account_type",
            sa.Enum("CURRENT_ACCOUNT", "SAVINGS_ACCOUNT", name="accounttypeenum"),
            nullable=False,
            comment="Account type",
        ),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False, comment="ID"),
        sa.Column(
            "creation_date",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
            comment="Creation date",
        ),
        sa.Column(
            "update_date",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
            comment="Update date",
        ),
        sa.Column("is_active", sa.Boolean(), nullable=False, comment="Active flag"),
        sa.CheckConstraint("balance >= 0", name="ck_balance"),
        sa.CheckConstraint(
            "daily_withdrawal_limit >= 0", name="ck_daily_withdrawal_limit"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id", name="uq_account_id"),
    )
    with op.batch_alter_table("account", schema=None) as batch_op:
        batch_op.create_index(
            "idx_account_id_account_type", ["id", "account_type"], unique=False
        )
        batch_op.create_index("idx_person_id", ["id"], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("account", schema=None) as batch_op:
        batch_op.drop_index("idx_person_id")
        batch_op.drop_index("idx_account_id_account_type")

    op.drop_table("account")
    # ### end Alembic commands ###

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "20250926_0001_initial"
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("username", sa.String(length=50), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
    )
    op.create_index("ix_users_id", "users", ["id"], unique=False)
    op.create_index("ix_users_username", "users", ["username"], unique=True)
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    op.create_table(
        "categories",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("name", "user_id", name="uq_category_name_user"),
    )
    op.create_index("ix_categories_id", "categories", ["id"], unique=False)
    op.create_index("ix_categories_name", "categories", ["name"], unique=False)

    op.create_table(
        "expenses",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("amount", sa.Float(), nullable=False),
        sa.Column("currency", sa.String(length=10), nullable=False, server_default="USD"),
        sa.Column("category", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(length=500), nullable=True),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_expenses_id", "expenses", ["id"], unique=False)
    op.create_index("ix_expenses_user_id", "expenses", ["user_id"], unique=False)
    op.create_index("ix_expenses_user_date", "expenses", ["user_id", "date"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_expenses_user_date", table_name="expenses")
    op.drop_index("ix_expenses_user_id", table_name="expenses")
    op.drop_index("ix_expenses_id", table_name="expenses")
    op.drop_table("expenses")

    op.drop_index("ix_categories_name", table_name="categories")
    op.drop_index("ix_categories_id", table_name="categories")
    op.drop_table("categories")

    op.drop_index("ix_users_email", table_name="users")
    op.drop_index("ix_users_username", table_name="users")
    op.drop_index("ix_users_id", table_name="users")
    op.drop_table("users")

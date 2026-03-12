"""initial

Revision ID: 0001_initial
Revises: 
Create Date: 2026-01-01
"""
from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("sales", sa.Column("order_id", sa.String(), primary_key=True), sa.Column("order_date", sa.Date(), nullable=False), sa.Column("product_id", sa.String(), nullable=False), sa.Column("region_id", sa.String(), nullable=False), sa.Column("customer_id", sa.String(), nullable=False), sa.Column("revenue", sa.Float(), nullable=False), sa.Column("quantity", sa.Integer(), nullable=False), sa.Column("cost", sa.Float(), nullable=False))
    op.create_table("products", sa.Column("product_id", sa.String(), primary_key=True), sa.Column("product_name", sa.String(), nullable=False), sa.Column("category", sa.String(), nullable=False), sa.Column("subcategory", sa.String(), nullable=False), sa.Column("price", sa.Float(), nullable=False))
    op.create_table("customers", sa.Column("customer_id", sa.String(), primary_key=True), sa.Column("segment", sa.String(), nullable=False), sa.Column("country", sa.String(), nullable=False), sa.Column("signup_date", sa.Date(), nullable=False), sa.Column("churned", sa.Boolean(), nullable=False))
    op.create_table("regions", sa.Column("region_id", sa.String(), primary_key=True), sa.Column("region_name", sa.String(), nullable=False), sa.Column("market", sa.String(), nullable=False))
    op.create_table("churn", sa.Column("month", sa.String(), primary_key=True), sa.Column("segment", sa.String(), primary_key=True), sa.Column("churn_rate", sa.Float(), nullable=False), sa.Column("retained_customers", sa.Integer(), nullable=False))
    op.create_table("question_runs", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("request_id", sa.String(64), nullable=False), sa.Column("question", sa.Text(), nullable=False), sa.Column("response_json", sa.JSON(), nullable=False), sa.Column("model", sa.String(128), nullable=False), sa.Column("created_at", sa.DateTime(), nullable=False))
    op.create_table("generated_charts", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("question_run_id", sa.Integer(), sa.ForeignKey("question_runs.id"), nullable=False), sa.Column("chart_id", sa.String(128), nullable=False, unique=True), sa.Column("title", sa.String(255), nullable=False), sa.Column("path", sa.String(255), nullable=False), sa.Column("created_at", sa.DateTime(), nullable=False))
    op.create_table("tool_call_logs", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("question_run_id", sa.Integer(), sa.ForeignKey("question_runs.id")), sa.Column("server", sa.String(64), nullable=False), sa.Column("tool", sa.String(128), nullable=False), sa.Column("status", sa.String(32), nullable=False), sa.Column("latency_ms", sa.Integer(), nullable=False), sa.Column("output_summary", sa.Text(), nullable=False), sa.Column("created_at", sa.DateTime(), nullable=False))


def downgrade() -> None:
    op.drop_table("tool_call_logs")
    op.drop_table("generated_charts")
    op.drop_table("question_runs")
    op.drop_table("churn")
    op.drop_table("regions")
    op.drop_table("customers")
    op.drop_table("products")
    op.drop_table("sales")

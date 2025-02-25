"""Correction des relations User, Wishlist et Collection

Revision ID: 56fae9bbf0a9
Revises: 
Create Date: 2025-02-24 11:48:25.810202

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '56fae9bbf0a9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Supprimer la contrainte de clé étrangère avant de supprimer la table `set`
    with op.batch_alter_table('card', schema=None) as batch_op:
        batch_op.drop_constraint('card_ibfk_1', type_='foreignkey')

    # Supprimer la table `set` après avoir supprimé la contrainte de clé étrangère
    op.drop_table('set')

    # Modification de la table 'card'
    with op.batch_alter_table('card', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=mysql.VARCHAR(length=100),
               type_=sa.String(length=200),
               existing_nullable=False)
        batch_op.drop_column('story')
        batch_op.drop_column('image')
        batch_op.drop_column('cardIdentifier')
        batch_op.drop_column('set_id')
        batch_op.drop_column('rarity')
        batch_op.drop_column('number')
        batch_op.drop_column('api_id')
        batch_op.drop_column('thumbnail')
        batch_op.drop_column('description')
        batch_op.drop_column('version')

    # Modification de la table 'collection'
    with op.batch_alter_table('collection', schema=None) as batch_op:
        batch_op.drop_column('id')
        batch_op.drop_column('added_at')

    # Modification de la table 'user'
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('username',
               existing_type=mysql.VARCHAR(length=50),
               type_=sa.String(length=150),
               existing_nullable=False)
        batch_op.alter_column('email',
               existing_type=mysql.VARCHAR(length=100),
               type_=sa.String(length=150),
               existing_nullable=False)
        batch_op.alter_column('password_hash',
               existing_type=mysql.VARCHAR(length=255),
               type_=sa.String(length=256),
               existing_nullable=False)

    # Modification de la table 'wishlist'
    with op.batch_alter_table('wishlist', schema=None) as batch_op:
        batch_op.drop_column('id')
        batch_op.drop_column('added_at')


    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('wishlist', schema=None) as batch_op:
        batch_op.add_column(sa.Column('added_at', mysql.DATETIME(), nullable=True))
        batch_op.add_column(sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False))

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('password_hash',
               existing_type=sa.String(length=256),
               type_=mysql.VARCHAR(length=255),
               existing_nullable=False)
        batch_op.alter_column('email',
               existing_type=sa.String(length=150),
               type_=mysql.VARCHAR(length=100),
               existing_nullable=False)
        batch_op.alter_column('username',
               existing_type=sa.String(length=150),
               type_=mysql.VARCHAR(length=50),
               existing_nullable=False)

    with op.batch_alter_table('collection', schema=None) as batch_op:
        batch_op.add_column(sa.Column('added_at', mysql.DATETIME(), nullable=True))
        batch_op.add_column(sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False))

    with op.batch_alter_table('card', schema=None) as batch_op:
        batch_op.add_column(sa.Column('version', mysql.VARCHAR(length=50), nullable=False))
        batch_op.add_column(sa.Column('description', mysql.TEXT(), nullable=True))
        batch_op.add_column(sa.Column('thumbnail', mysql.VARCHAR(length=255), nullable=True))
        batch_op.add_column(sa.Column('api_id', mysql.VARCHAR(length=100), nullable=False))
        batch_op.add_column(sa.Column('number', mysql.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('rarity', mysql.VARCHAR(length=50), nullable=False))
        batch_op.add_column(sa.Column('set_id', mysql.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('cardIdentifier', mysql.VARCHAR(length=100), nullable=False))
        batch_op.add_column(sa.Column('image', mysql.VARCHAR(length=255), nullable=True))
        batch_op.add_column(sa.Column('story', mysql.TEXT(), nullable=True))
        batch_op.create_foreign_key('card_ibfk_1', 'set', ['set_id'], ['id'])
        batch_op.create_index('api_id', ['api_id'], unique=True)
        batch_op.alter_column('name',
               existing_type=sa.String(length=200),
               type_=mysql.VARCHAR(length=100),
               existing_nullable=False)

    op.create_table('set',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('api_id', mysql.VARCHAR(length=100), nullable=False),
    sa.Column('name', mysql.VARCHAR(length=100), nullable=False),
    sa.Column('code', mysql.VARCHAR(length=50), nullable=False),
    sa.Column('release_date', sa.DATE(), nullable=True),
    sa.Column('prerelease_date', sa.DATE(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    with op.batch_alter_table('set', schema=None) as batch_op:
        batch_op.create_index('code', ['code'], unique=True)
        batch_op.create_index('api_id', ['api_id'], unique=True)

    # ### end Alembic commands ###

import importlib
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
from stardew.core.db.base import Base

target_metadata = Base.metadata

# 每次新增module就要在此列表进行添加
model_modules = {
	"stardew.models.system"
}
for module in model_modules:
	importlib.import_module(module)

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.
from stardew.settings import settings

def get_url():
	return settings.SQLALCHEMY_DATABASE_URI


def run_migrations_offline():
	"""Run migrations in 'offline' mode.

	This configures the context with just a URL
	and not an Engine, though an Engine is acceptable
	here as well.  By skipping the Engine creation
	we don't even need a DBAPI to be available.

	Calls to context.execute() here emit the given string to the
	script output.

	"""
	context.configure(
		url=get_url(),
		target_metadata=target_metadata,
		literal_binds=True
	)

	with context.begin_transaction():
		context.run_migrations()


def run_migrations_online():
	"""Run migrations in 'online' mode.

	In this scenario we need to create an Engine
	and associate a connection with the context.

	"""

	def process_revision_directives(context, revision, directives):
		if getattr(config.cmd_opts, 'autogenerate', False):
			script = directives[0]
			if script.upgrade_ops.is_empty():
				directives[:] = []

	configuration = config.get_section(config.config_ini_section)
	configuration["sqlalchemy.url"] = get_url()
	connectable = engine_from_config(
		configuration,
		prefix="sqlalchemy.",
		poolclass=pool.NullPool,
	)

	with connectable.connect() as connection:
		context.configure(
			connection=connection,
			target_metadata=target_metadata,
			process_revision_directives=process_revision_directives,
			compare_type=True,  # 检查字段类型
			compare_server_default=True,  # 比较默认值
		)

		with context.begin_transaction():
			context.run_migrations()


if context.is_offline_mode():
	run_migrations_offline()
else:
	run_migrations_online()

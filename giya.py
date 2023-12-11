import os

from dotenv import load_dotenv

load_dotenv()

import click
from app import create_app, db
from app.models.user import Permission, Role, User
from flask_migrate import Migrate

app = create_app(os.getenv("FLASK_CONFIG") or "dev")
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role, Permission=Permission)


@app.cli.command()
@click.argument("test_names", nargs=-1)
def test(test_names):
    """Run unit tests"""
    import unittest

    if test_names:
        """Run specific unit tests.

        Example:
        $ flask test tests.test_auth_api tests.test_user_model ...
        """
        tests = unittest.TestLoader().loadTestsFromNames(test_names)

    else:
        tests = unittest.TestLoader().discover("tests", pattern="test*.py")

    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0

    # Return 1 if tests failed, won't reach here if succeeded.
    return 1

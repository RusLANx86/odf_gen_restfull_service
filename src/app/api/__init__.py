"""Apis."""
from .example.views import example_blueprint
from ..tools.common import BlueprintContainer
from .user import user_blueprint
from .data import data_blueprint


blueprints = []
blueprints.append(BlueprintContainer(user_blueprint, "/api/user"))
blueprints.append(BlueprintContainer(data_blueprint, "/api/data"))
blueprints.append(BlueprintContainer(example_blueprint, "/api/example"))

import inspect
from core.roles import SYSTEM_ADMIN
from rest_access_policy import AccessPolicy


class BaseAccessPolicy(AccessPolicy):
    @classmethod
    def scope_queryset(cls, request, qs):
        return qs.all()

    def get_policy_statements(self, request, view):
        return self.statements + [
            {"principal": f"group:{SYSTEM_ADMIN}", "action": "*", "effect": "allow"},
            {
                "principal": "*",
                "action": ["permissions", "metadata"],
                "effect": "allow",
            },
        ]
    def is_viewset_class(self, view):
        return inspect.isclass(view)

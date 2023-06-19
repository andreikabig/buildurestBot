class RoleValidatorService:
    ADMIN = "admin"
    CLIENT = "client"

    @staticmethod
    def ValidateAdminRole(user):
        return user.role.name == "admin"
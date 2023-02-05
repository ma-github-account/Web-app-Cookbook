from django.contrib.admin.apps import AdminConfig


class CookbookAdminConfig(AdminConfig):
    default_site = 'cookbook_admin.admin.CookbookAdmin'

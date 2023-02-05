from django.contrib import admin

class CookbookAdminSite(admin.AdminSite):
    title_header = 'Cookbook Admin'
    site_header = 'Cookbook administration'
    index_title = 'Cookbook site admin'


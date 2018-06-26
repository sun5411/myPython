#coding:utf-8

from django.contrib import admin
from importInfo.models import AvailableCids,ImportStatusRecord
# Register your models here.

class StatusAdmin(admin.ModelAdmin):
    list_display = ('cid','status', 'curr_sql_date','tried_num','duration','curr_sql_file','import_time')
    search_fields = ('cid','status','curr_sql_date','curr_sql_file')
    list_filter = ('status','curr_sql_date')
    date_hierarchy = 'curr_sql_date'
    ordering = ('-import_time',)
    #fields = ('cid','status','curr_sql_date','curr_sql_file')
    #filter_horizontal = ('mport_time',)

class CidAdmin(admin.ModelAdmin):
    list_display = ('cid','start_date')
    search_fields = ('cid','start_date')
    date_hierarchy = 'start_date' 
    ordering = ('-start_date',)

admin.site.site_header = "乐影影院数据导入管理"
admin.site.disable_action('delete_selected')
admin.site.register(AvailableCids,CidAdmin)
admin.site.register(ImportStatusRecord,StatusAdmin)

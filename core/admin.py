from django.contrib import admin
from .models import Province, Statistic, Alert, Project, ChartData, DevelopmentPillar, NavigationItem, DashboardSettings

admin.site.register(ChartData)
admin.site.register(DevelopmentPillar)
admin.site.register(NavigationItem)
admin.site.register(DashboardSettings)

@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('name', 'population', 'area')
    search_fields = ('name',)

@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    list_display = ('title', 'value', 'color_class', 'order')
    list_editable = ('order', 'color_class')

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_urgent', 'created_at')
    list_filter = ('is_urgent',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'province', 'status', 'latitude', 'longitude')
    list_filter = ('province', 'status')

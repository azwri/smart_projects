from django.shortcuts import render
from .models import Statistic, Project, Alert, ChartData, DevelopmentPillar
import json
from django.core.serializers.json import DjangoJSONEncoder

def index(request):
    # 1. Statistics Cards
    statistics = Statistic.objects.all()

    # 2. Alerts
    alerts = Alert.objects.all()

    # 3. Projects (for Map)
    projects = Project.objects.select_related('province').all()
    projects_data = []
    for p in projects:
        projects_data.append({
            'name': p.name,
            'latitude': p.latitude,
            'longitude': p.longitude,
            'status': p.status,
            'province__name': p.province.name
        })

    # 4. Charts Data
    # Line Chart
    line_current = ChartData.objects.filter(chart_type='line_current').order_by('month')
    line_previous = ChartData.objects.filter(chart_type='line_previous').order_by('month')
    
    line_chart_data = {
        'labels': [d.label for d in line_current],
        'current': [d.value for d in line_current],
        'previous': [d.value for d in line_previous]
    }

    # Bar Chart
    bar_monthly = ChartData.objects.filter(chart_type='bar_monthly').order_by('month')
    bar_chart_data = {
        'labels': [d.label for d in bar_monthly],
        'values': [d.value for d in bar_monthly],
        'colors': [d.color for d in bar_monthly]
    }

    # Donut Chart
    pillars = DevelopmentPillar.objects.all()
    donut_chart_data = {
        'labels': [p.name for p in pillars],
        'values': [p.value for p in pillars],
        'colors': [p.color for p in pillars]
    }

    # 5. Map Legend Data (Province Stats)
    from django.db.models import Count, Q
    from .models import Province
    
    provinces = Province.objects.annotate(
        total=Count('projects'),
        completed=Count('projects', filter=Q(projects__status='completed')),
        in_progress=Count('projects', filter=Q(projects__status='in_progress')),
        delayed=Count('projects', filter=Q(projects__status='delayed')),
        planned=Count('projects', filter=Q(projects__status='planned')),
    ).filter(total__gt=0)

    province_stats = []
    for p in provinces:
        stats = {
            'name': p.name,
            'total': p.total,
            'completed_pct': (p.completed / p.total) * 100,
            'in_progress_pct': (p.in_progress / p.total) * 100,
            'delayed_pct': (p.delayed / p.total) * 100,
            'planned_pct': (p.planned / p.total) * 100,
        }
        province_stats.append(stats)

    # 6. Navigation Items
    from .models import NavigationItem
    nav_items = NavigationItem.objects.all()

    # 7. Dashboard Settings
    from .models import DashboardSettings
    dashboard_settings = DashboardSettings.objects.first()
    if not dashboard_settings:
        dashboard_settings = DashboardSettings.objects.create()

    context = {
        'statistics': statistics,
        'alerts': alerts,
        'projects_json': json.dumps(projects_data, cls=DjangoJSONEncoder),
        'line_chart_json': json.dumps(line_chart_data, cls=DjangoJSONEncoder),
        'bar_chart_json': json.dumps(bar_chart_data, cls=DjangoJSONEncoder),
        'donut_chart_json': json.dumps(donut_chart_data, cls=DjangoJSONEncoder),
        'pillars': pillars,
        'province_stats': province_stats,
        'nav_items': nav_items,
        'projects': projects,
        'dashboard_settings': dashboard_settings,
    }
    return render(request, 'core/index.html', context)

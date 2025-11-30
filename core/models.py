from django.db import models

class Province(models.Model):
    name = models.CharField(max_length=100, verbose_name="Province Name")
    description = models.TextField(blank=True, verbose_name="Description")
    population = models.IntegerField(null=True, blank=True, verbose_name="Population")
    area = models.FloatField(null=True, blank=True, verbose_name="Area (km²)")
    # GeoJSON data can be stored as a JSONField or just a text field if simple
    # For simplicity and standard SQLite support without GeoDjango extensions, we'll use TextField for now
    geojson_data = models.TextField(blank=True, help_text="GeoJSON geometry for the province", verbose_name="GeoJSON Data")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Province"
        verbose_name_plural = "Provinces"

class Statistic(models.Model):
    title = models.CharField(max_length=100, verbose_name="Title")
    value = models.CharField(max_length=50, verbose_name="Value")
    color_class = models.CharField(max_length=50, default='bg-blue-600', help_text="Tailwind background class (e.g., bg-red-600)", verbose_name="Background Color")
    order = models.IntegerField(default=0, verbose_name="Display Order")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']
        verbose_name = "Statistic"
        verbose_name_plural = "Statistics"

class Alert(models.Model):
    title = models.CharField(max_length=100, verbose_name="Title")
    content = models.TextField(verbose_name="Content")
    action_text = models.CharField(max_length=50, blank=True, verbose_name="Action Button Text")
    is_urgent = models.BooleanField(default=False, verbose_name="Is Urgent?")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name = "AI Alert"
        verbose_name_plural = "AI Alerts"

class Project(models.Model):
    name = models.CharField(max_length=100, verbose_name="Project Name")
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='projects', verbose_name="Province")
    latitude = models.FloatField(verbose_name="Latitude")
    longitude = models.FloatField(verbose_name="Longitude")
    status = models.CharField(max_length=50, choices=[
        ('completed', 'Completed'),
        ('in_progress', 'In Progress'),
        ('delayed', 'Delayed'),
        ('planned', 'Planned')
    ], default='planned', verbose_name="Status")
    video = models.CharField(max_length=200, blank=True, null=True, verbose_name="Project Video", help_text="Path to video file (e.g., /static/core/video.mp4)")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"

class ChartData(models.Model):
    CHART_TYPES = [
        ('line_current', 'Line Chart (Current Year)'),
        ('line_previous', 'Line Chart (Previous Year)'),
        ('bar_monthly', 'Bar Chart (Monthly Status)'),
    ]
    
    chart_type = models.CharField(max_length=50, choices=CHART_TYPES, verbose_name="Chart Type")
    month = models.IntegerField(verbose_name="Month (1-12)")
    value = models.IntegerField(verbose_name="Value")
    label = models.CharField(max_length=50, blank=True, verbose_name="Label (e.g., Month Name)")
    color = models.CharField(max_length=50, blank=True, verbose_name="Color (Hex or Class)")

    def __str__(self):
        return f"{self.get_chart_type_display()} - {self.label}: {self.value}"

    class Meta:
        ordering = ['chart_type', 'month']
        verbose_name = "Chart Data Point"
        verbose_name_plural = "Chart Data Points"

class DevelopmentPillar(models.Model):
    name = models.CharField(max_length=100, verbose_name="Pillar Name")
    value = models.IntegerField(verbose_name="Value (%)")
    color = models.CharField(max_length=50, default='#3B82F6', verbose_name="Color (Hex)")
    order = models.IntegerField(default=0, verbose_name="Display Order")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']
        verbose_name = "Development Pillar"
        verbose_name_plural = "Development Pillars"

class NavigationItem(models.Model):
    title = models.CharField(max_length=100, verbose_name="Title")
    url = models.CharField(max_length=200, default='#', verbose_name="URL")
    icon_class = models.CharField(max_length=50, blank=True, default='bi-chevron-left', verbose_name="Bootstrap Icon Class")
    order = models.IntegerField(default=0, verbose_name="Display Order")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']
        verbose_name = "Navigation Item"
        verbose_name_plural = "Navigation Items"

class DashboardSettings(models.Model):
    site_title = models.CharField(max_length=200, default="المشاريع الذكية", verbose_name="Site Title")
    ai_alerts_title = models.CharField(max_length=200, default="التنبيهات الذكية - AI Alerts", verbose_name="AI Alerts Title")
    
    def __str__(self):
        return "Dashboard Settings"

    class Meta:
        verbose_name = "Dashboard Settings"
        verbose_name_plural = "Dashboard Settings"

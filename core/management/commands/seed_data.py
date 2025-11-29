from django.core.management.base import BaseCommand
from core.models import Statistic, Project, Province, Alert, ChartData, DevelopmentPillar
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Seeds the database with dummy data for the dashboard'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # Clear existing data
        Statistic.objects.all().delete()
        Project.objects.all().delete()
        Province.objects.all().delete()
        Alert.objects.all().delete()
        ChartData.objects.all().delete()
        DevelopmentPillar.objects.all().delete()

        # 1. Statistics
        stats = [
            {'title': 'المبادرات التطويرية', 'value': '42', 'color_class': 'bg-gray-600', 'order': 1}, # Changed from 29
            {'title': 'المشاريع المتعثرة', 'value': '3', 'color_class': 'bg-red-600', 'order': 2}, # Changed from 5
            {'title': 'المشاريع قيد التنفيذ', 'value': '25', 'color_class': 'bg-yellow-500', 'order': 3}, # Changed from 20
            {'title': 'المشاريع المكتملة', 'value': '45', 'color_class': 'bg-green-500', 'order': 4}, # Changed from 30
            {'title': 'إجمالي المشاريع', 'value': '73', 'color_class': 'bg-blue-600', 'order': 5}, # Changed from 35
        ]
        for stat in stats:
            Statistic.objects.create(**stat)

        # 2. Provinces
        provinces_data = [
            {'name': 'أبها', 'lat': 18.2465, 'lng': 42.5117},
            {'name': 'بيشة', 'lat': 20.0005, 'lng': 42.6050},
            {'name': 'طريب', 'lat': 18.2, 'lng': 43.2}, # Approx
            {'name': 'خميس مشيط', 'lat': 18.3, 'lng': 42.73},
        ]
        provinces = {}
        for p_data in provinces_data:
            prov = Province.objects.create(name=p_data['name'])
            provinces[p_data['name']] = {'obj': prov, 'lat': p_data['lat'], 'lng': p_data['lng']}

        # 3. Projects
        # Create some random projects around the provinces
        statuses = ['completed', 'in_progress', 'delayed', 'planned']
        for i in range(20):
            prov_name = random.choice(list(provinces.keys()))
            prov_info = provinces[prov_name]
            
            # Random offset
            lat = prov_info['lat'] + random.uniform(-0.1, 0.1)
            lng = prov_info['lng'] + random.uniform(-0.1, 0.1)
            
            Project.objects.create(
                name=f"Project {i+1}",
                province=prov_info['obj'],
                latitude=lat,
                longitude=lng,
                status=random.choice(statuses)
            )

        # 4. Alerts
        alerts = [
            {'title': 'تنبيه استراتيجي عاجل', 'content': 'البنية التحتية الرقمية: مشروع رفع سرعة الإنترنت في المحافظات متأخر بنسبة 15% عن الخطة المستهدفة.', 'action_text': 'عرض التفاصيل', 'is_urgent': True},
            {'title': 'إشارة متابعة', 'content': 'الخدمات الإلكترونية: نظام التعاملات الإلكترونية (إمارة بلا ورق) تجاوز 90% من التنفيذ.', 'action_text': 'عرض التفاصيل', 'is_urgent': False},
            {'title': 'فرصة مؤثرة', 'content': 'التكامل والحوكمة: ربط نظام الموارد البشرية مع منصة وزارة الداخلية حقق تكاملاً بنسبة 70%.', 'action_text': 'عرض التفاصيل', 'is_urgent': False},
            {'title': 'بُشرى نجاح', 'content': 'استمرارية الأعمال: مشروع البريد الإلكتروني (ديم) أنهى اختبارات الأمان بنجاح.', 'action_text': 'عرض التفاصيل', 'is_urgent': False},
        ]
        for alert in alerts:
            Alert.objects.create(**alert)

        # 5. Chart Data
        # Line Chart - Current Year
        current_year_data = [20, 25, 22, 30, 28, 35, 40] # Changed values
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul']
        for i, val in enumerate(current_year_data):
            ChartData.objects.create(
                chart_type='line_current',
                month=i+1,
                value=val,
                label=months[i]
            )

        # Line Chart - Previous Year
        prev_year_data = [10, 15, 12, 18, 20, 22, 25] # Changed values
        for i, val in enumerate(prev_year_data):
            ChartData.objects.create(
                chart_type='line_previous',
                month=i+1,
                value=val,
                label=months[i]
            )

        # Bar Chart - Monthly Status
        bar_data = [8, 15, 10, 15, 6, 12, 8, 15, 10, 16, 6, 12]
        bar_colors = ['#1F2937', '#F59E0B', '#1F2937', '#F59E0B', '#93C5FD', '#DC2626', '#4B5563', '#F59E0B', '#DC2626', '#1F2937', '#DC2626', '#1F2937']
        months_full = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        for i, val in enumerate(bar_data):
            ChartData.objects.create(
                chart_type='bar_monthly',
                month=i+1,
                value=val,
                label=months_full[i],
                color=bar_colors[i]
            )

        # 6. Development Pillars (Donut)
        pillars = [
            {'name': 'البنية التحتية الرقمية', 'value': 40, 'color': '#059669', 'order': 1},
            {'name': 'الخدمات الإلكترونية', 'value': 20, 'color': '#F59E0B', 'order': 2},
            {'name': 'التكامل والحوكمة', 'value': 15, 'color': '#4B5563', 'order': 3},
            {'name': 'استمرارية الأعمال', 'value': 25, 'color': '#DC2626', 'order': 4},
        ]
        for pillar in pillars:
            DevelopmentPillar.objects.create(**pillar)

        self.stdout.write(self.style.SUCCESS('Successfully seeded database'))

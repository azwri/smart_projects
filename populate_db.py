
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Statistic, Alert, Project, Province, ChartData, DevelopmentPillar, NavigationItem

def populate():
    print("Populating database...")

    # 1. Alerts
    Alert.objects.all().delete()
    Alert.objects.create(title="تنبيه انخفاض الأداء", content="انخفض أداء المشاريع في منطقة عسير بنسبة 10% مقارنة بالشهر الماضي.", action_text="عرض التفاصيل", is_urgent=True)
    Alert.objects.create(title="اكتمال مشروع جديد", content="تم الانتهاء من مشروع تطوير الواجهة البحرية بنجاح.", action_text="عرض التقرير", is_urgent=False)
    Alert.objects.create(title="تحديث البيانات", content="تم تحديث بيانات المشاريع لشهر نوفمبر.", action_text="", is_urgent=False)
    print("Alerts populated.")

    # 2. Statistics
    Statistic.objects.all().delete()
    Statistic.objects.create(title="المبادرات التطويرية", value="29", color_class="bg-gray-600", order=1)
    Statistic.objects.create(title="المشاريع المتعثرة", value="5", color_class="bg-red-600", order=2)
    Statistic.objects.create(title="المشاريع قيد التنفيذ", value="20", color_class="bg-yellow-500", order=3)
    Statistic.objects.create(title="المشاريع المكتملة", value="30", color_class="bg-green-500", order=4)
    Statistic.objects.create(title="إجمالي المشاريع", value="35", color_class="bg-blue-600", order=5)
    print("Statistics populated.")

    # 3. Provinces & Projects
    Project.objects.all().delete()
    Province.objects.all().delete()
    
    bisha = Province.objects.create(name="بيشة")
    abha = Province.objects.create(name="أبها")
    tareeb = Province.objects.create(name="طريب")

    Project.objects.create(name="تطوير وسط المدينة", province=bisha, latitude=20.0, longitude=42.6, status="completed")
    Project.objects.create(name="مشروع الإسكان", province=bisha, latitude=20.01, longitude=42.61, status="completed")
    Project.objects.create(name="حديقة الملك", province=bisha, latitude=19.99, longitude=42.59, status="in_progress")
    
    Project.objects.create(name="جسر أبها", province=abha, latitude=18.2, longitude=42.5, status="in_progress")
    Project.objects.create(name="ممشى الضباب", province=abha, latitude=18.21, longitude=42.51, status="delayed")
    
    Project.objects.create(name="مستشفى طريب", province=tareeb, latitude=18.5, longitude=43.0, status="delayed")
    print("Provinces and Projects populated.")

    # 4. Chart Data
    ChartData.objects.all().delete()
    # Line Chart (Current Year)
    for i in range(1, 13):
        ChartData.objects.create(chart_type="line_current", month=i, value=i*10 + 5, label=f"شهر {i}")
    # Line Chart (Previous Year)
    for i in range(1, 13):
        ChartData.objects.create(chart_type="line_previous", month=i, value=i*8 + 10, label=f"شهر {i}")
    
    # Bar Chart
    ChartData.objects.create(chart_type="bar_monthly", month=1, value=65, label="مكتمل", color="#10B981")
    ChartData.objects.create(chart_type="bar_monthly", month=2, value=59, label="قيد التنفيذ", color="#F59E0B")
    ChartData.objects.create(chart_type="bar_monthly", month=3, value=80, label="مخطط", color="#3B82F6")
    ChartData.objects.create(chart_type="bar_monthly", month=4, value=81, label="متأخر", color="#EF4444")
    print("Chart Data populated.")

    # 5. Development Pillars
    DevelopmentPillar.objects.all().delete()
    DevelopmentPillar.objects.create(name="الاقتصاد المزدهر", value=30, color="#10B981", order=1)
    DevelopmentPillar.objects.create(name="المجتمع الحيوي", value=40, color="#3B82F6", order=2)
    DevelopmentPillar.objects.create(name="الوطن الطموح", value=30, color="#F59E0B", order=3)
    print("Development Pillars populated.")

    # 6. Navigation Items
    NavigationItem.objects.all().delete()
    NavigationItem.objects.create(title="المشاريع", url="#", icon_class="bi-briefcase", order=1)
    NavigationItem.objects.create(title="محاور الخطة التطويرية", url="#", icon_class="bi-pie-chart", order=2)
    NavigationItem.objects.create(title="المستثمرون", url="#", icon_class="bi-people", order=3)
    NavigationItem.objects.create(title="التقارير", url="#", icon_class="bi-file-earmark-text", order=4)
    print("Navigation Items populated.")

if __name__ == '__main__':
    populate()

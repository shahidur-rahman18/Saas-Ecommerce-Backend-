from django.db import models
from django_tenants.models import TenantMixin, DomainMixin

# Create your models here.
class Client(TenantMixin):
    """
    Client Model (Tenant)
    সেন্ট্রাল Public Schema-তে সংরক্ষিত থাকবে।
    প্রতিটি মার্চেন্টের স্কিমা নাম এবং সাবস্ক্রিপশন তথ্য ট্র্যাক করে।
    """
    name = models.CharField(max_length=100)
    paid_until = models.DateField(null=True, blank=True)
    on_trial = models.BooleanField(default=True)
    created_on = models.DateField(auto_now_add=True)

    # schema_name ফিল্ডটি TenantMixin থেকে অটোমেটিক যুক্ত হবে।
    # auto_create_schema = True (TenantMixin-এ ডিফল্টভাবে ট্রু থাকে)

    def __str__(self):
        return f"{self.name} ({self.schema_name})"


class Domain(DomainMixin):
    """
    Domain Model
    সেন্ট্রাল Public Schema-তে সংরক্ষিত থাকবে।
    Client/Tenant-এর সাথে Subdomain বা Custom Domain লিংক করে।
    """
    pass
